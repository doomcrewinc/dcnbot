# sudoBot
A Discord bot written in Python

## Getting Started

These are needed to be able to run **sudobot**.

- [Python 3.5](https://www.python.org/)
- [Discord.py](https://github.com/Rapptz/discord.py)
- [Pillow](https://github.com/python-pillow/Pillow)
- [A unicode font like Noto Sans CJK (or a font of your choice)](https://www.google.com/get/noto/help/cjk/)

## Setup

Edit `config.sample.json` to your liking, then save it as `config.json`.

Place your selected font in `/data/fonts/` and be sure to link it in the config.

Once you're ready just run `python bot.py` in the active directory to start the bot.

## Cogs

**Sudobot** has different modules that you can enable / disable. The current 'cogs' available are : 

- General : General commands used within a server. 
- Fun : Commands that are fun for users to play with, and serve nothing other than lighthearted spammy goodness.
- Mod : Administrative and Moderative commands.

Currently, the only way to enable / disable these are through `config.json` but this will change in the future.

## Commands
```php
Fun:
  profile      Get an information card on a user in this server.
  profilesetup Setup your profile card
  setprofilebg Set a profile card background image.
General:
  joindistro   Join one of the many distribution roles available.
  listdistro   List available user distro roles.
  leavedistro  Leave a distribution role that is currently assigned to you.
  pacman       Pacman commands.
  source       Post a link to the bot source code.
  warnstatus   Check your own warning points.
Mod:
  kick         Kicks a member from the server.
  ban          Bans a member from the server.
  prune        Prunes user messages.
  prunebot     Prunes bot messages.
  warn         Warns a user
  liftwarn     Removes warning points from user
Misc:
  uptime       Check bot uptime.
  help         Shows this message.
```
