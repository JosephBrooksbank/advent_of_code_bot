from discord.ext import commands
import discord
from discord import app_commands, User, Member
from dotenv import load_dotenv
import os
import sqlite
import aoc_leaderboard

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True
year = "2025"
bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)}")

async def get_user_roles(user: User):
    return user.roles

async def get_missing_roles(user: User, days):
    roles = await get_user_roles(user)
    missing_roles = []
    for day in days:
        if day not in roles:
            missing_roles.append(day)
    return missing_roles

async def get_role_by_name(name):
    for role in bot.guilds[0].roles:
        if role.name == name:
            return role
    else:
        role = await add_role_to_server(name)
        return role

async def add_role_to_server(name):
    server = bot.guilds[0]
    role = await server.create_role(name=name)
    await add_channel_for_role(role)
    return role


async def add_channel_for_role(role):

    guild = bot.guilds[0]
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        role: discord.PermissionOverwrite(read_messages=True)
    }
    return await guild.create_text_channel(role.name + "-solution-" + year, overwrites=overwrites, category=guild.categories[1])

async def add_roles(user: Member, roles):
    for role in roles:
        server_role = await get_role_by_name(role)
        await user.add_roles(server_role)

async def sync_user(interaction, aoc_userId, leaderboard):
    for member in leaderboard["members"]:
        if member == aoc_userId:
            days_completed = aoc_leaderboard.get_days_completed(member)
            missing_roles = await get_missing_roles(interaction.user, days_completed)
            await add_roles(interaction.user, missing_roles)
            break


@bot.tree.command(name="sync")
async def sync(interaction: discord.Interaction):
    db = sqlite.Sqlite()
    leaderboard = aoc_leaderboard.refresh_leaderboard()
    if not leaderboard:
        await interaction.message.send_message("Failed to get leaderboard, likely due to invalid session cookie in bot", ephemeral=True)
    user = db.get_discord_user(interaction.user.id)
    if user:
        await sync_user(interaction, user[0], leaderboard)
        await interaction.response.send_message("Synced!", ephemeral=True)
    else:
        await interaction.response.send_message("You are not registered, use /register", ephemeral=True)

@bot.tree.command(name="register")
@app_commands.describe(username = "Enter the name you see in the top right of advent of code")
async def register(interaction: discord.Interaction, username: str):
    username = username.strip()
    db = sqlite.Sqlite()
    leaderboard = aoc_leaderboard.refresh_leaderboard()
    if not leaderboard:
        await interaction.message.send_message("Failed to get leaderboard, likely due to invalid session cookie in bot", ephemeral=True)
    for member in leaderboard["members"]:

        if leaderboard["members"][member]["name"].strip() == username:
            db.insert_user(interaction.user.id, member, username)
            await sync_user(interaction, member, leaderboard)

            await interaction.response.send_message(
                f"Registered {username} as AoC username for {interaction.user.name}", ephemeral=True)
            break
    else:
        print(leaderboard)
        await interaction.response.send_message(f"Could not find user {username} in leaderboard", ephemeral=True)


def run():
    bot.run(os.getenv("BOT_TOKEN"))