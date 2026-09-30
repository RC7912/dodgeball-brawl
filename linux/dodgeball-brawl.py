#!/usr/bin/env python3
"""Dodgeball Brawl desktop app: runs the HTML5 game in a native GTK + WebKit window."""
import os
import sys

import gi
gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("WebKit2", "4.1")
from gi.repository import Gdk, GLib, Gtk, WebKit2  # noqa: E402

APP_ID = "dodgeball-brawl"
TITLE = "Dodgeball Brawl"


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

        self.view = WebKit2.WebView()
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
