import discord_bot
from sqlite import Sqlite


def main():
    db = Sqlite()
    db.create_table()
    discord_bot.run()



if __name__ == "__main__":
    main()