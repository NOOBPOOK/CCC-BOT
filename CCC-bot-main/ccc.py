import nextcord
from nextcord.ui import Button, View 
from nextcord.utils import get
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import wikipedia
import smtplib
import datetime
import webbrowser
import youtube_dl
import humanfriendly
import time
import random
import asyncio
import asyncpraw
import youtube_dl
from youtubesearchpython.__future__ import VideosSearch

reddit = asyncpraw.Reddit(client_id= "rlxZ8ONX4K12gG28bslAQw",
                     client_secret = "SeclhK30B2TG7ndn7V4gRB6yQs5bmg",
                     username = "Advanced_Daikon756",
                     password = "#noobpookveduki1234",
                     user_agent = "scrbot")

intents=nextcord.Intents(messages = True, message_content=True, guilds = True, voice_states = True)
client = commands.Bot(command_prefix="&", help_command=None, intents=intents)
gameOver = True
cricket_p1 = ""
cricket_p2 = ""
player1 = ""
player2 = ""
turn = ""
tic_time = 0
gameOver = True
GameOver = True
board = []
music = []
queue = []
dur = []
que_time = 0

winningConditions = [
    [ 0, 1, 2],
    [ 3, 4, 5],
    [ 6, 7, 8],
    [ 0, 3, 6],
    [ 1, 4, 7],
    [ 2, 5, 8],
    [ 0, 4, 8],
    [ 2, 4, 6]
]
    
@client.command(pass_context = True)
async def join(ctx):
    if ctx.voice_client == None:
        if (ctx.author.voice):
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.reply("Bot connected to play music!🎶")
        else:
            await ctx.reply("You're not in a Voice Channel!🎶")
    else:
        await ctx.reply("The Bot is already connected to a Voice Channel!")
            
@client.command(pass_context = True)
async def leave(ctx):
    if ctx.voice_client:
        global music
        global queue
        global dur
        global que_time
        await ctx.voice_client.disconnect()
        await ctx.reply("Disconnected from Voice channel!")
        music = []
        queue = []
        dura = []
        que_time = 0
    else:
        await ctx.reply("The Bot is not connected to any Voice Channel!")
    
@client.command(pass_context = True)
async def play(ctx,* ,arg):
    if ctx.voice_client:
        if ctx.author.voice:
            global music
            global queue
            global dur
            global que_time
            video = VideosSearch(str(arg),limit=1)
            vid = await video.next()
            url =(vid['result'][0]['link'])
            name = (vid['result'][0]['title'])
            dura = (vid['result'][0]['duration'])
            if len(music) != 0:
                music.append(url)
                queue.append(name)
                dur.append(dura)
                x = dura.split(":")
                dt = int(x[0])*60 + int(x[1])
                que_time+=dt
                await ctx.message.delete()
                await ctx.send(f"**{name}** has been added to the queue\n**Expexted time:- **{int(que_time/60)}:{int(que_time%60)}!")
            else:
                music.append(url)
                queue.append(name)
                dur.append(dura)
                x = dura.split(":")
                dt = int(x[0])*60 + int(x[1])
                que_time+=dt
                await qplay(ctx, url)
        else:
            await ctx.reply("You are not connected to Voice Channel!")
    else:
        await ctx.reply(f"The Bot is not connected to any Voice Channel!")

@client.command()
async def q(ctx):
    global queue
    global dur
    global que_time
    if len(queue)>1:
        mins = int(que_time/60)
        sec = int(que_time%60)
        quebed = nextcord.Embed(title = f"MUSIC QUEUE🎶", description=('\n\n'.join(map(str,queue))) ,color=0x3498db)
        quebed.set_thumbnail(url = "https://cdn.pixabay.com/photo/2018/09/17/14/27/headphones-3683983_960_720.jpg")
        quebed.set_footer(text = f"Time for the whole queue {mins}mins {sec}seconds!")
        await ctx.reply(embed = quebed)
    else:
        await ctx.reply("No Queue Exits!")
    
@client.command()
async def qremove(ctx, n:int):
    global music
    global dur
    global queue
    global que_time
    if n<=(len(music)+1) and n !=0:
        await ctx.reply(f"{queue[n-1]} has been removed from the queue!\nQueue Updated!")
        del music[n-1]
        x = dur[n-1].split(":")
        dt = int(x[0])*60 + int(x[1])
        que_time-=dt
        del dur[n-1]
        del queue[n-1]
    else:
        await ctx.reply("Song doesn't exist at this Position!")

async def qplay(ctx,url):
    global music
    global queue
    global dur
    FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format':'bestaudio'}
    vc = ctx.voice_client
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url , download = False)
        try:
            await ctx.message.delete()
        except:
            print("Not Available!")
           
        url2 = info['formats'][0]['url']
        music_bed = nextcord.Embed(title = f"Music World!", description=f"{info['title']}", color=0x3498db)
        music_bed.set_image(url = f"{info['thumbnails'][3]['url']}")
        music_bed.set_thumbnail(url = "https://cdn.pixabay.com/photo/2018/09/17/14/27/headphones-3683983_960_720.jpg")
        music_bed.set_footer(text = f"Length of the song >>> {dur[0]}")
        await ctx.send(embed = music_bed)
        vc.play(await nextcord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS))
        await music_but(ctx)
               
async def music_but(ctx):
    global button1
    global button2
    global mus_but
    global view
    global but1
    global but2
    but1 = 0
    but2 = 0
    button1 = Button(label="Resume", style=nextcord.ButtonStyle.green, emoji="▶️")
    button2 = Button(label="Pause", style=nextcord.ButtonStyle.blurple, emoji="⏸")
    button3 = Button(label="Skip/Next", style=nextcord.ButtonStyle.danger, emoji="⏭️")
    view = View(timeout=500)
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    mus_but = await ctx.send(view = view)
    async def button_callback(interaction):
        global button2
        global mus_but
        global view
        global but2
        global but1
        if but2 == 1:
            button2.disabled = False
        ctx.voice_client.resume()
        button1.disabled = True
        await mus_but.edit(view = view)
        but1 = 1
    button1.callback = button_callback
    async def button_callback(interaction):
        global button1
        global mus_but
        global view
        global but2
        global but1
        if but1 == 1:
            button1.disabled = False
        ctx.voice_client.pause()
        button2.disabled = True
        await mus_but.edit(view = view)
        but2 = 1
    button2.callback = button_callback
    async def button_callback(interaction):
        global button1
        global button2
        global view
        global mus_but
        global music
        global queue
        global dur
        global que_time
        ctx.voice_client.stop()
        button1.disabled = True
        button2.disabled = True
        button3.disabled = True
        await mus_but.edit(view = view)
        del music[0]
        del queue[0]
        x = dur[0].split(":")
        dt = int(x[0])*60 + int(x[1])
        que_time-=dt
        del dur[0]
        try:
            url = music[0]
            await qplay(ctx, url)
        except:
            await ctx.send("Queue Ended 🎧!")
    button3.callback = button_callback
        
@client.event
async def on_ready():
    print("Bot just landed on the server!")
    
@client.command()
async def private(ctx):
    myEmbed = nextcord.Embed(title = "CCC UTILITIES", description=f"Hello there In Private! **{ctx.author}**\nHow may I help you?", color=0xffff00)
    myEmbed.set_author(name="CCC Utilities#6430")
    await ctx.author.send(embed=myEmbed)
    
@client.command()
async def wiki(ctx, *, arg):
    mes_1 = await ctx.reply("Searching Google!")
    try:
        results = wikipedia.page(arg)
        url = results.url
        content = results.content
        await mes_1.edit(content=f"According to CCC, {url}")
    except Exception as e:
        await mes_1.edit(content="Could not get what you were looking for!")
        
@client.command()
async def luckyroles(ctx, role_id :int):
    user_give = ctx.author
    user_rol = get(user_give.guild.roles, id=967856535982198875)#Owner Role
    user2_rol = get(user_give.guild.roles, id=967856535961231396)#Staff Helper role
    if user_rol in user_give.roles or user2_rol in user_give.roles or user_give == await client.fetch_user(763676643356835840):
        guild_mem = user_give.guild
        mem_list = []
        for member in guild_mem.members:
            mem_list.append(member)
            
        giveaway_mem = random.choice(mem_list)
        try:
            giv_role = get(user_give.guild.roles, id=role_id)
            await giveaway_mem.add_roles(giv_role)
            give_embed = nextcord.Embed(title="CCC UTILITIES", description = f"**{giveaway_mem}** \n You have just won the giveaway held by **{ctx.author}**\n You have got the **{giv_role}** !🎆🎊🎉*", color=0xffff00)
            await ctx.send(embed=give_embed)
            try:
                await giveaway_mem.send(embed=give_embed)
            except:
                await ctx.author.send("Cannot send message to the user who won the giveaway!")
        except:
            await ctx.send("Above mentioned role_id doesn't exist. \nPlease put the role_id correctly or either the bot is unable to give the role due to less permissions!")
    else:
        await ctx.send(f"You don't have the necessary role to perrform a giveaway!\n You should have **{user_rol}** or **{user2_rol}** to perform giveaway in the server!")
        
@client.command()
async def admin(ctx, pas:int , chn_id:int, *, arg):
    if pas == 2333:
        try:
            chn = client.get_channel(chn_id)
            admin_ctx = await ctx.author.send("Sending your message!")
            await chn.send(arg)
            await admin_ctx.edit(content=f"Your message has been sent successfully to this channel {chn.mention}")
        except Exception as e:
            await admin_ctx.edit(content=f"Your message could not be delivered to the channel!\n Here is why {e}")
    else:
        await ctx.send(f"The above password is Wrong {ctx.author.mention}!\nTry again!")
        
@client.command()
async def meme(ctx):
    all_subs = []
    subreddit = await reddit.subreddit("memes")
    top_red = subreddit.top("day", limit=50)
    async for top_hot in top_red:
        all_subs.append(top_hot)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    memEmbed = nextcord.Embed(title= name)
    memEmbed.set_thumbnail(url = "https://static-prod.adweek.com/wp-content/uploads/2021/06/Reddit-Avatar-Builder-Hero-1280x680.png")
    memEmbed.set_image(url = url)
    ctx_mem = await ctx.reply(embed = memEmbed)
    await meme_but(ctx,ctx_mem)
        
async def meme_but(ctx,ctx_mem):
    button = Button(label="Another One!", style=nextcord.ButtonStyle.blurple, emoji="🤚")
    view = View(timeout=100)
    view.add_item(button)
    async def button_callback(interaction):
        await mem_rep(ctx,ctx_mem)
    button.callback = button_callback
    await ctx.reply(view = view)
        
async def mem_rep(ctx,ctx_mem):
    all_subs = []
    subreddit = await reddit.subreddit("memes")
    top_red = subreddit.top("day", limit=50)
    async for top_hot in top_red:
        all_subs.append(top_hot)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    memEmbed = nextcord.Embed(title= name)
    memEmbed.set_thumbnail(url = "https://static-prod.adweek.com/wp-content/uploads/2021/06/Reddit-Avatar-Builder-Hero-1280x680.png")
    memEmbed.set_image(url = url)
    await ctx_mem.edit(embed = memEmbed)
            
@client.command()
async def help(ctx):
    help_embed = nextcord.Embed(title = "**Content Creator Community**", description = "Here are the various cmds to help you out!", color=0xffff00)
    help_embed.add_field(name="**🤖COMMANDS🤖**", value=f"1.**\&private**: Opens a dm with the user. \n2.**\&wiki [subject]**: Gives Information about the concerned subject. \n3.**\&luckyroles [role_id]**: Makes a giveaway of the mentioned role if the user has suitable permissions.\n4.**\&admin [password] [channel_id] [content]**: Sends the content matter to the described channel through the bot.\n5.**\&selfrole**: Send various options available for roles in the server.\n6.**\&meme**:Gives memes from reddit.",inline = True)
    help_embed.set_author(name = "CCC Utilities#6430")
    await ctx.reply(embed = help_embed)
            
@client.command()
async def cricket(ctx, p1 : nextcord.Member, p2 : nextcord.Member):   
    global gameOver
    if gameOver and p1 != await client.fetch_user(949215188672974871) and p2 != await client.fetch_user(949215188672974871):
        global runs1
        global runs2
        global wickets1
        global wickets2
        global balls1
        global balls2
        global score1
        global score2
        global length1
        global length2
        global cricket_p1
        global cricket_p2
        global target
        global ing1
        gameOver = False
        ing1 = False
        runs1 = ""
        runs2 = ""
        score1 = 0
        score2 = 0
        target = 0
        wickets1 = 0
        wickets2 = 0
        balls1 = ""
        balls2 = ""
        length1 = 0
        length2 = 0
        cricket_toss = random.randint(1, 2)
        if cricket_toss == 1:
            cricket_p1 = p1
            cricket_p2 = p2
        else:
            cricket_p1 = p2
            cricket_p2 = p1
        myEmbed = nextcord.Embed(title = "World Icc nextcord Tournament", description="🎮Cricket🎮", color=0xffff00)
        myEmbed.add_field(name="RULES:-" ,value=f"1.Press the button only once.\n2. {cricket_p1.mention} will bat first.\n3.{cricket_p2.mention} will ball now.\n4. {cricket_p1.mention} should click button immediately while {cricket_p2.mention} will click after 3sec!\n5. Click the button only once!", inline=True)
        myEmbed.set_author(name="Cricket bot#0162")
        await ctx.send(embed=myEmbed)
        time.sleep(10)
        await play(ctx)
    else:
        await ctx.send(f"A Game is already in progress between {p1.mention} and {p2.mention}!")
        
async def play(ctx):
    global cricket_p1
    global cricket_p2
    print(cricket_p1)
    print(cricket_p2)
    button = Button(label="One", style = nextcord.ButtonStyle.green, emoji="1️⃣")
    button2 = Button(label="Two", style = nextcord.ButtonStyle.green, emoji="2️⃣")
    button3 = Button(label="Three", style = nextcord.ButtonStyle.blurple, emoji="3️⃣")
    button4 = Button(label="Four", style = nextcord.ButtonStyle.blurple, emoji="4️⃣")
    button5 = Button(label="Six", style = nextcord.ButtonStyle.danger, emoji="6️⃣")
    view = View(timeout=20)
    view.add_item(button)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)
    view.add_item(button5)
    async def button_callback(interaction):
        if interaction.user == cricket_p1:
            abc = "One"
            move1(abc)
            await asyncio.sleep(5)
            await match(ctx)
        elif interaction.user == cricket_p2:
            ugh = "One"
            move2(ugh)
    button.callback = button_callback
    async def button_callback(interaction):
        if interaction.user == cricket_p1:
            abc = "Two"
            move1(abc)
            await asyncio.sleep(5)
            await match(ctx)
        elif interaction.user == cricket_p2:
            ugh = "Two"
            move2(ugh)
    button2.callback = button_callback
    async def button_callback(interaction):
        if interaction.user == cricket_p1:
            abc = "Three"
            move1(abc)
            await asyncio.sleep(5)
            await match(ctx)
        elif interaction.user == cricket_p2:
            ugh = "Three"
            move2(ugh)
    button3.callback = button_callback
    async def button_callback(interaction):
        if interaction.user == cricket_p1:
            abc = "Four"
            move1(abc)
            await asyncio.sleep(5)
            await match(ctx)
        elif interaction.user == cricket_p2:
            ugh = "Four"
            move2(ugh)
    button4.callback = button_callback
    async def button_callback(interaction):
        if interaction.user == cricket_p1:
            abc = "Six"
            move1(abc)
            await asyncio.sleep(5)
            await match(ctx)
        elif interaction.user == cricket_p2:
            ugh = "Six"
            move2(ugh)
    button5.callback = button_callback
    await ctx.send(view=view)

#runs 
def move1(abc):
    global runs1
    global score1
    runs1 = abc
    if abc == "One":
        score1+=1
    elif abc == "Two":
        score1+=2
    elif abc == "Three":
        score1+=3
    elif abc == "Four":
        score1+=4
    elif abc == "Six":
        score1+=6
    print(runs1)
    print(score1)
    
#balls
def move2(ugh):
    global balls1
    balls1 = ugh
    print(balls1)
    
async def match(ctx):
    print("Run test")
    global runs1
    global balls1
    global score1
    global wickets1
    global length1
    global cricket_p1
    global cricket_p2
    print(runs1)
    print(score1)
    print(cricket_p1)
    print(cricket_p2)
    if runs1 == "One" and balls1 == "One":
        wickets1 +=1
        score1-=1
        length1+=1
        myEmbed = nextcord.Embed(title = "ICC WORLD CUP", description=f"{cricket_p1.mention} One ⚔ One {cricket_p2.mention}", color=0xffff00)
        myEmbed.add_field(name="Score:", value=f"{cricket_p1.mention}:{score1}/{wickets1}:{cricket_p2.mention} in {length1} balls", inline=True)
        myEmbed.set_thumbnail(url = "https://m.media-amazon.com/images/I/81tzdBv+89L._SY450_.jpg")
        myEmbed.set_author(name="CCC Utilities#6430")
        await ctx.send(embed=myEmbed)
        wickets1 +=1
        runs1 = "" 
        balls1 = ""
        await asyncio.sleep(3)
        await pointcount(ctx)
    elif runs1 == "Two" and balls1 == "Two":
        wickets1 +=1
        score1 -=2
        length1+=1
        myEmbed = nextcord.Embed(title = "ICC WORLD CUP", description=f"{cricket_p1.mention} Two ⚔ Two {cricket_p2.mention}", color=0xffff00)
        myEmbed.add_field(name="Score:", value=f"{cricket_p1.mention}:{score1}/{wickets1}:{cricket_p2.mention} in {length1} balls", inline=True)
        myEmbed.set_thumbnail(url = "https://m.media-amazon.com/images/I/81tzdBv+89L._SY450_.jpg")
        myEmbed.set_author(name="CCC Utilities#6430")
        await ctx.send(embed=myEmbed)
        runs1 = "" 
        balls1 = ""
        await asyncio.sleep(3)
        await pointcount(ctx)
    elif runs1 == "Three" and balls1 == "Three":
        wickets1 +=1
        score1-=3
        length1+=1
        myEmbed = nextcord.Embed(title = "ICC WORLD CUP", description=f"{cricket_p1.mention} Three ⚔ Three {cricket_p2.mention}", color=0xffff00)
        myEmbed.add_field(name="Score:", value=f"{cricket_p1.mention}:{score1}/{wickets1}:{cricket_p2.mention} in {length1} balls", inline=True)
        myEmbed.set_thumbnail(url = "https://m.media-amazon.com/images/I/81tzdBv+89L._SY450_.jpg")
        myEmbed.set_author(name="CCC Utilities#6430")
        await ctx.send(embed=myEmbed)
        runs1 = "" 
        balls1 = ""
        await asyncio.sleep(3)
        await pointcount(ctx)
    elif runs1 == "Four" and balls1 == "Four":
        wickets1 +=1
        score1 -=4
        length1+=1
        myEmbed = nextcord.Embed(title = "ICC WORLD CUP", description=f"{cricket_p1.mention} Four ⚔ Four {cricket_p2.mention}", color=0xffff00)
        myEmbed.add_field(name="Score:", value=f"{cricket_p1.mention}:{score1}/{wickets1}:{cricket_p2.mention} in {length1} balls", inline=True)
        myEmbed.set_thumbnail(url = "https://m.media-amazon.com/images/I/81tzdBv+89L._SY450_.jpg")
        myEmbed.set_author(name="CCC Utilities#6430")
        await ctx.send(embed=myEmbed)
        runs1 = "" 
        balls1 = ""
        await asyncio.sleep(3)
        await pointcount(ctx)
    elif runs1 == "Six" and balls1 == "Six":
        wickets1 +=1
        score1 -=6
        length1+=1
        myEmbed = nextcord.Embed(title = "ICC WORLD CUP", description=f"{cricket_p1.mention} Six ⚔ Six {cricket_p2.mention}", color=0xffff00)
        myEmbed.add_field(name="Score:", value=f"{cricket_p1.mention}:{score1}/{wickets1}:{cricket_p2.mention} in {length1} balls", inline=True)
        myEmbed.set_thumbnail(url = "https://m.media-amazon.com/images/I/81tzdBv+89L._SY450_.jpg")
        myEmbed.set_author(name="CCC Utilities#6430")
        await ctx.send(embed=myEmbed)
        runs1 = "" 
        balls1 = ""
        await asyncio.sleep(3)
        await pointcount(ctx)
    elif balls1 == "":
        length1+=1
        myEmbed = nextcord.Embed(title = "ICC WORLD CUP", description=f"{cricket_p1.mention} {runs1} ⚔ Did not respond! {cricket_p2.mention}", color=0xffff00)
        myEmbed.add_field(name="Score:", value=f"{cricket_p1.mention}:{score1}/{wickets1}:{cricket_p2.mention} in {length1} balls", inline=True)
        myEmbed.set_author(name="CCC Utilities#6430")
        await ctx.send(embed=myEmbed)
        runs1 = "" 
        balls1 = ""
        await asyncio.sleep(3)
        await pointcount(ctx)
    elif runs1 != balls1:
        length1+=1
        myEmbed = nextcord.Embed(title = "ICC WORLD CUP", description=f"{cricket_p1.mention} {runs1} ⚔ {balls1} {cricket_p2.mention}", color=0xffff00)
        myEmbed.add_field(name="Score:", value=f"{cricket_p1.mention}:{score1}/{wickets1}:{cricket_p2.mention} in {length1} balls", inline=True)
        myEmbed.set_author(name="CCC Utilities#6430")
        await ctx.send(embed=myEmbed)
        runs1 = "" 
        balls1 = ""
        await asyncio.sleep(3)
        await pointcount(ctx)
        
async def pointcount(ctx):
    global wickets1
    global length1
    global score1
    global cricket_p1
    global cricket_p2
    global target
    global gameOver
    
    if ing1==False:
        if wickets1==3 or length1==10 :
            score1+=1
            myEmbed = nextcord.Embed(title = "ICC WORLD CUP", description=f"Innings One has come to an end!", color=0xffff00)
            myEmbed.add_field(name="Innings 1 Score:", value=f"{cricket_p1.mention}:{score1-1}/{wickets1}:{cricket_p2.mention}\n{length1} balls", inline=True)
            myEmbed.add_field(name="Innings 2 on the Way!", value=f"{cricket_p2.mention} will bat now!\n{cricket_p1.mention} will ball now!")
            myEmbed.add_field(name="Target!", value=f"{cricket_p2.mention} have to score {score1} in 10 balls with 3 wickets in hands!\nCan they do it??")
            myEmbed.set_thumbnail(url = "https://thefederal.com/wp-content/uploads/2020/05/ICC-T20-World-Cup-2020-Trophy-696x387.jpg")
            myEmbed.set_author(name="CCC Utilities#6430")
            await ctx.send(embed=myEmbed)
            await intchange(ctx)
        else:
            await play(ctx)
            
    elif ing1 == True:
        if wickets1>=3 or length1>=10 :
            myEmbed = nextcord.Embed(title = "ICC WORLD CUP", description=f"Innings Two has come to an end!", color=0xffff00)
            myEmbed.add_field(name="Innings 2 Score:", value=f"{cricket_p1.mention}:{score1}/{wickets1}:{cricket_p2.mention}\n{length1} balls", inline=True)
            myEmbed.add_field(name="Winner!", value=f"{cricket_p2.mention} defends bravely as {cricket_p1.mention} falls short to chase the target", inline=False)
            myEmbed.set_author(name="CCC Utilities#6430")
            await ctx.send(embed=myEmbed)
            gameOver = True
        elif target <= score1:
            myEmbed = nextcord.Embed(title = "ICC WORLD CUP", description=f"Innings Two come to an end!", color=0xffff00)
            myEmbed.add_field(name="Innings 2 Score:", value=f"{cricket_p1.mention}:{score1}/{wickets1}:{cricket_p2.mention}\n{length1} balls", inline=True)
            myEmbed.add_field(name="Winner!", value=f"{cricket_p1.mention} beat the crap out of {cricket_p2.mention} as they finish off in style!", inline=True)
            myEmbed.set_author(name="CCC Utilities#6430")
            await ctx.send(embed=myEmbed)
            gameOver = True
        else:
            await asyncio.sleep(3)
            await play(ctx)
        
async def intchange(ctx):
    global cricket_p1
    global cricket_p2
    global score1
    global score2
    global length1
    global length2
    global target
    global ing1
    global wickets1
    global wickets2
    wickets1 = wickets2
    cricket_p1,cricket_p2 = cricket_p2,cricket_p1
    target = score1
    score1 = score2
    length1 = length2
    ing1 = True
    await asyncio.sleep(5)
    await play(ctx)

@client.command()
async def endgame(ctx):
    global cricket_p1
    global cricket_p2 
    global gameOver
    if ctx.author == cricket_p1 or ctx.author == cricket_p2:
        num =random.randint(1, 2)
        if num == 1:
            await ctx.reply(f"{cricket_p1.mention} Wins the Game By Random choice!")
        else:
            await ctx.reply(f"{cricket_p2.mention} Wins the Game By Random choice!")
        gameOver = True
        await ctx.reply("Game Over.\nYou may start a new one!")
    else:
        await ctx.reply(f"You can only end the game played by you!\nCurrently the game is being played between {cricket_p1.mention} and {cricket_p2.mention}")

@client.command()
async def crickethelp(ctx):
    myEmbed = nextcord.Embed(title = "ICC WORLD CUP", description=f"Here are the various commands and rules in order to play this game!", color=0xffff00)
    myEmbed.add_field(name="Commands:-", value=f"1.**&cricket [player1] [player2] ** which starts the game.\n2.**&endgame** ends the current game and crowns one as the winner(Inorder to use this command, you should be the one who is playing the game).", inline=True)
    myEmbed.add_field(name="Rules:-", value=f"1.Both players should press the button only once.\n2.The one who will bat first will always get the message as interaction failed but don't worry as the response is noted.\n3.Both players should press the button within 5 seconds.\n4.If the bot gets stuck it may be an internal error and you may end the game and restart a new one.\n5.**Enjoy and have a Good Time!**", inline=False)
    myEmbed.set_author(name="CCC Utilities#6430")
    await ctx.reply(embed=myEmbed)
    
@client.command()
async def tictactoe(ctx, p1 : nextcord.Member, p2 : nextcord.Member ):
    global player1
    global player2
    global turn
    global gameOver
    global count
    global tic_time
    
    if gameOver and p1 != await client.fetch_user(975623272496529408) and p2 != await client.fetch_user(975623272496529408):
        await tictactoeplay(ctx,p1,p2)
    elif p1 == await client.fetch_user(975623272496529408) or p2 == await client.fetch_user(975623272496529408):
        await ctx.reply("You cannot play with the Bot itself!")
    else:
        await ctx.reply("A game is already in progress! \n Finish it before starting a new one!")
        
async def tictactoeplay(ctx,p1,p2):        
        global player1
        global player2
        global turn
        global gameOver
        global count
        global tic_time
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0
        player1 = p1
        player2 = p2
        #print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]
                
        #determines who goes first!
        num =random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send(f"It is {player1.mention} turn!")
        elif num == 2:
            turn = player2
            await ctx.send(f"It is {player2.mention} turn!")
            
        #calculates time
        tic_time=0
        while True:
            if gameOver == False:
                await asyncio.sleep(1)
                tic_time+=1
            else:
                break
                   
@client.command()
async def place(ctx, pos : int):
    global turn
    global board
    global count
    global player1 
    global player2
    global gameOver
    global tic_time
    
    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0<pos<10 and board[pos - 1] == ":white_large_square:":
                board[pos-1] = mark
                count+=1
                
                #print board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]
                
                checkWinner(winningConditions, mark)
                if gameOver == True:
                    await asyncio.sleep(2)
                    if mark == ":regional_indicator_x:":
                        myEmbed = nextcord.Embed(title="TICTACTOE❌⭕", description=f"{player1.mention} :regional_indicator_x: Wins the Game!", color=0xffff00)
                        myEmbed.add_field(name="Game Stats!", value=f"Time taken:{tic_time} seconds\n Total Moves:{count}",inline = True)
                        myEmbed.set_author(name="CCC Utilities#6430")
                        await ctx.send(embed=myEmbed)
                        await playagain(ctx)
                    elif mark == ":o2:":
                        myEmbed = nextcord.Embed(title="TICTACTOE❌⭕", description=f"{player2.mention} :o2: Wins the Game in just {count} moves!", color=0xffff00)
                        myEmbed.add_field(name="Game Stats!", value=f"Time taken:{tic_time} seconds\n Total Moves:{count}",inline = True)
                        myEmbed.set_author(name="CCC Utilities#6430")
                        await ctx.send(embed=myEmbed)
                        await playagain(ctx)
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")
                    await playagain(ctx)
                
                
                #switch turns
                if turn == player1: 
                    turn = player2
                elif turn == player2:
                    turn = player1
                
            else:
                await ctx.reply("Be sure to change an integer between 1 and 9 and an unmarked tile!")
        else:
            await ctx.reply("It is not you turn!")
    else:
        await ctx.reply("Please start a new game!")

async def playagain(ctx):
    global player1
    global player2
    global kli
    kli=0
    button = Button(label="Yes", style = nextcord.ButtonStyle.green, emoji="👍")
    view = View(timeout=10)
    view.add_item(button)
    async def button_callback(interaction):
        global kli
        kli+=1
    button.callback = button_callback
    await ctx.send("Would like to play the game again with same player?",view=view)
    await asyncio.sleep(10)
    await check_rsp(ctx)

async def check_rsp(ctx):
    global kli
    global player1
    global player2
    if kli >= 2:
        p1=player1
        p2=player2
        await ctx.send(f"Starting a new game again between {p1.mention} and {p2.mention}")
        await tictactoeplay(ctx,p1,p2)
    else:
        await ctx.send("Game Request Rejected!")
        
@client.command()
async def clear(ctx):
    global player1
    global player2
    global gameOver
    if ctx.author == player1 or ctx.author == player2:
        num =random.randint(1, 2)
        if num == 1:
            await ctx.reply(f"{player1.mention} Wins the Game By Random choice")
        else:
            await ctx.reply(f"{player2.mention} Wins the Game By Random choice")
        gameOver = True
        await ctx.reply("Game Over!")
    else:
        await ctx.reply("You can only end the game played by you!")
            
def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@client.command()
async def tictactoehelp(ctx):
    myEmbed = nextcord.Embed(title = "TICTACTOE⭕❌", description=f"Here are the various commands and rules in order to play this game!", color=0xffff00)
    myEmbed.add_field(name="Commands:-", value=f"1.**&tictactoe [player1] [player2] ** which starts the game.\n2.**&clear** ends the current game and crowns one as the winner(Inorder to use this command, you should be the one who is playing the game).\n3.**&place [number between 1 to 9]** Marks the your tile in the board!", inline=True)
    myEmbed.set_author(name="CCC Utilities#6430")
    await ctx.reply(embed=myEmbed)
    
client.run("********BOT-TOKEN*********")
