import discord
from discord.ext import commands
import asyncio
import os
import random
# For Database related stuff
import sqlite3
from datetime import datetime
from datetime import date


loading_embed = discord.Embed(description="loading...")