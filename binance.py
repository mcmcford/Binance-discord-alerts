import requests
import json
import time
import traceback
import hashlib
import sqlite3
from datetime import datetime
import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions

# Changeable Variables
your_user_id = '225321172018003968'
bot_token = ''
bots_prefix = "!"


# create database
db = sqlite3.connect('Binance.db')
cursor = db.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS pricenotifications(pair TEXT, creationtime TEXT primary key, action TEXT, price TEXT,creator_id TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS config(value TEXT primary key, value_key TEXT)')

#bots prefix 
bot = commands.Bot(command_prefix=commands.when_mentioned_or(bots_prefix))



@bot.event
async def on_ready():
    """On ready event!"""
    print("Logged in as " + str(bot.user))
    print("User ID: " + str(bot.user.id))
    
@bot.command()
async def above(ctx): 
    try:
        #delete the senders message
        await ctx.message.delete()
    except Exception:
        print("not deleting message due to it being in a DM")
    
    args = ctx.message.content.split()
    
    del args[0] #remove the actual command leaving just the arguments
    print(len(args))
    
    if len(args) != 2:
        await ctx.send("Please ensure you have formatted the command correctly eg. `!above ETHGBP 3000`")
    else:
        try:
            float(args[1])
        except:
            await ctx.send("Please ensure you have formatted the command correctly eg. `!above ETHGBP 3000`")
            return
        
        seconds = time.time()
        
        #updating the database
        cursor.execute("INSERT INTO pricenotifications VALUES(?,?,?,?,?)",(args[0],seconds,"UPTO",args[1],str((ctx.message.author).id)))
        db.commit()

@bot.command()
async def below(ctx): 
    try:
        #delete the senders message
        await ctx.message.delete()
    except Exception:
        print("not deleting message due to it being in a DM")
    
    args = ctx.message.content.split()
    
    del args[0] #remove the actual command leaving just the arguments
    print(len(args))
    
    if len(args) != 2:
        await ctx.send("Please ensure you have formatted the command correctly eg. `!below ETHGBP 3000`")
    else:
        try:
            float(args[1])
        except:
            await ctx.send("Please ensure you have formatted the command correctly eg. `!below ETHGBP 3000`")
            return
        
        seconds = time.time()
        
        #updating the database
        cursor.execute("INSERT INTO pricenotifications VALUES(?,?,?,?,?)",(args[0],seconds,"DOWNTO",args[1],str((ctx.message.author).id)))
        db.commit()

bot.run(bot_token)