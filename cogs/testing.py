import discord
from discord.ext import commands
import asyncio, aiohttp, io, os

class Testing:
    """
    Testing cog
    """

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.command(pass_context=True)
    async def testing(self, ctx):
        """Lets test and see if this works"""
        await self.bot.say("Testing 1 2 3!");
