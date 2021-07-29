# TGTK - A Telegram Bot

## Notes:

**do note that [yash-dk](https://github.com/yash-dk) will be creating a heroku fork of ttk, you should wait until he releases it in late may.**

all code do not belong to me, the original author is [yash-dk](https://github.com/yash-dk). please support his works by using the repo what is was made for, and leaving a star on his repo.

contact me on [telegram.](https://t.me/orsixtyone)

### how it works
a pypi package named [tgtk](https://pypi.org/project/tgtk) containing all bot code, easily to install with 
```
pip install tgtk
```
deploying from an docker image [reaitten/tk:latest](https://hub.docker.com/r/reaitten/tk/tags?page=1&ordering=last_updated)

## Deploy via Heroku
- Click the button below
- Add required variables
- Build
<p><a href="https://heroku.com/deploy?template=https://github.com/reaitten/tgtk"> <img src="https://img.shields.io/badge/Deploy%20To%20Heroku-blueviolet?style=for-the-badge&logo=heroku" width="200""/></a></p>
    
## Deploy via Heroku CLI
- Download [deploy.zip](https://github.com/reaitten/tgtk/releases).
- Unzip & open a command prompt.
- Change stack dyno to container:
```
heroku stack:set container --app your-app-name
```
- Initialise the project files as a Git Repository, push the repo to 'Heroku Git' and build the Docker Image:
```
git init
git add .
heroku git:remote -a your-app-name`
git commit -m "initial commit"
git push heroku main
```

## Prevent Sleeping Dyno
To keep the dyno alive, and prevent it from idling/sleeping, you can use [Kaffeine[(https://kaffeine.herokuapp.com/)

# Credits

> [yash-dk's TorToolkit](https://github.com/yash-dk/TorToolkit-Telegram)

> [tortoolkit's tortoolkit-Telegram](https://github.com/tk/tk-Telegram)

> [sahadz's tortoolkit-Telegram](https://github.com/sahadz/tk-Telegram)

> [dr-qaatil <3](https://github.com/dr-qaatil)

## Variables
`IS_VPS` = False
## Compulsory Vars

`API_HASH` = Obtained from Telegram 

`APP_ID` = Obtained from Telegram

`BOT_TOKEN` = Obtained from Botfather

`BASE_URL_OF_BOT` = IP/domain of your bot like "https://appname.herokuapp.com" (for heroku)

`AUTH_CHANNEL` = It is a list of IDs of all the allowed groups and useres who can use this bot in private. Seperated by spaces e.g: "-1022222 -33322211 11222333"

`DB_URI` = Postgres database URL.

`OWNER_ID` = self-explanatory, get value from [@userinfobot](https://t.me/userinfobot)

## Optional Vars
(IT IS RECOMMENDED TO SET THE OPTIONAL VARS FROM SETTINGS MENU, If not all vars atleast use settings menu for RCLONE that way is much easier.)

`EDIT_SLEEP_SECS` = Seconds to Sleep before edits. Recommended is 40.

`TG_UP_LIMIT` = Telegram Upload limit in bytes.

`BOT_CMD_POSTFIX` = Set this to your bot username if you want to add the username of your bot at the end of the commands. e.g `/leech@TorToolkitBot` so the value will be @TorToolkitBot

`FORCE_DOCUMENTS` = Should all the upload to telegram be made as documents or not.

`COMPLETED_STR` = Character used to denote completed progress. 

`REMAINING_STR` = Character used to denote remaining progress.

`RCLONE_BASE_DIR` = Rclone Base Directory to where stuff should be clonned. (cannot be configured from settings)

`LEECH_ENABLED` = Upload to telegram should be enabled or not.

`RCLONE_ENABLED` = Upload to rclone should be enabled or not.

`DEFAULT_TIMEOUT` = Default destination to choose if the user fails to choose upload destination in 60 seconds.

`RCLONE_CONFIG` = rclone file path. usually it's /app/rclone.conf if you uploaded rclone.conf onto the root directory of folder.

`DEF_RCLONE_DRIVE` = Default Drive for rclone to use. e.g: if my drive is called `tk-drive`, then i would add the value, `tk-drive`.

`MAX_YTPLAYLIST_SIZE` = Max size of a playlist that is allowed (Number of videos)

`MAX_TORRENT_SIZE` = Max torrent size in GBs

Other varibles are not to be changed.

## Commands
add in [@BotFather](https://t.me/BotFather)

    leech - To Leech a torrent or download a direct link
    ytdl - Donwload YouTube Video
    pytdl - Download YouTube Playlist
    about - About the bot
    status - Status of all the downloads
    stats - Get server status
    usettings - User Settings (private also)
    instadl - Instagram Post/Reel/IGTV download
    setthumb - Set the thumbnail
    clearthumb - Clear the thumbnail
    settings - Settings of the bot ⚠️ Admin Only
    pauseall - Pause all torrents⚠️ Admin Only
    resumeall - Resume all torrents⚠️ Admin Only
    purge - Delete all torrents ⚠️ Admin Only
    logs - Get the robot logs ⚠️ Admin Only
