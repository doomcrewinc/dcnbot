# Developed by doomcrewinc for OdinForce
import discord
from discord.ext import commands
import random
from pprint import pprint
import asyncio, json

class Catfacts:
    """
    Random cat facts.
    """

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.command(pass_context=True)
    async def catfact(self, ctx):
        """Random facts about your furry best friend and overlord!"""
        with open('catfacts.json', encoding='utf-8') as cat_file:
            catdata = json.loads(cat_file.read())
        factslist=[]
        for line in catdata["data"]:
            factslist.append(line)
        choice=random.choice(factslist)
        pprint(choice['fact'])

        return await self.bot.say("`" + choice['fact'] + "`")
