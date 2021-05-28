import os
import keep_alive
import string
import replit
import psutil
import time

from asyncio.exceptions import TimeoutError as te

from asyncio import sleep

import random

keep_alive.keep_alive()

import discord
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bad_words=["\x66\x75\x63\x6b","\x73\x68\x69\x74","\x64\x69\x63\x6b","\x70\x65\x6e\x69\x73","\x62\x69\x74\x63\x68","\x73\x65\x78","\x73\x65\x78y","ssa"[::-1],"🖕","\x70\x6f\x72\x6e"]

def is_command(messagetext,command):
    return messagetext.lower() == command or messagetext.lower().startswith(command+" ")

correct =  0x00000000
wrong   =  0x00000001
timeout = -0x00000001 

class Question(object):
    def __init__(this,client:discord.Client,answer:int,question:str,channel,user:discord.User,options:list):
        this.client = client
        this.answer = answer 
        this.options = options 
        this.question = question
        this.channel = channel
        this.user = user

    async def ask(this):

        def check(ctx,user):
            print("REACT")
            return ctx.message == this.message and this.user == user;

        embed = discord.Embed(title="Question",description=this.question,color=0x00FF00)
        for i in range(1,4+1):
            embed.add_field(name=str(i),value=this.options[i-1],inline=False)
        this.message = await this.channel.send(embed=embed)
        await this.message.add_reaction("1️⃣")
        await this.message.add_reaction("2️⃣")
        await this.message.add_reaction("3️⃣")
        await this.message.add_reaction("4️⃣")

        try:
            react,user = await client.wait_for("reaction_add",check=check,timeout = 30)
            print(react.emoji[0],str(this.answer))
            if react.emoji[0] == str(this.answer):
                return correct
            else:
                return wrong
        except te:
            await this.channel.send("Timeout, you lost $1000.")
            return timeout
        


spamming=True

client = discord.Client(max_messages=None)
@client.event
async def on_message(message):
    global spamming
    # if message.author == client.user:
    #     return
    if any(ext.strip() in message.content.lower().replace(","," ").replace("."," ").replace("?"," ").split(" ") for ext in bad_words) and not message.channel.is_nsfw():
        await message.reply(f"<@{message.author.id}> Woah! Don't say that...")
        try:
            await message.delete()
        except discord.errors.Forbidden:
            pass
        return
    if message.guild == None:
        print(f"@{message.author.name}: {message.content}")
    else:
        print(f"{message.guild.name}@{message.author.name}: {message.content}")
    if is_command(message.content,"spammer: help"):
        try:
            user_text=message.content[13:].strip()
            if user_text.split(" ") == [""]:
                embedNum=0
                embeds = []
                embedVar = discord.Embed(title="Commands [1]", description="The prefix is `spammer:`", color=0x00ff00)
                embedVar.add_field(name="help", value="Gets help", inline=False)
                embedVar.add_field(name="spam", value="Spams", inline=False)
                embedVar.add_field(name="stop", value="Stops spam", inline=False)
                embeds.append(embedVar)
                embedVar = discord.Embed(title="Commands [2]",description = "The prefix is `spammer:`", color = 0x00ff00)
                embedVar.add_field(name="choose", value="Choose an option", inline=False)
                embedVar.add_field(name="die", value="Self destruct", inline=False)
                embedVar.add_field(name="delete", value="Delete this.", inline=False)
                embeds.append(embedVar)
                embedVar = discord.Embed(title="Commands [3]",description = "The prefix is `spammer:`", color = 0x00ff00)
                embedVar.add_field(name="ran", value="Random number", inline=False)
                embedVar.add_field(name="clear", value="Clear channel", inline=False)
                embedVar.add_field(name="credits", value="Credits", inline=False)
                embeds.append(embedVar)
                embedVar = discord.Embed(title="Commands [4]",description = "The prefix is `spammer:`", color = 0x00ff00)
                embedVar.add_field(name="status", value="View current stats", inline=False)
                embedVar.add_field(name="game work", value="Work", inline=False)
                embedVar.add_field(name="game bal", value="View balence", inline=False)
                embeds.append(embedVar)

                def check(ctx,user):
                    print("CHECK")
                    return str(ctx.emoji) in ['⬅️', '➡️'] and ctx.message == m and user == message.author

                m = await message.channel.send(embed=embeds[embedNum])
                await m.add_reaction("⬅️")
                await m.add_reaction("➡️")
                while True:
                    try:
                        react,user = await client.wait_for("reaction_add",check=check,timeout = 30)
                        if react.emoji == "➡️":
                            embedNum += 1
                            if embedNum>=len(embeds):
                                embedNum = 0;
                        if react.emoji == "⬅️":
                            embedNum -= 1
                            if embedNum<0:
                                embedNum = len(embeds)-1;
                        await react.remove(user)
                        await m.edit(embed = embeds[embedNum])
                    except te:
                        emb = discord.Embed(title="This message has timed out.",description="Please start a new help page.")
                        await m.edit(embed=emb)
                        break
            if user_text.lower().split(" ") == ['help']:
                await message.channel.send("You already know what this means dummy")
            if user_text.lower().split(" ") == ["spam"]:
                await message.channel.send(
"""\
Syntax: `spammer: spam <number> <text>`
Spams `<text>` `<number>` of times.
Variables:
`$count` : Count
`$CurrentMessage` : Current message that's being sent
"""
                )
            if user_text.lower().split(" ") == ["choose"]:
                await message.channel.send(
"""\
Syntax: `spammer: choose <options split by commas>`
Sends a random message in <options>.
"""
                )
            if user_text.lower().split(" ") == ['credits']:
                await message.channel.send(
"""\
Syntax: `spammer: credits`
See the credits of Spammer.
"""
                )
            if user_text.lower().split(" ") == ["stop"]:
                await message.channel.send(
"""\
Syntax: `spammer: stop`
Stops spam.
"""
                )
            if user_text.lower().split(" ") == ["status"]:
                await message.channel.send(
"""\
Syntax: `spammer: status`
View stats of Spammer right now.
"""
                )
            if user_text.lower().split(" ") == ["ran"]:
                await message.channel.send(
"""\
Syntax: `spammer: ran <start> <end>`
Random number between `<start>` and `<end>`
"""
                )
            if user_text.lower().split(" ") == ["clear"]:
                await message.channel.send(
"""\
Syntax: `spammer: clear`
Clear the channel
"""
                )
            if user_text.lower().split(" ") == ["clear"]:
                await message.channel.send(
"""\
Syntax: `spammer: die`
Self destruct
"""
                )
            if user_text.lower().split(" ") == ["clear"]:
                await message.channel.send(
"""\
Syntax: `spammer: delete`
Delete this message
"""
                )
            if user_text.lower().split(" ") == ["game","work"]:
                await message.channel.send(
"""\
Syntax: `spammer: game work`
Earn money in the game
"""
                )
            if user_text.lower().split(" ") == ["game","bal"]:
                await message.channel.send(
"""\
Syntax: `spammer: game bal`
See your amount of money in the game
"""
                )
        except:
            pass

    if is_command(message.content,"spammer: game work"):
        if str(message.author.id) in replit.db.keys():
            if float(replit.db[str(message.author.id)]['last'])+1000 > time.time():
                await message.channel.send(f"You need to wait {float(replit.db[str(message.author.id)]['last'])+1000 - time.time()} seconds before you can work again!")
                return
            stuff = replit.db[str(message.author.id)]
            stuff['last'] = str(time.time())
            replit.db[str(message.author.id)] = stuff 
            questions = [
                Question(client=client,answer=1,question="What is water?",channel=message.channel,user=message.author,options=["H2O","H20","HO","H0"]),
                Question(client=client,answer=3,question="Who made this bot?",channel=message.channel,user=message.author,options=["No one","Discord","maxj1510.exe#3326","maxj1015.xex#3226"]),
                Question(client=client,answer=1,question="Take a break.",channel=message.channel,user=message.author,options=["Yes!","NO","Why?",":("]),
                Question(client=client,answer=3,question="This is a scam. Say \"scam\" or else...",channel=message.channel,user=message.author,options=["Scam","nah","else...","I don't care"]),
                Question(client=client,answer=2,question="How many lines of code was used to make Spammer? [Right now]",channel=message.channel,user=message.author,options=["1852","About 500","195736","About 257"])
            ]
            que = await random.choice(questions).ask()
            if que == correct:
                mon = 12000
                await message.channel.send('You got '+str(mon))
            elif que == wrong:
                mon = random.randint(-7000,-1000)
                await message.channel.send('You answered wrong and lost '+str(-mon))
            elif que == timeout:
                mon=-1000 
            stuff['money']+=mon
            replit.db[str(message.author.id)] = stuff
        else:
            replit.db[str(message.author.id)] = {"money":0,"last":0}
            await message.channel.send("You joined the game! Do `spammer: game work` to earn money.")
    if is_command(message.content,"spammer: game bal"):
        if str(message.author.id) in replit.db.keys():
            await message.channel.send(f"You have ${replit.db[str(message.author.id)]['money']}")
        else:
            await message.channel.send("You have nothing.")
    if is_command(message.content,"spammer: stop"):
        try:
            await message.channel.send("Stopping.")
        except:
            pass
        spamming=False
    if is_command(message.content,"spammer: easteregg"):
        try:
            await message.channel.send("There are no easter eggs.")
        except:
            pass
    if is_command(message.content,"spammer: delete"):
        try:
            await message.delete()
        except:
            await message.channel.send("I don't have permissions.")
    if is_command(message.content,"spammer: clear"):
        try:
            await message.channel.clone()
            await message.channel.delete()
        except:
            await message.channel.send("I don't have permissions.")
    if is_command(message.content,"spammer: die"):
        await message.channel.send("Self destructing in 3..")
        await sleep(1)
        await message.channel.send("Self destructing in 2..")
        await sleep(1)
        await message.channel.send("Self destructing in 1..")
        await sleep(1)
        await message.channel.send(":boom:"*4)
        await sleep(2)
        await message.channel.send("Actually, I think I'l stick around.")
    if is_command(message.content,"spammer: credits"):
        embedVar = discord.Embed(title="Credits", description="Credits for the bot", color=0x00ff00)
        embedVar.add_field(name="Who made this?", value="maxj1510#3326", inline=False)
        embedVar.add_field(name="Invite to your server", value="[Invite to your server](https://spammerdiscordbot.maxjiang2021.repl.co)", inline=False)
        await message.channel.send(embed=embedVar)
    if is_command(message.content,"spammer: choose"):
        options = message.content[15:].split(",")
        try:
            if len(options)==1 and options!=['']:
                await message.channel.send("There's only one option :thinking:")
                return
            await message.channel.send(random.choice(options))
        except:
            await message.channel.send("Invalid command syntax. Run `spammer: help choose` for more information.")
    if is_command(message.content,'spammer: spam'):
        try:
            user_text=message.content[13:]
            items=user_text.split(" ")[1:]
            try:
                num=int(items[0].strip())
                if num>30:
                    await message.channel.send("NO. Discord will ban me!!!")
                    return
                for i in range(1,num+1):
                    if not spamming:
                        spamming=True
                        await message.channel.send("Spam interrupted.")
                        return
                    msg=" ".join(items[1:])
                    og=msg
                    msg = msg.replace("$count",str(i))
                    msg = msg.replace("$CurrentMessage",og)
                    await message.channel.send(msg)
            except:
                try:
                    await message.channel.send(
"""\
Invalid command syntax. Run `spammer: help spam` for more information.
"""
                    )
                except:
                    pass
        except:
            await message.channel.send("Sorry, something went wrong!!")
    if is_command(message.content,'spammer: ran'):
        try:
            user_text=message.content[13:]
            items=user_text.split(" ")
            try:
                start=int(items[0].strip())
                end=int(items[1].strip())
                if (start>end):
                    await message.channel.send("The start is bigger than the end??? :thinking:")
                    return
                await message.channel.send(random.randint(start,end))
            except:
                try:
                    await message.channel.send(
"""\
Invalid command syntax. Run `spammer: help ran` for more information.
"""
                    )
                except:
                    pass
        except:
            await message.channel.send("Sorry, something went wrong!!")
    if is_command(message.content,'spammer: manage'):
        user_text=message.content[15:]
        items=user_text.split(" ")[1:]
        print("Manager",items)
        if items[0]=="sendmessage":
            if items[1]==os.getenv("PASSWORD"):
                try:
                    await eventloop(message)
                except te:
                    await message.channel.send("You didn't reply...")
                except Exception:
                    await message.channel.send("Something went wrong...")
    if is_command(message.content,'spammer: status'):
        emb = discord.Embed(title="Spammer stats",description="Lines of code: about 500",color=0x00FF00)
        emb.add_field(name="CPU%",value=str(psutil.cpu_percent()))
        emb.add_field(name="MEMORY%",value=str(psutil.virtual_memory().percent))
        emb.add_field(name="#SERVERS",value=str(len(client.guilds)))
        await message.channel.send(embed=emb)
    if is_command(message.content,"spammer: nuke"):
        if message.guild == None:
            await message.channel.send("This is a dm, I cannot do that!")
            return
        try:
            if replit.db["SERVER_"+str(message.guild.id)] == "disabled":
                await message.channel.send("This is disabled.")
                return
        except KeyError:
            replit.db["SERVER_"+str(message.guild.id)] == "enabled"
        for channel in message.guild.channels:
            try:
                await channel.delete()
            except:
                pass
        await message.guild.create_text_channel("Nuked")
    if is_command(message.content,"spammer: settings"):
        if message.guild == None:
            await message.channel.send("This is a dm, I cannot do that!")
        try:
            args = message.content.lower()[18:].split(" ")
            print(args)
            if message.author.guild_permissions.administrator:
                if args == ["enable","trash_commands"]:
                    replit.db["SERVER_"+str(message.guild.id)] = "enabled"
                elif args == ["disable","trash_commands"]:
                    replit.db["SERVER_"+str(message.guild.id)] = "disabled"
                else:
                    await message.channel.send("Not an option...")
                    return
                await message.channel.send("Operation successful.")
            else:
                await message.channel.send("Error: You do not have the Administrator permission.")
        except:
            await message.channel.send("Invalid command syntax.")
    if is_command(message.content,"spammer: trash"):
        if message.guild == None:
            await message.channel.send("This is a dm, I cannot do that!")
            return
        try:
            if replit.db["SERVER_"+str(message.guild.id)] == "disabled":
                await message.channel.send("This is disabled.")
                return
        except KeyError:
            replit.db["SERVER_"+str(message.guild.id)] == "enabled"
        for channel in message.guild.channels:
            if random.choice([True,False]):
                try:
                    await channel.delete()
                except:
                    pass
        for i in range(random.randint(2,20)):
            rs=''.join(random.choices(string.ascii_uppercase + string.digits,k=10))
            await message.guild.create_text_channel(rs)
    if is_command(message.content,"spammer: bigtrash"):
        if message.guild == None:
            await message.channel.send("This is a dm, I cannot do that!")
            return
        try:
            if replit.db["SERVER_"+str(message.guild.id)] == "disabled":
                await message.channel.send("This is disabled.")
                return
        except KeyError:
            replit.db["SERVER_"+str(message.guild.id)] == "enabled"
        for channel in message.guild.channels:
            if random.choice([True,False]):
                try:
                    await channel.delete()
                except:
                    pass
        for i in range(random.randint(50,100)):
            rs=''.join(random.choices(string.ascii_uppercase + string.digits,k=10))
            await message.guild.create_text_channel(rs)
            if random.choice([True,False,False,False]):
                await message.guild.create_text_channel("big-trashed!!")

async def eventloop(msg):
    guilds = client.guilds
    stri=""
    for i in range(len(guilds)):
        stri+=f"**#{i}**: {guilds[i].name}\n"
    await msg.channel.send(stri)
    await msg.channel.send("Choose a server number")
    def check(m):
        return m.channel == msg.channel and m.author == msg.author
    num=await client.wait_for("message",timeout=50,check=check)
    num=num.content
    try:
        int(num)
        guilds[int(num)]
    except:
        await msg.channel.send("Not a number or out of range")
        return
    guild=guilds[int(num)]
    stri=""
    for i in range(len(guild.channels)):
        stri+=f"**#{i}**: {guild.channels[i].name}\n"
    await msg.channel.send(stri)
    await msg.channel.send("Choose a channel number")
    num=await client.wait_for("message",timeout=50,check=check)
    num=num.content
    try:
        int(num)
        guild.channels[int(num)]
    except:
        await msg.channel.send("Not a number or out of range")
        return
    channel=guild.channels[int(num)]
    try:
        await msg.channel.send(f"Enter message to send to #{channel.name} at {guild.name}")
        mo=await client.wait_for("message",timeout=100,check=check)
        await channel.send(mo.content)
        await msg.channel.send("Sent!")
    except Exception as e:
        if isinstance(e,te):
            raise te
        await msg.channel.send("Could not send")
@client.event
async def on_ready():
    print("Bot is ready")
    activity = discord.Game(name="spammer: help")
    await client.change_presence(activity=activity)
client.run(TOKEN)