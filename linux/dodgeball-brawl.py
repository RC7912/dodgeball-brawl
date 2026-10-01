#!/usr/bin/env python3
"""Dodgeball Brawl desktop app: runs the HTML5 game in a native GTK + WebKit window."""
import json
import os
import sqlite3
import sys

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("WebKit2", "4.1")
from gi.repository import Gdk, GLib, Gtk, WebKit2  # noqa: E402

APP_ID = "dodgeball-brawl"
TITLE = "Dodgeball Brawl"
SAVE_FILE = os.path.join(GLib.get_user_data_dir(), APP_ID, "save.json")


def read_legacy_save():
    """Saves from 1.2.0 lived in WebKit's localStorage, which WebKit doesn't always load back. Rescue them."""
    path = os.path.join(GLib.get_user_data_dir(), APP_ID, "localstorage", "file__0.localstorage")
    try:
        db = sqlite3.connect("file:%s?mode=ro" % path, uri=True)
        try:
            rows = dict(db.execute("SELECT key, value FROM ItemTable").fetchall())
        finally:
            db.close()
    except sqlite3.Error:
        return None
    text = lambda v: v.decode("utf-16-le") if isinstance(v, bytes) else v
    try:
        data = json.loads(text(rows["dodgeball-save"])) if "dodgeball-save" in rows else {}
        for diff in ("easy", "normal", "hard"):
            key = "dodgeball-endless-best-" + diff
            if key in rows:
                data.setdefault("best", {})[diff] = json.loads(text(rows[key]))
    except ValueError:
        return None
    return json.dumps(data) if data else None


def read_save():
    try:
        with open(SAVE_FILE, encoding="utf-8") as f:
            text = f.read()
        json.loads(text)  # only hand valid saves to the game
        return text
    except (OSError, ValueError):
        legacy = read_legacy_save()
        if legacy:
            write_save(legacy)
        return legacy


def write_save(text):
    json.loads(text)
    os.makedirs(os.path.dirname(SAVE_FILE), exist_ok=True)
    tmp = SAVE_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, SAVE_FILE)  # atomic: never leaves a half-written save


def find_game():
    here = os.path.dirname(os.path.realpath(__file__))
    for path in (os.path.join(here, "index.html"),                  # installed: /usr/share/dodgeball-brawl
                 os.path.join(here, "..", "index.html"),            # running from the repo's linux/ folder
                 "/usr/share/dodgeball-brawl/index.html"):
        if os.path.isfile(path):
            return os.path.realpath(path)
    sys.exit("Dodgeball Brawl: couldn't find index.html")


class GameWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title=TITLE)
        self.set_default_size(1100, 760)
        self.set_icon_name(APP_ID)
        self.fullscreen_on = False

        # the game saves through this handler; we write save.json right away
        content = WebKit2.UserContentManager()
        content.register_script_message_handler("dodgeballSave")
        content.connect("script-message-received::dodgeballSave", self.on_save)
        content.add_script(WebKit2.UserScript(
            "window.__desktopSave = %s;" % json.dumps(read_save()),
            WebKit2.UserContentInjectedFrames.TOP_FRAME,
            WebKit2.UserScriptInjectionTime.START, None, None))
        self.view = WebKit2.WebView.new_with_user_content_manager(content)
        settings = self.view.get_settings()
        settings.set_enable_webaudio(True)
        settings.set_enable_developer_extras(False)
        settings.set_media_playback_requires_user_gesture(False)
        # right click is the catch button in the game, so no browser context menu
        self.view.connect("context-menu", lambda *a: True)
        bg = Gdk.RGBA(); bg.parse("#0e0f14")
        self.view.set_background_color(bg)
        self.view.load_uri(GLib.filename_to_uri(find_game(), None))

        self.add(self.view)
        self.connect("key-press-event", self.on_key)
        self.show_all()
        self.view.grab_focus()

    def on_save(self, _content, result):
        try:
            write_save(result.get_js_value().to_string())
        except (OSError, ValueError) as err:
            print("Dodgeball Brawl: couldn't save:", err, file=sys.stderr)

    def on_key(self, _widget, event):
        if event.keyval == Gdk.KEY_F11:
            if self.fullscreen_on:
                self.unfullscreen()
            else:
                self.fullscreen()
            self.fullscreen_on = not self.fullscreen_on
            return True
        return False  # everything else goes to the game


class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="io.github.rc7912.DodgeballBrawl")

    def do_activate(self):
        win = self.get_active_window() or GameWindow(self)
        win.present()


if __name__ == "__main__":
    GLib.set_prgname(APP_ID)  # so the dock matches the .desktop file
    GLib.set_application_name(TITLE)
    sys.exit(App().run(sys.argv))
