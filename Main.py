# Importing Libraries required for the bot to function
import discord
import os
import sqlite3
import asyncio
from dotenv import load_dotenv
from discord.ext import commands, tasks
from pretty_help import PrettyHelp
from itertools import cycle
from datetime import datetime
from discord_slash import SlashCommand
import random

# Getting Token from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Adding Intents
intents = discord.Intents.default()
intents.members = True
intents.guilds = True

# Setting Prefix
client = commands.Bot(command_prefix=[
                      '_'], case_insensitive=True, strip_after_prefix=True, intents=intents)

slash = SlashCommand(client, sync_commands=True)

# Startup routine
client.remove_command('help')

@client.event
async def on_ready():
    print('Bot is ready.')
    print(f'Logged in as: {client.user.name} ID: {client.user.id}')
    print(f'Online in Guilds:')
    for server in client.guilds:
        print(f'Guild name: {server.name}')
        print(f'Guild ID: {server.id}')
    await client.change_presence(activity=discord.Game(name=f"Risk hai to ishq hai | {client.command_prefix[0]}help"))

@client.command(name='help')
async def help(ctx):
    HelpEmbed = discord.Embed(title="Help", colour=random.randint(0, 0xffffff))
    HelpEmbed.add_field(name="Search", value=f"`{client.command_prefix[0]}search <bse-listed-company>` to search companies.\nAliases: `find` `look` `s`", inline=False)
    HelpEmbed.add_field(name="Quote", value=f"`{client.command_prefix[0]}quote <script-code>` to get quotation of particular stock.\nAliases: `estimate` `q`", inline=False)
    HelpEmbed.add_field(name="Top Gainers", value=f"`{client.command_prefix[0]}top_gainers` to get top performers of BSE.\nAliases: `gainers` `topg` `tg`", inline=False)
    HelpEmbed.add_field(name="Top Losers", value=f"`{client.command_prefix[0]}top_losers` to get worst performers of BSE.\nAliases: `losers` `topl` `tl`", inline=False)
    HelpEmbed.add_field(name="News", value=f"`{client.command_prefix[0]}news <script-code>` to get latest new to particular stock.\nAliases: `n`", inline=False)
    HelpEmbed.add_field(name="Company Profile", value=f"`{client.command_prefix[0]}info <script-code>` to get detailed information about the company.\nAliases: `comp_profile` `cprofile` `company_profile`", inline=False)
    HelpEmbed.add_field(name="Analysis", value=f"`{client.command_prefix[0]}study <script-code>` to get detailed analysis of the company or stock.\nAliases: `analysis` `review` `research`", inline=False)
    HelpEmbed.set_footer(text = "Bot might respond slow because of huge data size.\nComming Soon: Financial statements for cashflow, balancesheets, Year-on-Year reports, quarter repots, histrorical statements, statements analysis")
    await ctx.send(embed=HelpEmbed)

if __name__ == '__main__':
    extensions = {'Stock'}
    for extension in extensions:
        try:
            client.load_extension(extension)
            print(f'Loaded Cog {extension} successfully')
        except Exception as error:
            print(f'Failed to load Cog {extension}. Reason: {error}')

# The following commands will be used to load Cogs
# They are locked behind a has_role check which requires the user to have the "SleepBot Admin" role
# This can be changed to allow people having Administrator permissions by changing the check to
# @commands.has_permissions(administrator=True)

@client.command(name='load')
@commands.has_role("BSE Manager")
async def load(ctx, *, extension):
    if extension == '':
        await ctx.send("Please enter a valid cog.")
    try:
        client.load_extension(extension)
        await ctx.send(f'Loaded {extension}!')
    except Exception as error:
        await ctx.send(f'Failed to load Cog {extension}. Reason: {error}')

@client.command(name='unload')
@commands.has_role("BSE Manager")
async def unload(ctx, *, extension):
    if extension == '':
        await ctx.send("Please enter a valid cog.")
    try:
        client.unload_extension(extension)
        await ctx.send(f'Unloaded {extension}!')
    except Exception as error:
        await ctx.send(f'Failed to unload Cog {extension}. Reason: {error}')

@client.command(name='reload')
@commands.has_role("BSE Manager")
async def reload(ctx, extension):
    if extension == '':
        await ctx.send("Please enter a valid cog.")
    try:
        client.unload_extension(extension)
        client.load_extension(extension)
        await ctx.send(f'Reloaded {extension}!')
    except Exception as error:
        await ctx.send(f'Failed to reload Cog {extension}. Reason: {error}')

# Command to shut the bot down
# Again requires user to have "SleepBot Admin" role which can also be changed

@client.command(name='logout')
@commands.has_role("BSE Manager")
async def logout(ctx):
    await ctx.send("Logged Out")
    await client.logout()

@logout.error
async def logout_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send(f'You do not have permission to run this command!')

@client.event
async def on_command_error(ctx, error):
    ErrorEmbed = discord.Embed(
        title="Something Went Wrong", colour=discord.Colour.red())
    ErrorEmbed.add_field(
        name="Reason :", value="{}".format(error), inline=False)
    ErrorEmbed.add_field(name="What to do now?",
                         value="Try running the command again or report this to <@!674861679074344962>.", inline=False)
    await ctx.send(embed=ErrorEmbed, delete_after=10)

client.run(TOKEN)