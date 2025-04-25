from datetime import datetime

import discord
from discord import app_commands

from creds import TOKEN, SERVER_ID, CHANNEL_ID, ROLE_ID, OWNER_IDS

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

    channel = client.get_channel(int(CHANNEL_ID))
    print("Bot ready")
    print("---------------------")
    await channel.send(f"<@&{ROLE_ID}> \n gub gub is alive again!!! :poop:")


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
        role = interaction.user.guild.get_role(int(ROLE_ID))
        await interaction.user.add_roles(role)
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
async def reregister(interaction):
    """reregister user into star rail sim players"""
    id = interaction.user.id
    name = interaction.user.name
    role = interaction.user.guild.get_role(int(ROLE_ID))
    await interaction.user.add_roles(role)
    user = User(id, name)
    user.save()
    await interaction.response.send_message('Resetting user data')


@tree.command(
    name="rerole",
    description="gives you the gubbers role",
    guild=discord.Object(SERVER_ID)
)
async def rerole(interaction):
    """gives the role that is affiliated with ROLE_ID"""
    role = interaction.user.guild.get_role(int(ROLE_ID))
    await interaction.user.add_roles(role)
    await interaction.response.send_message('You have been reroled!')


@tree.command(
    name="derole",
    description="takes away the gubbers role",
    guild=discord.Object(SERVER_ID)
)
async def rerole(interaction):
    """gives the role that is affiliated with ROLE_ID"""
    role = interaction.user.guild.get_role(int(ROLE_ID))
    await interaction.user.remove_roles(role)
    await interaction.response.send_message('You have been deroled!')


@tree.command(
    name="log",
    description="log your poops, default to 1",
    guild=discord.Object(SERVER_ID)
)
async def log_poops(interaction, n: int = 1):
    """log n poops"""
    id = interaction.user.id
    if not user_exists(id):
        await interaction.response.send_message("Please register first using /register")
    else:
        user = load_user(id)
        msg = user.log_poop(n)
        user.save()
        await interaction.response.send_message(msg)


@tree.command(
    name="check_log",
    description="look at how many times you pooped on a date (YYYY-MM-DD), 'total' or 'today'",
    guild=discord.Object(SERVER_ID)
)
async def check_log(interaction, date: str = 'today'):
    """log n poops"""
    id = interaction.user.id
    if not user_exists(id):
        await interaction.response.send_message("Please register first using /register")
    else:
        user = load_user(id)
        count = user.get_poop_count(date)

        if not validate_date(date):
            await interaction.response.send_message('Please enter a valid date stinky poo :rage:')
        else:
            if date == 'total':
                msg = f'You pooped {count} time(s) in total :poop:'
            elif date == 'today' or date == str(datetime.today().date()).replace('/', '-'):
                msg = f'You pooped {count} time(s) today :poop:'
            else:
                msg = f'You pooped {count} time(s) on {date} :poop:'
            await interaction.response.send_message(msg)


@tree.command(
    name="leaderboard",
    description="look at a leaderboard on a date (YYYY-MM-DD), 'total' or 'today'",
    guild=discord.Object(SERVER_ID)
)
async def leaderboard(interaction, date: str = 'today'):
    """look at leaderboard on date"""

    if not validate_date(date):
        await interaction.response.send_message('Please enter a valid date stinky poo :rage:')
    else:
        leaderboard = load_leaderboard()
        if date == 'total':
            msg = leaderboard.get_total_leaderboard()
        elif date == 'today' or date == str(datetime.today().date()).replace('/', '-'):
            msg = leaderboard.get_today_leaderboard()
        else:
            msg = leaderboard.get_date_leaderboard(date)
        await interaction.response.send_message(msg)


@client.event
async def on_message(msg):
    """send message through bot from ,dms if you have the OWNER_ID"""
    if isinstance(msg.channel, discord.DMChannel) and str(msg.author.id) in OWNER_IDS:
        channel = client.get_channel(int(CHANNEL_ID))
        if msg.content != '':
            await channel.send(msg.content)
        if msg.attachments:
            for attach in msg.attachments:
                await channel.send(attach.url)


if __name__ == '__main__':
    client.run(TOKEN)
