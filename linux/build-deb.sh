#!/usr/bin/env bash
# Builds dist/dodgeball-brawl_<version>_all.deb
set -euo pipefail
VERSION="${1:-1.0.0}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
umask 022
PKG="$(mktemp -d)"
chmod 755 "$PKG"
trap 'rm -rf "$PKG"' EXIT

install -Dm755 "$ROOT/linux/dodgeball-brawl.py"      "$PKG/usr/share/dodgeball-brawl/dodgeball-brawl.py"
install -Dm644 "$ROOT/index.html"                    "$PKG/usr/share/dodgeball-brawl/index.html"
install -Dm644 "$ROOT/linux/dodgeball-brawl.desktop" "$PKG/usr/share/applications/dodgeball-brawl.desktop"
install -Dm644 "$ROOT/linux/dodgeball-brawl.svg"     "$PKG/usr/share/icons/hicolor/scalable/apps/dodgeball-brawl.svg"
mkdir -p "$PKG/usr/bin"
ln -s ../share/dodgeball-brawl/dodgeball-brawl.py "$PKG/usr/bin/dodgeball-brawl"

mkdir -p "$PKG/DEBIAN"
cat > "$PKG/DEBIAN/control" <<CTRL
Package: dodgeball-brawl
Version: $VERSION
Section: games
Priority: optional
Architecture: all
Depends: python3, python3-gi, gir1.2-gtk-3.0, gir1.2-webkit2-4.1
Maintainer: RC7912 <RC7912@users.noreply.github.com>
Homepage: https://github.com/RC7912/dodgeball-brawl
Description: One-ball dodgeball against CPU bots
 Fast top-down dodgeball: free-for-all or Blue vs Red teams, one ball,
 sit where you get hit and grab the ball to get back in. Bots dodge,
 catch, help each other and talk trash.
CTRL
cat > "$PKG/DEBIAN/postinst" <<'POST'
#!/bin/sh
set -e
command -v gtk-update-icon-cache >/dev/null && gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor || true
command -v update-desktop-database >/dev/null && update-desktop-database -q /usr/share/applications || true
POST
chmod 755 "$PKG/DEBIAN/postinst"

mkdir -p "$ROOT/dist"
dpkg-deb --build --root-owner-group "$PKG" "$ROOT/dist/dodgeball-brawl_${VERSION}_all.deb"
