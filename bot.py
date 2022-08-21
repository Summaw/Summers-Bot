import json
from urllib import request
import discord
from discord.ext import commands

import requests
import asyncio
import io
import os
import sys
import ast
import contextlib
import textwrap
from traceback import format_exception


from pathlib import Path
from aioconsole import aexec

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
settings = json.load(open("settings.json", encoding="utf-8"))
logs_channel = settings["logs_channel"]



snipe_message_author = {}
snipe_message_content = {}

count1=0
count2=0



def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content

@bot.event
async def on_message_delete(message):
     snipe_message_author[message.channel.id] = message.author
     snipe_message_content[message.channel.id] = message.content

@bot.command()
async def snipe(ctx):
    channel = ctx.channel
    try:
        embed = discord.Embed(description = f"> `{snipe_message_content[channel.id]}`\n> Message sent by **{snipe_message_author[channel.id]}**!", color = 0x00c230)
        embed.set_author(name = f"Last deleted message in #{channel.name}")
        embed.set_footer(text = f"Snipe requested by `{ctx.message.author}`")
        await ctx.send(embed = embed)
    except:
     embed1 = discord.Embed(colour = 0x00c230)
     embed1.set_author(name=f"There are no deleted messages in #{ctx.channel}!")
     embed1.set_footer(text=f"Snipe requested by {ctx.message.author}")
     await ctx.channel.send(embed=embed1)



@bot.command()
async def helpem(ctx):
    await ctx.message.delete()
    embed=discord.Embed(color=0x39fd3f)
    embed.set_author(name=ctx.author.display_name, url="https://github.com/UmRange")
    embed.set_thumbnail(url="https://cdna.artstation.com/p/assets/images/images/044/000/530/medium/herin-philippe-charliepp.jpg?1638839611")
    embed.add_field(name="!help", value="```Displays this command.```", inline=False)
    embed.add_field(name="!say", value="```Displays your text in an embed.```", inline=False)
    embed.add_field(name="!calculate", value="```!calculator <operation> <equation> returns the solved equation```", inline=False)
    embed.add_field(name="!userinfo", value="```!userinfo <@user> returns user information```",inline=False)
    embed.add_field(name="!btc", value="```!btc returns the live price of BTC in USD```",inline=False)
    embed.add_field(name="!snipe", value="```!snipe returns the last deleted message```",inline=False)
    embed.add_field(name="!request", value="```!request <url> returns the response status of the page```",inline=False)
    embed.add_field(name="!stats", value="```!stats returns member stats of the guild!```",inline=False)
    embed.add_field(name="!eval", value="```!eval <python code> will run your code for you and show you the output!```",inline=False)
    embed.add_field(name="!nuke[admin]", value="```Nukes the channel command was ran in.```", inline=False)
    embed.add_field(name="!kick[admin]", value="```!kick <user> <reason> will kick the user out of the server.```", inline=False)
    embed.add_field(name="!ban[admin]", value="```!ban <user> <reason> will ban the user from the server.```", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def say(ctx, *, text):
    message = ctx.message
    await message.delete()
    embed=discord.Embed(color=0x39fd3f)
    embed.add_field(name="‎", value=text, inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=embed)

@bot.command()
async def nuke(ctx, channel: discord.TextChannel = None):
    if channel == None:
        embed=discord.Embed(color=0xFFFF00)
        embed.add_field(name="Error!", value="Please mention the channel you would like to nuke.", inline=False)
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)
        return

    nuke_channel = discord.utils.get(ctx.guild.channels, name=channel.name)

    if nuke_channel is not None:
        new_channel = await nuke_channel.clone(reason="Has been Nuked!")
        await nuke_channel.delete()
        embed=discord.Embed(color=0x39fd3f)
        embed.set_author(name=ctx.author.display_name, url="https://github.com/UmRange")
        embed.add_field(name="Nuke Command Was Ran", value="Incominggg!!!!", inline=False)
        embed.set_image(url="https://c.tenor.com/24gGug50GqQAAAAC/nuke-nuclear.gif")
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await new_channel.send(embed=embed)

@bot.command()
async def kick(ctx, member: discord.Member, *, reason):
    await member.kick(reason=reason)
    embed=discord.Embed(color=0xff0000)
    embed.set_author(name=ctx.author.display_name, url="https://github.com/UmRange")
    embed.add_field(name="Kicked Successfully", value=f"{member} was kick for {reason}\nBy: {ctx.author.mention}", inline=False)
    embed.set_image(url="http://cdn2.sbnation.com/imported_assets/1770729/ZDW0KVk.gif")
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=embed)

@bot.command()
async def ban(ctx, user: discord.Member, *, reason):
        await user.ban(reason=reason)
        ban = discord.Embed(title=f":boom: Banned {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await ctx.channel.send(embed=ban)
        await user.send(embed=ban)

@bot.command()
async def calculate(ctx, operation, *nums):
    if operation not in ['+', '-', '*', '/']:
        embed=discord.Embed(color=0xFFFF00)
        embed.add_field(name="Error!", value="> Please type a valid operation type.\n\n> **Example**: !calculate <operation ex: +, -, /, *> <10+10>", inline=False)
        await ctx.send(embed=embed)
    var = f' {operation} '.join(nums)
    #await ctx.send(f'{var} = {eval(var)}')
    embed=discord.Embed(color=0xff0000)
    embed.set_author(name=ctx.author.display_name, url="https://github.com/UmRange")
    embed.add_field(name="Equation Solved", value=f"> {var} = {eval(var)}", inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=embed)

@bot.command()
async def btc(ctx):
    x = requests.get('https://min-api.cryptocompare.com/data/pricemulti?fsyms=BTC&tsyms=USD')
    live_price = x.text
    embed=discord.Embed(color=0xf2a900)
    embed.set_author(name=ctx.author.display_name, url="https://github.com/UmRange")
    embed.set_thumbnail(url="https://whales.io/analytics/logo.gif")
    embed.add_field(name="Btc Live Price", value=f"> {live_price}", inline=False)
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=embed)
    #print(live_price)

@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    if not member:  
        member = ctx.message.author  
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at, title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar.url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)

    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
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
    embed.add_field(name="Online", value=f'{len(online_members)} :green_circle:', inline=True)
    embed.add_field(name="DND", value =f'{len(offline_members)} :red_circle:', inline =True)
    embed.set_footer(text=f"Requested by {ctx.message.author}")
    await ctx.send(embed=embed)


@bot.command()
async def eval(ctx, *, args):
        old_stdout = sys.stdout 
        new_stdout = io.StringIO() 
        sys.stdout = new_stdout 
        mycode = args
        exec(mycode)
        result = sys.stdout.getvalue().strip()
        sys.stdout = old_stdout
        embed = discord.Embed(title=f'Eval Command', color=0x39fd3f)
        embed.add_field(name="Eval Command", value=f'```py\n\nYour Code:\n{mycode} \n\nOutput:\n{str(result)} ```')
        embed.set_footer(text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)




bot.run(settings['token'])
