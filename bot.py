import ast
import asyncio
import contextlib
import datetime
import io
import json
import os
import sys
import textwrap
import time
import pyfiglet
from pathlib import Path
import traceback
from urllib import request
from PIL import Image, ImageFont, ImageDraw
from easy_pil import Editor, load_image_async, Font
from bs4 import BeautifulSoup
import random
import youtube_dl


import requests
from aioconsole import aexec

import discord
from discord import Embed, File
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord.utils import get
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')
settings = json.load(open("settings.json", encoding="utf-8"))
logs_channel = settings["logs_channel"]


snipe_message_author = {}
snipe_message_content = {}

count1 = 0
count2 = 0

servers = []
totalInvites = 0


def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content


@bot.event
async def on_message_join(member):
    channel = bot.get_channel("your welcome channel")
    embed = discord.Embed(
        title=f"Welcome {member.name}", description=f"Thanks for joining {member.guild.name}!")
    embed.set_thumbnail(url=member.avatar_url)

    await channel.send(embed=embed)


@bot.event
async def on_message_delete(message):
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        em = discord.Embed(
            title=f"Error!!!", description=f"Command not found.\nRun `!help` for more information on the commands", color=ctx.author.color)
        await ctx.send(embed=em)


@bot.command()
async def snipe(ctx):
    channel = ctx.channel
    try:
        embed = discord.Embed(
            description=f"> `{snipe_message_content[channel.id]}`\n> Message sent by **{snipe_message_author[channel.id]}**!", color=0x00c230)
        embed.set_author(name=f"Last deleted message in #{channel.name}")
        embed.set_footer(text=f"Snipe requested by `{ctx.message.author}`")
        await ctx.send(embed=embed)
    except:
        embed1 = discord.Embed(colour=0x00c230)
        embed1.set_author(
            name=f"There are no deleted messages in #{ctx.channel}!")
        embed1.set_footer(text=f"Snipe requested by {ctx.message.author}")
        await ctx.channel.send(embed=embed1)


@bot.command()
async def help(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=0x39fd3f)
    embed.set_author(name=ctx.author.display_name,
                     url="https://github.com/UmRange")
    embed.set_thumbnail(
        url="https://cdna.artstation.com/p/assets/images/images/044/000/530/medium/herin-philippe-charliepp.jpg?1638839611")
    embed.add_field(name="!comhelp",
                    value="> Displays community commands", inline=False)
    embed.add_field(name="!adminhelp",
                    value="> Displays the admin commands", inline=False)
    embed.add_field(name="!musichelp",
                    value="> Displays music commands", inline=False)
    embed.add_field(name="!codehelp",
                    value="> Displays code commands", inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=embed)


@bot.command()
async def codehelp(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=0x39fd3f)
    embed.set_author(name=ctx.author.display_name,
                     url="https://github.com/UmRange")
    embed.set_thumbnail(
        url="https://cdna.artstation.com/p/assets/images/images/044/000/530/medium/herin-philippe-charliepp.jpg?1638839611")
    embed.add_field(
        name="!eval", value="> !eval `<python code>` will run your code for you and show you the output!", inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=embed)


@bot.command()
async def adminhelp(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=0x39fd3f)
    embed.set_author(name=ctx.author.display_name,
                     url="https://github.com/UmRange")
    embed.set_thumbnail(
        url="https://cdna.artstation.com/p/assets/images/images/044/000/530/medium/herin-philippe-charliepp.jpg?1638839611")
    embed.add_field(
        name="!nuke[admin]", value="> !nuke `<channel>` Nukes the channel command was ran in.", inline=False)
    embed.add_field(
        name="!kick[admin]", value="> !kick `<user>` `<reason>` will kick the user out of the server.", inline=False)
    embed.add_field(
        name="!ban[admin]", value="> !ban `<user>` `<reason>` will ban the user from the server.", inline=False)
    embed.add_field(
        name="!banhistory[admin]", value="> !banhistory will show all prevous bans", inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=embed)


@bot.command()
async def comhelp(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=0x39fd3f)
    embed.set_author(name=ctx.author.display_name,
                     url="https://github.com/UmRange")
    embed.set_thumbnail(
        url="https://cdna.artstation.com/p/assets/images/images/044/000/530/medium/herin-philippe-charliepp.jpg?1638839611")
    embed.add_field(
        name="!say", value="> !say Displays your text in an embed.", inline=False)
    embed.add_field(name="!calculate",
                    value="> !calculator `<operation>` `<equation>` returns the solved equation", inline=False)
    embed.add_field(
        name="!userinfo", value="> !userinfo `<@user>` returns user information", inline=False)
    embed.add_field(
        name="!btc", value="> !btc returns the live price of BTC in USD", inline=False)
    embed.add_field(
        name="!snipe", value="> !snipe returns the last deleted message", inline=False)
    embed.add_field(
        name="!ascii", value="> !ascii `<text>` returns your text in ascii art", inline=False)
    embed.add_field(
        name="!stats", value="> !stats returns member stats of the guild!", inline=False)
    embed.add_field(
        name="!cat", value="> !cat returns a picture of a cat", inline=False)
    embed.add_field(
        name="!dog", value="> !dog returns a picture of a dog", inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=embed)


@bot.command()
async def musichelp(ctx):
    await ctx.message.delete()
    embed = discord.Embed(color=0x39fd3f)
    embed.set_author(name=ctx.author.display_name,
                     url="https://github.com/UmRange")
    embed.set_thumbnail(
        url="https://cdna.artstation.com/p/assets/images/images/044/000/530/medium/herin-philippe-charliepp.jpg?1638839611")
    embed.add_field(
        name="!join", value="> !join will have the bot join your voice channel you are in", inline=False)
    embed.add_field(
        name="!play", value="> !play `<youtube song url>`", inline=False)
    embed.add_field(
        name="!pause", value="> !pause will pause the current song playing", inline=False)
    embed.add_field(
        name="!leave", value="> !leave will have me leave the current voice channel!", inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=embed)


@bot.command()
async def say(ctx, *, text):
    message = ctx.message
    await message.delete()
    embed = discord.Embed(color=0x39fd3f)
    embed.add_field(name="‎", value=text, inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=embed)


@bot.command()
async def ascii(ctx, args):
    result = pyfiglet.figlet_format(args, font="bubble")
    embed = discord.Embed(color=0x39fd3f)
    embed.add_field(name="‎", value=f'{result}', inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=embed)


@bot.command()
async def nuke(ctx, channel: discord.TextChannel = None):
    if channel == None:
        embed = discord.Embed(color=0xFFFF00)
        embed.add_field(
            name="Error!", value="Please mention the channel you would like to nuke.", inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)
        return

    nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

    if nuke_channel is not None:
        new_channel = await nuke_channel.clone(reason="Has been Nuked!")
        await nuke_channel.delete()
        embed = discord.Embed(color=0x39fd3f)
        embed.set_author(name=ctx.author.display_name,
                         url="https://github.com/UmRange")
        embed.add_field(name="Nuke Command Was Ran",
                        value="Incominggg!!!!", inline=False)
        embed.set_image(
            url="https://c.tenor.com/24gGug50GqQAAAAC/nuke-nuclear.gif")
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await new_channel.send(embed=embed)


@bot.command()
async def kick(ctx, member: discord.Member, *, reason):
    if member == None:
        embed = discord.Embed(color=0xFFFF00)
        embed.add_field(
            name="Error!", value="Please mention the user you would like to kick!", inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)
    else:
        await member.kick(reason=reason)
        embed = discord.Embed(color=0xff0000)
        embed.set_author(name=ctx.author.display_name,
                         url="https://github.com/UmRange")
        embed.add_field(name="Kicked Successfully",
                        value=f"{member} was kick for {reason}\nBy: {ctx.author.mention}", inline=False)
        embed.set_image(
            url="http://cdn2.sbnation.com/imported_assets/1770729/ZDW0KVk.gif")
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)


@bot.command()
async def ban(ctx, user: discord.Member, *, reason):
    if user == None:
        embed = discord.Embed(color=0xFFFF00)
        embed.add_field(
            name="Error!", value="Please mention the user you would like to ban!", inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)
    else:
        await user.ban(reason=reason)
        ban = discord.Embed(color=0xff0000,
                            title=f":boom: Banned {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await ctx.channel.send(embed=ban)
        await user.send(embed=ban)


@bot.command()
async def calculate(ctx, operation, *nums):
    if operation not in ['+', '-', '*', '/']:
        embed = discord.Embed(color=0xFFFF00)
        embed.add_field(
            name="Error!", value="> Please type a valid operation type.\n\n> **Example**: !calculate <operation ex: +, -, /, *> <10+10>", inline=False)
        await ctx.send(embed=embed)
    var = f' {operation} '.join(nums)
    embed = discord.Embed(color=0xff0000)
    embed.set_author(name=ctx.author.display_name,
                     url="https://github.com/UmRange")
    embed.add_field(name="Equation Solved",
                    value=f"> {var} = {eval(var)}", inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=embed)


@bot.command()
async def invites(ctx, usr: discord.Member = None):
    if usr == None:
        user = ctx.author
    else:
        user = usr
    total_invites = 0
    for i in await ctx.guild.invites():
        if i.inviter == user:
            total_invites += i.uses
    await ctx.send(f"{user.name} has invited {totalInvites} member{'' if totalInvites == 1 else 's'}!")


@bot.command()
async def btc(ctx):
    x = requests.get(
        'https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC&tsyms=USD')
    live_price = x.text
    embed = discord.Embed(color=0xf2a900)
    embed.set_author(name=ctx.author.display_name,
                     url="https://github.com/UmRange")
    embed.set_thumbnail(url="https://whales.io/analytics/logo.gif")
    embed.add_field(name="Btc Live Price",
                    value=f"> {live_price}", inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=embed)


@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    if not member:
        member = ctx.message.author
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=discord.Colour.purple(
    ), timestamp=ctx.message.created_at, title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar.url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)

    embed.add_field(name="Created Account On:", value=member.created_at.strftime(
        "%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime(
        "%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Roles:", value="".join(
        [role.mention for role in roles]))
    embed.add_field(name="Highest Role:", value=member.top_role.mention)
    print(member.top_role.mention)
    await ctx.send(embed=embed)


@bot.command()
async def stats(ctx):
    online_members = []
    offline_members = []
    for member in ctx.guild.members:
        if member.status is not discord.Status.offline:
            online_members.append(member.name)
        else:
            offline_members.append(member.name)

    embed = discord.Embed(title=f'"{ctx.guild.name}" Stats', color=0x39fd3f)
    embed.add_field(name="Member Count", value=ctx.guild.member_count)
    embed.add_field(
        name="Online", value=f'{len(online_members)} :green_circle:', inline=True)
    embed.add_field(
        name="DND", value=f'{len(offline_members)} :red_circle:', inline=True)
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=embed)


@bot.command()
async def eval(ctx, *, args):
    if args == None:
        embed = discord.Embed(color=0xFFFF00)
        embed.add_field(
            name="Could not execute!", value="Please enter your script you would like to test", inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)
    else:
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        mycode = args
    try:
        exec(mycode)
        result = sys.stdout.getvalue().strip()
        sys.stdout = old_stdout
        embed = discord.Embed(title=f'Eval Command', color=0x39fd3f)
        embed.add_field(name="Eval Command",
                        value=f'```py\n\nYour Code:\n{mycode} \n\nOutput:\n{str(result)} ```')
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)
    except Exception as err:
        print(err, traceback.format_exc())
        embed = discord.Embed(color=0xFFFF00)
        embed.add_field(
            name="Build Failed!", value=f'```py\n\nYour Code:\n{mycode} \n\nOutput:\n{err} ```', inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)


@bot.command()
async def cat(ctx):
    req = requests.get('https://api.thecatapi.com/v1/images/search')
    if req.status_code != 200:
        await ctx.send("API error, could not get a meow")
        print("Could not get a cat")
    catlink = json.loads(req.text)[0]
    rngcat = catlink["url"]
    em = discord.Embed()
    em.set_image(url=rngcat)
    em.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=em)


@bot.command()
async def dog(ctx):
    req = requests.get('http://random.dog/')
    if req.status_code != 200:
        await ctx.send("API error, could not get a woof")
        print("Could not get a dog")
    doglink = BeautifulSoup(req.text, 'html.parser')
    rngdog = 'http://random.dog/' + doglink.img['src']
    em = discord.Embed()
    em.set_image(url=rngdog)
    em.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=em)


youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename


@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        embed = discord.Embed(color=0xFFFF00)
        embed.add_field(
            name="Error!", value="{} is not connected to a voice channel".format(ctx.message.author.name), inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()


@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        embed = discord.Embed(color=0x39fd3f)
        embed.add_field(
            name="Now Playing!", value="> **I have successfully left the channel!**", inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)
        await voice_client.disconnect()
    else:
        embed = discord.Embed(color=0xFFFF00)
        embed.add_field(
            name="Error!", value="The bot is not connected to a voice channel.".format(ctx.message.author.name), inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)


@bot.command(name='play_song', help='To play song')
async def play(ctx, url):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(
                executable="ffmpeg.exe", source=filename))
        embed = discord.Embed(color=0x39fd3f)
        embed.add_field(
            name="Now Playing!", value="**Now playing:** {}".format(filename), inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)
        # await ctx.send('**Now playing:** {}'.format(filename))
    except:
        embed = discord.Embed(color=0xFFFF00)
        embed.add_field(
            name="Error!", value="The bot is not connected to a voice channel.".format(ctx.message.author.name), inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        embed = discord.Embed(color=0xFFFF00)
        embed.add_field(
            name="Error!", value="The bot is not playing anything at the moment.".format(ctx.message.author.name), inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)


@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        embed = discord.Embed(color=0xFFFF00)
        embed.add_field(
            name="Error!", value="The bot was not playing anything before this. Use play_song command", inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)


@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        embed = discord.Embed(color=0xFFFF00)
        embed.add_field(
            name="Error!", value="The bot is not playing anything at the moment.".format(ctx.message.author.name), inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)

bot.run(settings['token'])
