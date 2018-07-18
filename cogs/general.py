import discord
from discord.ext import commands
import aiohttp
import json
import sys
import subprocess

class General:
    """
    General commands from dcnbotPy.
    """

    def __init__(self, bot, config):
        self.bot = bot
        self.config = config

    @commands.command(pass_context=True)
    async def listroles(self, ctx):
        """List available user assignable roles."""
        _rolesList = '\n'.join(map(str, self.config["user_roles"]))

        return await self.bot.say('```List of available roles\n' + _rolesList + '\n```')

    @commands.command(pass_context=True)
    async def joinrole(self, ctx, *, role=""):
        """Select one or more of the many user roles available."""
        _server = ctx.message.server
        _member = ctx.message.author

        _roles = self.config["user_roles"]

        _serverRoles = _server.roles
        _userRoles = _member.roles

        for idx, i in enumerate(_serverRoles):
            _role = i.name.lower()

            if role.lower() == _role:
                for idy, ii in enumerate(_roles):
                    _joinrole = ii.lower()

                    if role.lower() == _joinrole:
                        for idz, iii in enumerate(_userRoles):

                            _userrole = str(iii).lower()
                            if role.lower() == _userrole:
                                return await self.bot.say('You\'re already in that role.')
                            elif idz >= len(_userRoles)-1:
                                try:
                                    await self.bot.add_roles(_member, i)
                                    print('Added user to role')
                                    return await self.bot.say('Added ' + _member.name + ' to ' + i.name)
                                except Exception as error:
                                    return await self.bot.say('```Error : ' + str(error) + '```')
                    elif idy >= len(_roles)-1:
                        return await self.bot.say('You\'re not allowed to inherit that role.')
            elif idx >= len(_serverRoles)-1:
                return await self.bot.say('That role doesn\'t exist')

    @commands.command(pass_context=True)
    async def leaverole(self, ctx, *, role : str):
        """Remove a user role that is currently assigned to you."""
        _server = ctx.message.server
        _member = ctx.message.author
        _roles = self.config["user_roles"]
        _userRoles = _member.roles

        for idx, i in enumerate(_userRoles):
            _role = i.name.lower()

            if role.lower() == _role:
                for idy, ii in enumerate(_roles):
                    _checkroles = ii.lower()

                    if role.lower() == _checkroles.lower():

                        try:
                            await self.bot.remove_roles(_member, i)
                            print('Removed user from role.')
                            return await self.bot.say('Removed ' + _member.name + ' from ' + i.name)
                        except Exception as error:
                            return await self.bot.say('```Error : ' + str(error) + '```')
            elif idx >= len(_roles)-1:
                return await self.bot.say('You\'re not in that role.')

    @commands.command(pass_context=True)
    async def pacman(self, ctx, cmd=None, query=None):
        """Search Arch repos or AUR."""
        if cmd == '-Ss':
            if query is None:
                return await self.bot.say('Invalid amount of arguments passed.')

            await self.bot.say('Searching for {0} in Arch repositories and the AUR.'.format(query))

            pkgs = []
            pkginfos = []

            async with aiohttp.get('https://archlinux.org/packages/search/json?q={0}'.format(query)) as r:
                ar = await r.json()
                ar = ar['results']
                print('{0} packages from the Arch repo'.format(len(ar)))
                for count, res in enumerate(ar):
                    if count < 10:
                        if not res['pkgname'] in pkgs:
                            pkgs.append([res['pkgname'],res['repo'],res['arch']])
                            pkginfos.append([res['pkgname'],res['repo'],res['arch'],res['pkgver']+'-'+res['pkgrel'],res['pkgdesc'],res['url']])
                        else:
                            count -= 1

            async with aiohttp.get('https://aur.archlinux.org/rpc.php?v=5&type=search&arg={0}'.format(query)) as u:
                au = await u.json()
                au = au['results']
                print('{0} packages from the AUR'.format(len(au)))
                for count, res in enumerate(au):
                    if count < 10:
                        if not res['Name'] in pkgs:
                            pkgs.append([res['Name'],'AUR','any'])
                            pkginfos.append([res['Name'],'AUR','any',res['Version'],res['Description'],res['URL']])
                        else:
                            count -= 1

                if (len(pkgs) > 1):
                    result = '```tex\n'
                    for cnt, i in enumerate(pkgs):
                        result += 'Name: '+i[0]+' | Repo: '+i[1]+' | Arch: '+i[2]+'\n';

                    result += '\nReply with the name of one of the following package names within 20 seconds to get more information.'
                    await self.bot.say('{0}```'.format(result))

                    def reply_check(m):
                        print('Content of m: ' + m)
                        for i in pkgs:
                            if m == i[0]:
                                return True

                    userReply = await self.bot.wait_for_message(timeout=20.0, author=ctx.message.author)

                    try:
                        replyMatch = reply_check(userReply.content)
                    except Exception as error:
                        print(error)
                        print('Most likely a time-out')

                    if userReply is None:
                        await self.bot.say('Timed out')
                        return
                    elif replyMatch == True:
                        for j in pkginfos:
                            print('Ready to send info. Find data.')
                            if userReply.content in j[0]:
                                print('Found package!')
                                print(j)
                                pName = userReply.content
                                if 'AUR' in j[1]:
                                    print('IS IN AUR')
                                    pVersion = j[1]
                                    pDescription = j[2]
                                    pSourceURL = j[3]
                                    pURL = 'https://aur.archlinux.org/packages/'+pName

                                    await self.bot.say('Info on: {0}\n```tex\nPackage name: {0}\nVersion: {1}\nDescription: {2}\nSource: {3}\nAUR: {4}```'.format(pName, pVersion, pDescription, pSourceURL, pURL))
                                    return
                                else:
                                    print('IS IN ARCH REPO')
                                    pVersion = j[3]
                                    pDescription = j[4]
                                    pArch = j[2]
                                    pRepo = j[1]
                                    pSourceURL = j[5]

                                    await self.bot.say('Info on: {0}\n```tex\nPackage name: {0}\nVersion: {1}\nDescription: {2}\nArch: {3}\nRepo: {4}\nSource: {5}```'.format(pName, pVersion, pDescription, pArch, pRepo, pSourceURL))
                                    return
                    else:
                        return await self.bot.say('Previous search was exited')
                else:
                    return await self.bot.say('No results found')
        elif cmd != "-Ss" or cmd == None:
            await self.bot.say('Invalid arguments')

    @commands.command(description='Return a link to the source code.')
    async def source(self):
        """Post a link to the bot source code."""
        source = "https://github.com/doomcrewinc/dcnbot"
        await self.bot.say(source)

    @commands.command(pass_context=True, no_pm=True)
    async def warnstatus(self, ctx, user : discord.Member = None):
        """Check how many warning points you currently have."""
        if user is None:
            user = ctx.message.author

        dataFile = 'data/warns/warns.dat'
        data = {}

        with open(dataFile, 'r', encoding='utf8') as f:
            data = json.load(f)
            print(data)
            print('closed')

        if(user.id not in data or int(data["{0}".format(user.id)] == 0)):
            await self.bot.send_message(ctx.message.channel,"You currently have 0 warning points! Good job!")
        else:
            warnCount = data["{0}".format(user.id)]
            await self.bot.send_message(ctx.message.channel,"You currently have {0} warning points.".format(warnCount))
