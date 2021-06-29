import traceback
import os
import keep_alive
import string
import replit
import psutil
from datetime import datetime
import time
import asyncio

from asyncio.exceptions import TimeoutError as te
from discord_components import DiscordComponents, Button, ButtonStyle, ActionRow, InteractionType

from asyncio import sleep

import random

keep_alive.keep_alive()

import discord
from discord.ext import commands


TOKEN = os.getenv('DISCORD_TOKEN')

bad_words=["\x66\x75\x63\x6b","\x73\x68\x69\x74","\x64\x69\x63\x6b","\x70\x65\x6e\x69\x73","\x62\x69\x74\x63\x68","\x73\x65\x78","\x73\x65\x78y","ssa"[::-1],"🖕","\x70\x6f\x72\x6e"]

def is_command(messagetext,command):
    return messagetext.lower() == command or messagetext.lower().startswith(command+" ")

correct =  0x00000000
wrong   =  0x00000001
timeout = -0x00000001 

def GetRandomColor():
    return random.choice([0xCCA8FF,0x00DEAE,0xFC8A68,0xFC6868,0x4F87FF])

class Question(object):
    def __init__(this,client:discord.Client,answer:int,question:str,channel,user:discord.User,options:list):
        this.client = client
        this.answer = answer 
        this.options = options 
        this.question = question
        this.channel = channel
        this.user = user

    async def ask(this,author):

        def check(ctx,user):
            return ctx.message == this.message and this.user == user;

        embed = discord.Embed(title="Question",description=this.question,color=GetRandomColor())
        for i in range(1,4+1):
            embed.add_field(name=str(i),value=this.options[i-1],inline=False)
        this.message = await this.channel.send(
            embed=embed,
            components=[
                [
                    Button(label="1",style=ButtonStyle.blue),
                    Button(label="2",style=ButtonStyle.blue),
                    Button(label="3",style=ButtonStyle.blue),
                    Button(label="4",style=ButtonStyle.blue)
                ]
            ]
        )
        # await this.message.add_reaction("1️⃣")
        # await this.message.add_reaction("2️⃣")
        # await this.message.add_reaction("3️⃣")
        # await this.message.add_reaction("4️⃣")

        try:
            # react,user = await bot.wait_for("reaction_add",check=check,timeout = 30)
            # print(react.emoji[0],str(this.answer))
            interaction = await bot.wait_for("button_click", check = lambda i: i.message.id == this.message.id and i.author.id == author.id,timeout=30)
            # interaction.component.label
            await interaction.respond(content="Answered!",type=InteractionType.UpdateMessage)
            if interaction.component.label == str(this.answer):
                return correct
            else:
                return wrong
        except te:
            await this.channel.send("Timeout, you lost $1000.")
            return timeout
        

spamming=True


bot = commands.Bot(command_prefix=("spammer: ","Spammer: ","SPAMMER: "), case_insensitive=True)

questions_file = open("questions.txt")
questions_fetched = []

class TemporaryQuestion(object):
    def __init__(this,question,answer,options):
        this.question = question
        this.answer = answer
        this.options = options
    def __repr__(this):
        return f"TemporaryQuestion(question={repr(this.question)},answer={repr(this.answer)},options={repr(this.options)})"

for i in questions_file:
    q = i.split("\\")
    questions_fetched.append(TemporaryQuestion(question=q[0],answer=q[1],options=eval(q[2])))

print(questions_fetched)

@bot.event
async def on_message(message):
    global spamming
    # if message.author == bot.user:
    #     return
    if any(ext.strip() in message.content.lower().replace(","," ").replace("."," ").replace("?"," ").split(" ") for ext in bad_words) and message.guild and not message.channel.is_nsfw():
        await message.reply(f"<@{message.author.id}> Woah! Don't say that...")
        try:
            await message.delete()
        except discord.errors.Forbidden:
            pass
        return
    if message.content.endswith("<del>"):
        await asyncio.sleep(2)
        await message.delete()
    if message.guild == None:
        print(f"@{message.author.name}: {message.content}")
    else:
        print(f"{message.guild.name}#{message.channel.name}@{message.author.name}: {message.content}")

    if message.content.startswith("spammer: game ") and message.content[14:] in ["work","bal"]:
        await message.channel.send("This command doesn't exist anymore. Hint: commands that start with the name `game` do not have `game` in the beginning anymore.\nFor example: `spammer: game work` is now `spammer: work`.")

    await bot.process_commands(message)

bot.remove_command("help")
@bot.command(pass_context=True)
async def help(ctx,command:str="all"):
    message = ctx.message
    # if not message.guild:
    #     await message.channel.send("I'm sorry, but this command in a DM is not supported anymore and can cause issues.")
    #     return
    try:
        # user_text=message.content[13:].strip()
        if command=="all":
            embedNum=0
            embeds = []
            embedVar = discord.Embed(title="Commands [1]", description="The prefix is `spammer:`", color=GetRandomColor())
            embedVar.add_field(name="help", value="Gets help", inline=False)
            embedVar.add_field(name="spam", value="Spams", inline=False)
            embedVar.add_field(name="stop", value="Stops spam", inline=False)
            embedVar.add_field(name="choose", value="Choose an option", inline=False)
            embeds.append(embedVar)
            embedVar = discord.Embed(title="Commands [2]",description = "The prefix is `spammer:`", color = GetRandomColor())
            embedVar.add_field(name="die", value="Self destruct", inline=False)
            embedVar.add_field(name="delete", value="Delete this.", inline=False)
            embedVar.add_field(name="ran", value="Random number", inline=False)
            embedVar.add_field(name="work", value="Work", inline=False)
            embeds.append(embedVar)
            embedVar = discord.Embed(title="Commands [3]",description = "The prefix is `spammer:`", color = GetRandomColor())
            embedVar.add_field(name="bal", value="View balance", inline=False)
            embedVar.add_field(name="inv", value="View inventory", inline=False)
            embedVar.add_field(name="shop", value="View shop", inline=False)
            embedVar.add_field(name="buy", value="Buy item", inline=False)
            embeds.append(embedVar)
            embedVar = discord.Embed(title="Commands [4]",description = "The prefix is `spammer:`", color = GetRandomColor())
            embedVar.add_field(name="lock", value="Lock channel", inline=False)
            embedVar.add_field(name="unlock", value="Unlock channel", inline=False)
            embedVar.add_field(name="purge", value="Delete messages", inline=False)
            embedVar.add_field(name="giveaway", value="Start a giveaway [BETA]", inline=False)
            embeds.append(embedVar)
            embedVar = discord.Embed(title="Commands [5]",description = "The prefix is `spammer:`", color = GetRandomColor())
            embedVar.add_field(name="status", value="View current stats", inline=False)
            embedVar.add_field(name="credits", value="Credits", inline=False)
            embedVar.add_field(name="daily", value="Claim and view daily streak", inline=False)
            embedVar.add_field(name="timer", value="Timer", inline=False)
            embeds.append(embedVar)
            embedVar = discord.Embed(title="Commands [6]",description = "The prefix is `spammer:`", color = GetRandomColor())
            embedVar.add_field(name="stopwatch_start", value="Start stopwatch", inline=False)
            embedVar.add_field(name="stopwatch_get", value="Get stopwatch time", inline=False)
            embedVar.add_field(name="animation", value="Displays bouncing ball animation", inline=False)
            embeds.append(embedVar)


            m = await message.channel.send(embed=embeds[embedNum],components=[[Button(label="<"),Button(label=">")]])

            def check(ctx):
                print("CHECK",ctx.message.id == m.id)
                return ctx.message.id == m.id
                # return str(ctx.emoji) in ['⬅️', '➡️'] and ctx.message == m and user == message.author

            # await m.add_reaction("⬅️")
            # await m.add_reaction("➡️")
            while True:
                try:
                    # react,user = await bot.wait_for("reaction_add",check=check,timeout = 30)
                    # if react.emoji == "➡️":
                    #     embedNum += 1
                    #     if embedNum>=len(embeds):
                    #         embedNum = 0;
                    # if react.emoji == "⬅️":
                    #     embedNum -= 1
                    #     if embedNum<0:
                    #         embedNum = len(embeds)-1;
                    # await react.remove(user)

                    interaction = await bot.wait_for("button_click", check = check, timeout=30)
                    print(interaction.component.label)
                    if interaction.component.label == ">":
                        embedNum+=1
                        if embedNum>=len(embeds):
                            embedNum = 0;
                    else:
                        embedNum -= 1
                        if embedNum<0:
                            embedNum = len(embeds)-1;

                    await interaction.respond(embed=embeds[embedNum],type=InteractionType.UpdateMessage)                    

                    # await m.edit(embed = embeds[embedNum])
                    print("edited")
                except te:
                    emb = discord.Embed(title="This message has timed out.",description="Please start a new help page.")
                    await m.edit(embed=emb)
                    break
        if command=="all":
            return
        elif command=="help":
            await message.channel.send("You already know what this means dummy")
        elif command == "spam":
            await message.channel.send(
"""\
Syntax: `spammer: spam <number> <text>`
Spams `<text>` `<number>` of times.
Variables:
`$count` : Count
`$CurrentMessage` : Current message that's being sent
"""
            )
        elif command == "choose":
            await message.channel.send(
"""\
Syntax: `spammer: choose <options split by commas>`
Sends a random message in <options>.
"""
            )
        elif command == 'credits':
            await message.channel.send(
"""\
Syntax: `spammer: credits`
See the credits of Spammer.
"""
            )
        elif command == "stop":
            await message.channel.send(
"""\
Syntax: `spammer: stop`
Stops spam.
"""
            )
        elif command == "status":
            await message.channel.send(
"""\
Syntax: `spammer: status`
View stats of Spammer right now.
"""
            )
        elif command == "ran":
            await message.channel.send(
"""\
Syntax: `spammer: ran <start> <end>`
Random number between `<start>` and `<end>`
"""
            )
        elif command == "clear":
            await message.channel.send(
"""\
Syntax: `spammer: clear`
Clear the channel
"""
            )
        elif command == "die":
            await message.channel.send(
"""\
Syntax: `spammer: die`
Self destruct
"""
            )
        elif command == "delete":
            await message.channel.send(
"""\
Syntax: `spammer: delete`
Delete this message
"""
            )
        elif command == "work":
            await message.channel.send(
"""\
Syntax: `spammer: work`
Earn money in the game
"""
            )
        elif command == "bal":
            await message.channel.send(
"""\
Syntax: `spammer: bal`
See your amount of money in the game
"""
            )
        elif command == 'lock':
            await message.channel.send(
"""\
Syntax: `spammer: lock`
Lock this channel.
"""
            )
        elif command == 'unlock':
            await message.channel.send(
"""\
Syntax: `spammer: unlock`
Unlock this channel.
"""
            )
        elif command == 'purge':
            await message.channel.send(
"""\
Syntax: `spammer: purge <optional number>`
Deletes the previous <optional number> messages, if not specified will clear channel.
**Note: use `spammer: clear` if you want to clear the entire channel as discord does not allow bots to delete messages older than 2 weeks.**
"""
            )
        elif command == 'giveaway':
            await message.channel.send(
"""\
Syntax: `spammer: giveaway <title> <number of winners> <seconds> <optional mins> <optional hours> <optional days> <optional weeks>`
Starts a giveaway which people can click react to enter.
**This is a beta feature.**
For titles with spaces, quote it, for example `spammer: giveaway "title with spaces" 1 1`
"""
            )
        elif command == "daily":
            await message.channel.send(
"""\
Syntax: `spammer: daily`
Claim your daily then shows how many times you claimed.
If you already claimed it shows how many times you claimed, but you do not get anything.
"""
            )
        elif command == "timer":
            await message.channel.send(
"""\
Syntax: `spammer: timer <seconds> <optional mins> <optional hours>`
Countdown timer
"""
            )
        elif command == "stopwatch_start":
            await message.channel.send(
"""\
Syntax: `spammer: stopwatch_start`
Start stopwatch and gives you the stopwatch ID. Use `spammer: stopwatch_get <id>` to get the time passed since start.
"""
            )
        elif command == "stopwatch_get":
            await message.channel.send(
"""\
Syntax: `spammer: stopwatch_get <id>`
Gets the time passed since start of a timer by ID.
"""
            )
        elif command == "animation":
            await message.channel.send(
"""\
Syntax: `spammer: animation`
Displays a bouncing ball. Please do not spam this! The more animations at once the slower it will be.
"""
            )
        elif command == "stopwatch":
            await message.channel.send(
"""\
How stopwatch works:
Use `spammer: stopwatch_start` to start the stopwatch. It will give you an ID.
Use `spammer: stopwatch_get <id>` to get the time passed since start.
"""
            )
        elif command == "inv":
            await message.channel.send(
"""\
Syntax: `spammer: inv`
View your inventory
"""
            )
        elif command == "shop":
            await message.channel.send(
"""\
Syntax: `spammer: shop`
View shop
"""
            )
        elif command == "buy":
            await message.channel.send(
"""\
Syntax: `spammer: buy`
Buy item that you can view in the shop.
"""
            )
        else:
            await message.channel.send("Unknown command!")
    except:
        pass

@bot.command(name="work",pass_context=True)
async def game_work(ctx):
    message = ctx.message
    # if not message.guild:
    #     await message.channel.send("I'm sorry, but this command in a DM is not supported anymore and can cause issues.")
    #     return
    if str(message.author.id) in replit.db.keys():
        if float(replit.db[str(message.author.id)]['last'])+1000 > time.time():
            await message.channel.send(f"You need to wait {float(replit.db[str(message.author.id)]['last'])+1000 - time.time()} seconds before you can work again!")
            return
        stuff = replit.db[str(message.author.id)]
        stuff['last'] = str(time.time())
        replit.db[str(message.author.id)] = stuff 
        questions = []
        for i in questions_fetched:
            questions.append(Question(client=bot,answer=i.answer,question=i.question,channel=message.channel,user=message.author,options=i.options))
        que = await random.choice(questions).ask(ctx.author)
        if que == correct:
            mon = 12000
            emb=discord.Embed(title="Good work!",description=f"You answered correct and got ⏣{mon}!",color=GetRandomColor())
            # await message.channel.send(embed=emb)
            await ctx.send(embed=emb)
        elif que == wrong:
            mon = random.randint(-7000,-1000)
            mg = False
            try:
                stuff["items"]
                if stuff["items"].count("moneyguard")>0:
                    stuff["items"].remove("moneyguard")
                emb=discord.Embed(title="Wrong answer!",description=f"You answered wrong, however you had a moneyguard, so you didn't lose anything.",color=GetRandomColor())
                # await ctx.send(embed = emb)
                await ctx.send(embed=emb)
                return
            except KeyError:
                pass
            emb=discord.Embed(title="Wrong answer!",description=f"You answered wrong and lost ⏣{-mon}.",color=GetRandomColor())
            await message.channel.send(embed=emb)
        elif que == timeout:
            mon=-1000 
        stuff['money']+=mon
        replit.db[str(message.author.id)] = stuff
    else:
        replit.db[str(message.author.id)] = {"money":0,"last":0}
        await message.channel.send("You joined the game! Do `spammer: work` to earn money.")
@bot.command(pass_context=True,name="bal")
async def game_bal(ctx):
    message = ctx.message
    if str(message.author.id) in replit.db.keys():
        value=replit.db[str(message.author.id)]['money']
        b=f'{value:,}'
        emb=discord.Embed(title=f"{message.author}'s balance",description=f"Balance: ⏣{b}")
        emb.set_footer(text=datetime.strftime(datetime.now(),"%m-%d-%Y %H:%M:%S"))
        await message.channel.send(embed=emb)
        
    else:
        await message.channel.send("You haven't joined the game so you have nothing. Do `spammer: work` to start.")

@bot.command(pass_context=True)
async def fish(ctx):
    message = ctx.message
    if str(ctx.message.author.id) in replit.db.keys() and replit.db[ctx.message.author.id]["lastfish"]:
        if float(replit.db[str(ctx.message.author.id)]['last'])+1000 > time.time():
            await ctx.send(f"You need to wait {float(replit.db[str(message.author.id)]['lastfish'])+1000 - time.time()} seconds before you can fish again!")
            return
    else:
        await ctx.send("You don't have an account.. Run `spammer: work` to start.")
        return
    kv = {"gfish":"Goldfishes","fish":"Fishes","nothing":"Nothing"}
    item = random.choice(kv.keys(),item)
    num = random.randint(1,5)
    if item=="nothing":
        await ctx.send(f"You brought back Nothing!")
        return 
    
    await ctx.send(f"You broght back {num} {item}.")
    i=replit.db[ctx.message.author.id]
    for i in range(num):
        i["items"].append(item)
    replit.db[ctx.message.author.id] = i


@bot.command(pass_context=True)
async def stop(ctx):
    global spamming
    message = ctx.message
    try:
        await message.channel.send("Stopping.")
    except:
        pass
    spamming=False
@bot.command(pass_context=True)
async def easteregg(ctx):
    message = ctx.message
    try:
        await message.channel.send("There are no easter eggs.")
    except:
        pass
@bot.command(pass_context=True)
async def delete(ctx):
    message = ctx.message
    try:
        await message.delete()
    except:
        await message.channel.send("I don't have permissions.")
@bot.command(pass_context=True)
async def die(ctx):
    message = ctx.message
    await message.channel.send("Self destructing in 3..")
    await sleep(1)
    await message.channel.send("Self destructing in 2..")
    await sleep(1)
    await message.channel.send("Self destructing in 1..")
    await sleep(1)
    await message.channel.send(":boom:"*4)
    await sleep(2)
    await message.channel.send("Actually, I think I'l stick around.")
@bot.command(pass_context=True)
async def credits(ctx):
    message = ctx.message
    embedVar = discord.Embed(title="Credits", description="Credits for the bot", color=GetRandomColor())
    embedVar.add_field(name="Who made this?", value=f"{await bot.fetch_user(589894019597729822)}", inline=False)
    embedVar.add_field(name="Special thanks to...", value=f"{await bot.fetch_user(797124067663544380)} for helping me to think of what to put in this bot, helping me design the bot, and suggesting a lot.", inline=False)
    embedVar.add_field(name="Invite to your server", value="[Invite to your server](https://spammerdiscordbot.maxjiang2021.repl.co)", inline=False)
    await message.channel.send(embed=embedVar)
@bot.command(pass_context=True)
async def choose(ctx):
    message = ctx.message
    options = message.content[15:].split(",")
    try:
        if len(options)==1 and options!=['']:
            await ctx.send("There's only one option :thinking:")
            return
        option = random.choice(options)
        if not option.strip():
            await ctx.send("Empty message.")
            return
        await ctx.send(option)
    except:
        await message.channel.send("Invalid command syntax. Run `spammer: help choose` for more information.")
@bot.command(pass_context=True)
async def spam(ctx):
    global spamming
    message = ctx.message
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
@bot.command(pass_context=True)
async def ran(ctx,start:int,end:int):
    try:
        if (start>end):
            await ctx.send("The start is bigger than the end??? :thinking:")
            return
        else:
            await ctx.send(str(random.randint(start,end)))
    except:
        await ctx.send("Sorry, something went wrong!!")
@ran.error
async def ran_error(ctx):
    await ctx.send("Invalid command syntax.")
@bot.command(pass_context=True)
async def manage(ctx,command:str,password:str):
    message = ctx.message
    if message.guild:
        await message.delete()
        msg=await message.channel.send("No. Do not try to manage me in a public server. Do it privatly in a DM.")
        await sleep(2)
        await msg.delete()
        return
    if command=="sendmessage":
        if password==os.getenv("PASSWORD"):
            try:
                await eventloop(message)
            except te:
                await message.channel.send("You didn't reply...")
            except Exception:
                await message.channel.send("Something went wrong... The error is: \n```"+traceback.format_exc()+"```")
    if command=="delete":
        if password==os.getenv("PASSWORD"):
            try:
                await message.channel.send("Post the message ID")
                msg=await bot.wait_for("message",check=lambda c:c.channel==message.channel and c.author == message.author,timeout=30)
                itms=msg.content.split("-")
                c=await bot.fetch_channel(int(itms[0]))
                delm=await c.fetch_message(int(itms[1]))
                await delm.delete()
            except (ValueError,IndexError):
                await message.channel.send("Not a message ID")
                return
            except te:
                await message.channel.send("Timeout, you didn't reply...")
                return
            except Exception:
                await message.channel.send("Something went wrong... The error is: \n```"+traceback.format_exc()+"```")
                return
            await message.channel.send("Deleted!")
@bot.command(pass_context=True)
async def status(ctx):
    message = ctx.message
    emb = discord.Embed(title="Spammer stats",description="Lines of code: about 900",color=GetRandomColor())
    emb.add_field(name="CPU%",value=str(psutil.cpu_percent()))
    emb.add_field(name="MEMORY%",value=str(psutil.virtual_memory().percent))
    emb.add_field(name="#SERVERS",value=str(len(bot.guilds)))
    emb.add_field(name="#ASYNC TASKS",value=str(len(asyncio.all_tasks())))
    await message.channel.send(embed=emb)
@bot.command(pass_context=True)
async def nuke(ctx):
    message = ctx.message
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
@bot.command(pass_context=True)
async def settings(ctx,command:str,setting:str):
    message = ctx.message
    if message.guild == None:
        await message.channel.send("This is a dm, I cannot do that!")
    try:
        # args = message.content.lower()[18:].split(" ")
        # print(args)
        args = [command,setting]
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
@bot.command(pass_context=True)
async def trash(ctx):
    message = ctx.message
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
        else:
            try:
                await channel.edit(position=random.randint(0,len(message.guild.channels)))
            except:
                pass
    for i in range(random.randint(2,20)):
        rs=''.join(random.choices(string.ascii_uppercase + string.digits,k=10))
        await message.guild.create_text_channel(rs,position=random.randint(0,len(message.guild.channels)))
@bot.command(pass_context=True)
async def bigtrash(ctx):
    message = ctx.message
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
        else:
            try:
                await channel.edit(position=random.randint(0,len(message.guild.channels)))
            except:
                pass
    for i in range(random.randint(50,100)):
        rs=''.join(random.choices(string.ascii_uppercase + string.digits,k=10))
        await message.guild.create_text_channel(rs,position=random.randint(0,len(message.guild.channels)))
        if random.choice([True,False,False,False]):
            await message.guild.create_text_channel("big-trashed!!")

@bot.command(pass_context=True)
async def shuffletrash(ctx):
    message = ctx.message
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
            await channel.edit(position=random.randint(0,len(message.guild.channels)))
        except:
            pass

async def eventloop(msg):
    guilds = bot.guilds
    msgs=[]
    stri=""
    for i in range(len(guilds)):
        if len(stri)+len(f"**#{i}**: {guilds[i].name}\n")>2000:
            msgs.append(stri)
            stri=''
        stri+=f"**#{i}**: {guilds[i].name}\n"
    msgs.append(stri)
    for i in msgs:
        await msg.channel.send(i)
    await msg.channel.send("Choose a server number")
    def check(m):
        return m.channel == msg.channel and m.author == msg.author
    num=await bot.wait_for("message",timeout=50,check=check)
    num=num.content
    try:
        int(num)
        guilds[int(num)]
    except:
        await msg.channel.send("Not a number or out of range")
        return
    guild=guilds[int(num)]
    msgs=[]
    stri=""
    for i in range(len(guild.channels)):
        if len(stri)+len(f"**#{i}**: {guild.channels[i].name}\n")>2000:
            msgs.append(stri)
            stri=''
        stri+=f"**#{i}**: {guild.channels[i].name}\n"
    msgs.append(stri)
    for i in msgs:
        await msg.channel.send(i)
    await msg.channel.send("Choose a channel number")
    num=await bot.wait_for("message",timeout=50,check=check)
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
        mo=await bot.wait_for("message",timeout=100,check=check)
        m=await channel.send(mo.content)
        await msg.channel.send("Sent! ID: "+str(channel.id)+"-"+str(m.id))
    except Exception as e:
        if isinstance(e,te):
            raise te
        await msg.channel.send("Could not send")
@bot.event
async def on_ready():
    print("Bot is ready")
    DiscordComponents(bot)
    activity = discord.Game(name="spammer: help")
    await bot.change_presence(activity=activity)

@bot.command(pass_context=True,guild_only=True)
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    if not ctx.guild:
        await ctx.send("Server-only commands won't work in DMs!")
        return
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send('Channel locked.')
@lock.error
async def lock_error(ctx, error):
    print("U/LOCK error")
    if isinstance(error,commands.CheckFailure):
        await ctx.send('You at least need `manage_channels` permissions to use this.')
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("I don't have permissions!")

@bot.command(pass_context=True,guild_only=True)
@commands.has_permissions(manage_guild=True)
async def unlock(ctx):
    if not ctx.guild:
        await ctx.send("Server-only commands won't work in DMs!")
        return
    await ctx.send('Channel unlocked.')
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
@unlock.error
async def unlock_error(ctx, error):
    print("U/LOCK error")
    if isinstance(error,commands.CheckFailure):
        await ctx.send('You at least need `manage_server` permissions to use this.')
    else:
        await ctx.send("Hmm something went wrong. It could be because the argument format is incorrect.")

        
@bot.command(pass_context=True,guild_only=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx,number:int=999999999999999999999):
    if not ctx.guild:
        await ctx.send("Server-only commands won't work in DMs!")
        return
    messages = await ctx.channel.history(limit=number).flatten()
    await ctx.channel.delete_messages(messages)
@purge.error
async def purge_error(ctx,error):
    if isinstance(error,commands.CheckFailure):
        await ctx.send('You at least need `manage_messages` permissions to use this.')
    elif isinstance(error,commands.ArgumentParsingError) or isinstance(error,commands.BadArgument):
        await ctx.send("Invalid syntax. Type `spammer: help purge` for more information.")
    else:
        await ctx.send("Hmm... something went wrong. Discord does not allow bots to delete messages older than 2 weeks old. Use `spammer: clear` instead.")

import datetime as dt

@bot.command(pass_context=True,guild_only=True)
async def giveaway(ctx,title:str,winners:int,seconds:int,mins:int=0,hours:int=0,days:int=0,weeks:int=0):
    if not ctx.guild:
        await ctx.send("Server-only commands won't work in DMs!")
        return
    now=datetime.now()
    td=dt.timedelta(days=days,seconds=seconds,minutes=mins,hours=hours,weeks=weeks)
    end=now+td
    emb=discord.Embed(title=title,description=f"Item: {title}\nClick <:check:851490994586255400> to enter!\nEnds in {end-now}",color=GetRandomColor())
    m=await ctx.send("GIVEAWAY!!!",embed=emb)
    await m.add_reaction("<:check:851490994586255400>")
    for i in range(int(td.total_seconds()//60)):
        n=end-dt.datetime.now()
        emb=discord.Embed(title=title,description=f"Item: {title}\nClick <:check:851490994586255400> to enter!\nEnds in about {n-dt.timedelta(microseconds=n.microseconds)}\nWinners: {winners}",color=GetRandomColor())
        await m.edit(content="GIVEAWAY!!!",embed=emb)  
        await asyncio.sleep(60)
    n=end-dt.datetime.now()
    emb=discord.Embed(title=title,description=f"Item: {title}\nClick <:check:851490994586255400> to enter!\nEnds in about {n-dt.timedelta(microseconds=n.microseconds)}\nWinners: {winners}",color=GetRandomColor())
    await m.edit(content="GIVEAWAY!!!",embed=emb)  
    await asyncio.sleep(td.total_seconds()%60)
    u = discord.utils.get(bot.cached_messages, id=m.id)
    rs = u.reactions
    reactions=[]
    for i in rs:
        if i.me==True:
            r = await i.users().flatten()
            for j in r:
                reactions.append(j)
    print(reactions[1:])
    if len(reactions)==1:
        emb=discord.Embed(title=title,description=f"Item: {title}\nGiveaway ended. Not enough people joined.\nEnded at {end.strftime('%x %X')}",color=GetRandomColor())
    else:
        try:
            winner = random.sample(reactions[1:],winners)
        except ValueError:
            winner = reactions[1:]
        wrs = [f'<@{i.id}>' for i in winner]
        emb=discord.Embed(title=title,description=f"Item: {title}\nWinners: {','.join(wrs)}\nEnded at {end.strftime('%x %X')}",color=GetRandomColor())
    await m.edit(content="Giveaway ended.",embed=emb)    
@giveaway.error
async def giveaway_error(ctx,error):
    await ctx.send("Either the argument format is incorrect or something went wrong.")

    
@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send(f':ping_pong: Pong! | In {round(bot.latency * 1000)}ms')

@bot.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def clear(ctx):
    if not ctx.guild:
        await ctx.send("Server-only commands won't work in DMs!")
        return
    new_channel = await ctx.channel.clone()
    await new_channel.edit(position=ctx.channel.position)
    await ctx.channel.delete()
@clear.error
async def clear_error(ctx,error):
    if isinstance(error,commands.CheckFailure):
        await ctx.send("Error: you do not have the permission `manage_messages`.")
    else:
        await ctx.send("Something went wrong.")

@bot.event
async def on_message_delete(message):
    print(f"{message.author}'s message in channel {message.channel} of {message.guild} was deleted: {message.content}")

@bot.event
async def on_message_edit(before, after):
    message = before
    if message.author.id == bot.user.id:
        return
    print(f"{message.author}'s message in channel {message.channel} of {message.guild} was edited: {message.content} | {after.content}")

@bot.command(pass_context=True)
@commands.cooldown(1,86400,commands.BucketType.user)
async def daily(ctx):
    try:
        stuff = replit.db[str(ctx.message.author.id)]
        stuff["money"] += 10000
        try:
            stuff["dailyclaim"] +=1
        except KeyError:
            stuff["dailyclaim"] = 1
        replit.db[str(ctx.message.author.id)] = stuff
        em = discord.Embed(title=f"Daily claimed!",description=f"You got ⏣10,000.", color=GetRandomColor())
        em.set_footer(text=f"You have claimed your daily {stuff['dailyclaim']} times.")
        await ctx.send(embed=em)
    except KeyError:
        await ctx.send("You haven't started. Do `spammer: work` to start, then try this again.")
@daily.error
async def daily_error(ctx, error):
    stuff = replit.db[str(ctx.message.author.id)]
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"You've already claimed your daily.",description=f"Try again in {error.retry_after:.2f}s.", color=GetRandomColor())
        em.set_footer(text=f"You have claimed your daily {stuff['dailyclaim']} times.")
        await ctx.send(embed=em)
    if isinstance(error,commands.BadArgument) or isinstance(error,commands.ArgumentParsingError) or isinstance(error,commands.MissingRequiredArgument) or isinstance(error,commands.TooManyArguments):
        await ctx.send("Invalid argument")

@bot.command(pass_context=True)
async def timer(ctx,seconds:int,mins:int=0,hours:int=0):
    message = await ctx.send("Timer is starting...")
    start = datetime.now()
    end = start + dt.timedelta(0,seconds,0,0,mins,hours)
    for i in range(seconds+(mins*60)+(hours*60*60)):
        now = datetime.now()
        remaining = end - now
        if remaining < dt.timedelta(0,0,0,0,0,0,):
            break
        await message.edit(content=f"Remaining: {remaining}")
        await asyncio.sleep(2)
    await message.edit(content=f"Time's up!")
@timer.error
async def timer_error(ctx,error):
    if isinstance(error,commands.BadArgument) or isinstance(error,commands.ArgumentParsingError) or isinstance(error,commands.MissingRequiredArgument) or isinstance(error,commands.TooManyArguments):
        await ctx.send("Invalid command syntax. Run `spammer: help timer` for more information.")
import uuid

def does_not_exist(timer):
    try:
        replit.db[f"STOPWATCH_ID_{timer}"]
        return False
    except KeyError:
        return True

@bot.command(pass_context=True)
async def stopwatch_start(ctx):
    timer_id = uuid.uuid4()
    while not does_not_exist(timer_id):
        timer_id = uuid.uuid4()

    replit.db[f"STOPWATCH_ID_{timer_id}"] = repr(datetime.now())
    await ctx.send(f"Stopwatch ID: {timer_id}, use `spammer: stopwatch_get <ID>` to get the time passed.")

@bot.command(pass_context=True)
async def stopwatch_get(ctx,id:str):
    try:
        time_passed = datetime.now() - eval(replit.db[f"STOPWATCH_ID_{id}"],{"datetime":dt},{})
        await ctx.send(f"Time passed: {time_passed}")
    except KeyError:
        await ctx.send(f"Not a valid stopwatch ID")

def check_account(ctx):
    try:
        replit.db[str(ctx.message.author.id)]
        return True
    except:
        return False

@bot.command(pass_context=True)
async def shop(ctx,item:str="view"):
    item = item.lower()
    if check_account(ctx):
        stuff = replit.db[str(ctx.message.author.id)]
    else:
        ctx.send("You don't have an account... Run `spammer: work` to start.")
        return
    try:
        stuff["items"]
    except KeyError:
        stuff["items"] = []
    if item == "view":
        emb = discord.Embed(title="Shop items",color = GetRandomColor())
        emb.add_field(name="Money guard",value="ID `moneyguard`",inline=False)
        emb.set_footer(text="Use `spammer: shop <item>` to view more information on an item!\nUse `spammer: buy <item>` to get the item.")
        await ctx.send(embed=emb)
    elif item == "moneyguard":
        emb = discord.Embed(title=f"Money guard ({stuff['items'].count('moneyguard')} owned)",description="Prevents you from losing items when you answer wrong!",color=GetRandomColor())
        emb.set_footer(text="⏣5000")
        await ctx.send(embed = emb) 
    else:
        await ctx.send("That's not an item...")
    replit.db[str(ctx.message.author.id)] = stuff

def check_money(ctx,money):
    if check_account(ctx):
        if replit.db[str(ctx.message.author.id)]["money"] > money:
            return True
    return False

@bot.command(pass_context=True)
async def buy(ctx,item:str="nothing",amount:int=1):
    try:
        replit.db[str(ctx.message.author.id)]
    except KeyError:
        await ctx.send("You don't have an account... Run `spammer: work` to first start.")
        return
    stuff = replit.db[str(ctx.message.author.id)]
    try:
        stuff["items"]
    except KeyError:
        stuff["items"]=[]
    item = item.lower()
    if item=="nothing":
        await ctx.send("What do you want to buy?")
    elif item=="moneyguard":
        if check_money(ctx,5000*amount):
            stuff["money"]-=5000*amount
            for i in range(amount):
                stuff["items"].append("moneyguard")
        emb = discord.Embed(title="Purchased 1 moneyguard",description=f"Paid ⏣{5000*amount}.")
        await ctx.send(embed=emb)
    else:
        await ctx.send("That's not an item.")
from collections import Counter
@bot.command(pass_context=True)
async def inv(ctx):
    if check_account(ctx):
        try:
            replit.db[str(ctx.message.author.id)]["money"]
        except:
            await ctx.send("You don't have an inventory, buy something!")
        stuff = replit.db[str(ctx.message.author.id)]
        inv = dict(Counter(stuff["items"])).items()
        emb = discord.Embed(title=f"{ctx.message.author}'s inventory",color = GetRandomColor())
        kv = {"moneyguard":"Money Guard","fish":"Fish","gfish":"Goldfish"}
        for item,count in inv:
            emb.add_field(name=f"{count} {kv[item]}s",value=f"ID `{item}`")
        await ctx.send(embed=emb)
    else:
        await ctx.send("You don't have an account... Run `spammer: work` to start!")
@bot.command(pass_context=True)
async def animation(ctx):
    x=1
    y=2
    up = True
    ri = True
    mx = 5
    my = 10
    arr = [["⬛" for i in range(11)] for i in range(6)]
    m = await ctx.send("Loading...")
    for i in range(50):
        x+=ri*2-1
        y+=up*2-1
        s = ""
        arr[x][y]="🔵"
        for i in arr:
            s += "".join(i)
            s += "\n"
        await m.edit(content=s)
        await asyncio.sleep(1)
        arr[x][y]="⬛"
        if x<1:
            ri=True
        if x>=mx:
            ri=False
        if y<1:
            up=True
        if y>=my:
            up=False  

@bot.command(pass_context=True)
async def testcomp(ctx):
    await ctx.send("Click on the button!",components=[Button(label="test",style = ButtonStyle.blue)])
    interaction = await bot.wait_for("button_click", check = lambda i: i.component.label.startswith("test"))
    await interaction.respond(content = "Button clicked!")

bot.run(TOKEN)