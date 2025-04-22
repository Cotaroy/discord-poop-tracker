from datetime import datetime

import discord
from discord import app_commands

from creds import TOKEN, SERVER_ID

from load import load_leaderboard, load_user, user_exists
from user import User
from validate import validate_date

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def blockify(inp) -> str:
    """blockify"""
    return '```' + inp + '```'


@client.event
async def on_ready():
    """prepare bot"""
    await tree.sync(guild=discord.Object(SERVER_ID))
    print("Bot ready")
    print("---------------------")


@tree.command(
    name="register",
    description="register your account to the poop tracker",
    guild=discord.Object(SERVER_ID)
)
async def register(interaction):
    """register user into pooper tracker"""
    id = interaction.user.id
    name = interaction.user.name
    already_registered = user_exists(id)

    if not already_registered:
        user = User(id, name)
        user.save()
        await interaction.response.send_message(f'Registering new user \n Welcome {name} :tada:')
    else:
        await interaction.response.send_message("You're already registered :rage:")


@tree.command(
    name="reregister",
    description="reset your user data",
    guild=discord.Object(SERVER_ID)
)
async def reregister(ctx):
    """reregister user into star rail sim players"""
    id = ctx.user.id
    name = ctx.user.name
    user = User(id, name)
    user.save()
    await ctx.response.send_message('Resetting user data')


@tree.command(
    name="log",
    description="log your poops, default to 1",
    guild=discord.Object(SERVER_ID)
)
async def log_poops(ctx, n: int = 1):
    """log n poops"""
    id = ctx.user.id
    if not user_exists(id):
        await ctx.response.send_message("Please register first using /register")
    else:
        user = load_user(id)
        msg = user.log_poop(n)
        user.save()
        await ctx.response.send_message(msg)


@tree.command(
    name="check_log",
    description="look at how many times you pooped on a date (YYYY-MM-DD), 'total' or 'today'",
    guild=discord.Object(SERVER_ID)
)
async def check_log(ctx, date: str = 'today'):
    """log n poops"""
    id = ctx.user.id
    if not user_exists(id):
        await ctx.response.send_message("Please register first using /register")
    else:
        user = load_user(id)
        count = user.get_poop_count(date)

        if not validate_date(date):
            await ctx.response.send_message('Please enter a valid date stinky poo :rage:')
        else:
            if date == 'total':
                msg = f'You pooped {count} time(s) in total :poop:'
            elif date == 'today' or date == str(datetime.today().date()).replace('/', '-'):
                msg = f'You pooped {count} time(s) today :poop:'
            else:
                msg = f'You pooped {count} time(s) on {date} :poop:'
            await ctx.response.send_message(msg)


@tree.command(
    name="leaderboard",
    description="look at a leaderboard on a date (YYYY-MM-DD), 'total' or 'today'",
    guild=discord.Object(SERVER_ID)
)
async def leaderboard(ctx, date: str = 'today'):
    """look at leaderboard on date"""

    if not validate_date(date):
        await ctx.response.send_message('Please enter a valid date stinky poo :rage:')
    else:
        leaderboard = load_leaderboard()
        if date == 'total':
            msg = leaderboard.get_total_leaderboard()
        elif date == 'today' or date == str(datetime.today().date()).replace('/', '-'):
            msg = leaderboard.get_today_leaderboard()
        else:
            msg = leaderboard.get_date_leaderboard(date)
        await ctx.response.send_message(msg)


client.run(TOKEN)
