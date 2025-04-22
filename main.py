
import discord
from discord import app_commands

from creds import TOKEN, SERVER_ID

from load import load_user, check_user_exists
from user import User

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
    already_registered = check_user_exists(id)

    if not already_registered:
        user = User(id, name)
        user.save()
        await interaction.response.send_message(f'Registering new user \n Welcome {name} :tada:')
    else:
        await interaction.response.send_message("You're already registered :rage:")


client.run(TOKEN)
