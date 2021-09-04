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
    await bot.change_presence(activity=discord.Game(name="Server 4 Connected"))
    
    boolean_active_run = False
    
    while True:
        
        #get auto refresh status from db
        cursor.execute("SELECT value_key FROM config WHERE value = ?",("interval",))
        interval_to_check = cursor.fetchone()
        
        cursor.execute("SELECT value_key FROM config WHERE value = ?",("active",))
        active_check = cursor.fetchone()

        if active_check[0] == "True":
            boolean_active_run = True
        else:
            boolean_active_run = False
        
        time.sleep(int(interval_to_check[0]))
        
        if boolean_active_run == True:
            
            cursor.execute("SELECT pair FROM pricenotifications")
            pairs = cursor.fetchall()
            
            cursor.execute("SELECT action,price,creator_id,creationtime FROM pricenotifications")
            data = cursor.fetchall()
            
            print(data)
            
            try:
                now = datetime.now()

                current_time = now.strftime("%H:%M:%S")
                
                response = requests.get("https://api.binance.com/api/v3/ticker/price", headers={"User-Agent": "Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)"})
                json_data = json.loads(response.text)
                
                for x in range(len(pairs)):
                
                    try:
                        # get the price of the pair being checked
                        currency_split = str(json_data).split(pairs[x][0])
                        currency_price_split = currency_split[1].split(",")
                        int_spit_one = currency_price_split[1].split("'")
                        price = int_spit_one[3]
                    except:
                        Send = await channel.send("I have been given a non-existant pair, i am deleting it from my database\nData:\n**Action** = " + data[x][0] + "\n**price** = " + data[x][1]+  "\n**creator_id** = <@!" + data[x][2] + ">\n**creationtime** = " + data[x][3])
                        #delete alert
                        cursor.execute("DELETE FROM pricenotifications WHERE creationtime=?",(str(data[x][3]),))
                        db.commit()
                    
                    #find what comparison is happening
                    if data[x][0] == "UPTO":
                        if float(price) >= float(data[x][1]):
                        
                            # setting notification channel 
                            channel = bot.get_channel(883456575388389486) # the message's channel
                            
                            #building the embed
                            style = discord.Embed(name="price Notification", title=pairs[x][0], description="Is above the notification price of " + data[x][1], timestamp=datetime.utcnow(), color=0x00FF00)
                            style.add_field(name="Current Price:", value=price, inline=True)
                            style.add_field(name="Alert Price:", value=data[x][1], inline=True)
                            Send = await channel.send("<@!" + str(data[x][2]) +">",embed=style)
                            
                            #delete alert
                            cursor.execute("DELETE FROM pricenotifications WHERE creationtime=?",(str(data[x][3]),))
                            db.commit()
                    
                    elif data[x][0] == "DOWNTO":
                        if float(price) <= float(data[x][1]):
                        
                            # setting notification channel 
                            channel = bot.get_channel(883456575388389486) # the message's channel
                            
                            #building the embed
                            style = discord.Embed(name="price Notification", title=pairs[x][0], description="Is below the notification price of " + data[x][1], timestamp=datetime.utcnow(), color=0xFF0000)
                            style.add_field(name="Current Price:", value=price, inline=True)
                            style.add_field(name="Alert Price:", value=data[x][1], inline=True)
                            Send = await channel.send("<@!" + str(data[x][2]) +">",embed=style)
                            
                            #delete alert
                            cursor.execute("DELETE FROM pricenotifications WHERE creationtime=?",(str(data[x][3]),))
                            db.commit()
                    
                    print(pairs[x][0] + " " + price)
            except:
                traceback.print_exc()
        
    
bot.run(bot_token)
    
