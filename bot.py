#General imports
import discord
from discord.ext import commands
import asyncio
import json
import datetime
import threading
import os

#Import Modules
import cogs.general
import cogs.fun
import cogs.mod
import cogs.catfacts
import cogs.testing

dcnbotVersion = "0.1.2"

if not os.path.isfile('data/warns/warns.dat'):
    with open('data/warns/warns.dat', 'w') as f:
        data = {}
        json.dump(data, f)

async def decayWarn():
    dataFile = 'data/warns/warns.dat'
    data = {}

    with open(dataFile, 'r', encoding='utf8') as f:
        data = json.load(f)
        print(data)
        print('closed')

    for key, value in data.items():
        print (key, value)
        if(int(value) < 1000):
            temp = int(value) - 10
            if(int(temp) <= 0):
                print("They're already at the lowest")
                data[key] = 0
            else:
                data[key] = int(value) - 10
                if(int(data[key]) < 0):
                    data[key] = 0
                print("decay 10 points from {0}".format(key))

    with open(dataFile, 'w', encoding='utf8') as f:
        print("saving new data")
        json.dump(data, f)

    # 86400 = day
    # threading.Timer(60, decayWarn).start()
    thr.start()
    #Endif

thr = threading.Timer(86400, decayWarn)

#Load the config file and assign it to a variable.
with open('./config.json', 'r') as c_json:
    config = json.load(c_json)

description = '''dcnbotPy is written in Python. Version {}'''.format(dcnbotVersion)

#Assign the prefix.
prefix = config["prefix_settings"]["prefix"]

#Check if prefix includes a spacer (example : dcn <command> instead of dcn<command>)
if config["prefix_settings"]["use_space"] == True:
    prefix = prefix + ' '

#Create bot
bot = commands.Bot(command_prefix=prefix, description=description)

#Create variable for time of startup.
tu = datetime.datetime.now()


@bot.event
async def on_ready():
    print('Logged in as ')
    print(bot.user.name)
    print(bot.user.id)
    print('Bot prefix is set to ' + prefix)
    print('-------------')
    # await bot.change_presence(game=discord.Game(name='with systemd'))
    if config["default_presence"] == "":
        game = 'with systemd'
    else:
        game = config["default_presence"]

    await bot.change_presence(game=discord.Game(name=game, type=0))
    await decayWarn()

@bot.event
async def on_member_ban(self, member):
    log_chan = config['log_channel']
    chan_id = 0

    for i in channels:
        if log_chan in i.name:
            chan_id = i
            print('Channel Name is ' + chan_id.name)

    isNotBot = false

    def check(msg):
        if (msg.author == self.bot.user):
            isNotBot = false
        else:
            isNotBot = true
        return isNotBot

    initialMessage = await bot.send_message(log_chan, 'User **{0} : {1}** was banned for reason :\n***{2}***\nIf you were the moderator who banned this user, please reply in this channel with a reason for the ban.'.format(member.name, member.id, "unknown"))
    reason = await bot.wait_for_message(channel=log_chan, check=check)

    if(isNotBot == true):
        return await bot.edit_message(initialMessage, 'User **{0} : {1}** was banned for reason :\n***{2}***\n\nBanned by : **{3}**'.format(member.name, member.id, reason, moderator.name))

@bot.command()
async def uptime():
    """Check bot uptime."""
    global tu
    await bot.say(timedelta_str(datetime.datetime.now() - tu))

#Convert uptime to a string.
def timedelta_str(dt):
    days = dt.days
    hours, r = divmod(dt.seconds, 3600)
    minutes, sec = divmod(r, 60)

    if minutes == 1 and sec == 1:
        return '{0} days, {1} hours, {2} minute and {3} second.'.format(days,hours,minutes,sec)
    elif minutes > 1 and sec == 1:
        return '{0} days, {1} hours, {2} minutes and {3} second.'.format(days,hours,minutes,sec)
    elif minutes == 1 and sec > 1:
        return '{0} days, {1} hours, {2} minute and {3} seconds.'.format(days,hours,minutes,sec)
    else:
        return '{0} days, {1} hours, {2} minutes and {3} seconds.'.format(days,hours,minutes,sec)

def ready(bot, config):
    if config['modules']['general'] == True:
        bot.add_cog(cogs.general.General(bot, config))
    if config['modules']['fun'] == True:
        bot.add_cog(cogs.fun.Fun(bot, config))
    if config['modules']['mod'] == True:
        bot.add_cog(cogs.mod.Mod(bot, config, thr))
    if config['modules']['catfacts'] == True:
        bot.add_cog(cogs.catfacts.Catfacts(bot, config))
    if config['modules']['testing'] == True:
        bot.add_cog(cogs.testing.Testing(bot, config))


ready(bot, config)

bot.run(config['token'])
