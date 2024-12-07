# Advent of Code Discord Bot
This bot allows you to manage solution channels in your discord server.
Users can register their aoc user with their discord user, after which
the bot will sync their solutions with roles on the server.

## Using the Bot
1. Users will need to register their aoc account with
```
/register <aoc username>
```
which can be seen in the upper right of the aoc website. This will also sync them once.

2. After submitting solutions, users can then update their discord roles with
```
/sync
```

3. This bot will create a channel for each day called `day-X-solution`, which is viewable only by users with the role `day-X`.

## Setup
1. Clone the repository
2. Create a local venv with `python3 ./setup.py`
   3. this will install the required dependencies in an isolated environment
4. Create a `.env` file in the root of the project with the following content:
   ```
   BOT_TOKEN=<your bot token>
   LEADERBOARD_URL=<url to the leaderboard>
   SESSION_COOKIE=<your session cookie>
   ```
   A bot token can be obtained by creating a new bot on the discord developer portal. When adding it to your server,
it will need the following permissions:
* Manage Roles 
* Manage Channels 
* View Channels 
* Send Messages

   as well as the privileged gateway intents:

   1. message content

The leaderboard url comes from the advent of code website private leaderboard page after creating one.

The session cookie can be obtained by logging into aoc, opening dev tools, going to 'application' -> 'cookies' -> 'adventofcode.com' -> 'session' and copying the value.
It will last for roughly a month.

4. Run the bot
If you are running on a linux/systemctl system, you can use the `register.sh` script to register the bot as a service.
```
chmod +x register.sh
./register.sh
```
