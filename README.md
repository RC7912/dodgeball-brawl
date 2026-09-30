# Dodgeball Brawl

A fast HTML5 dodgeball game you play against CPU opponents, right in your browser.

**▶ Play it here: https://rc7912.github.io/dodgeball-brawl/**

## Modes
- **Free-for-all:** you against 1–7 CPUs, no teams. Last one standing wins.
- **Teams:** Blue vs Red (1v1 up to 4v4). Stay on your side of the center line and knock out the whole other team.
- **Endless:** you against never-ending waves of bots that get bigger, faster and more accurate. 3 lives, +1 life per wave cleared (max 5). Your best run is saved.

## Rules
- There's only **one ball**.
- Get hit and you're out: you sit down right where you got hit.
- If the loose ball rolls up close to you, you grab it and you're **back in**, already holding the ball.
- Bots randomly help: sometimes a bot rolls the ball to someone who's sitting out so they can get back in. In Teams mode they only help teammates.
- Bots talk: they trash-talk, react to hits and catches, beg for the ball while sitting, and say thanks when helped.
- Catch a throw and the thrower is out. In Teams mode a catch also brings a teammate back.

## Controls
| Action | Keys |
| --- | --- |
| Move | WASD / Arrow keys |
| Aim | Mouse |
| Throw | Left click |
| Catch | Space / Right click |
| Dash | Shift |
| Pause | P / Esc / ⏸ button |
| Restart | R |

## Ubuntu app
Download `dodgeball-brawl_1.1.0_all.deb` from the [latest release](https://github.com/RC7912/dodgeball-brawl/releases/latest), then:

```bash
sudo apt install ./dodgeball-brawl_1.1.0_all.deb
```

Open **Dodgeball Brawl** from your app menu (or run `dodgeball-brawl`). Press **F11** for fullscreen.
To remove it: `sudo apt remove dodgeball-brawl`.

Build the package yourself with `linux/build-deb.sh` (output goes to `dist/`).

## Run locally
It's a single file: just open `index.html` in a browser.
