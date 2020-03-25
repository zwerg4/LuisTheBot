import discord, flask_server
import math
import os
from itertools import combinations
from discord.ext import commands
from flask_server import keep_alive

bot = commands.Bot(command_prefix='-', description='best BOT EUW !')

likereactions = ['👍','👎']
pollreactions = ['👍','👎']
gayreactions = ['🇮','🇲','🇬', '🇦', '🇾']
gaycandidates = [336588827760132096, 336953197924974595, 337258187751161857, 349635204106944514, 233677953463091200, 280329030715310080, 336574818826715138, 188286395238973440]


anzahl_gruppen = 0
gruppen_namen = []
gruppen_punkte = []
spiele = []
runde = 0
max_runde = 0
runden_gleichzeitig = 0



##EVENTS##
@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="watten.org"))
  print("--- LUISTHEBOT started successfully ---")

##COMMANDS##

@bot.command()
async def ping(ctx):
    """| Pong!"""
    await ctx.send("Pong!")

@bot.command()
async def like(ctx):
    """| questions if you like the Server"""
    sendmsg = await ctx.send("Do you like this Server? ")
    for emoji in likereactions:
      await sendmsg.add_reaction(emoji)

@bot.command()
async def poll(ctx, poll_message):
    """| Start a poll | usage: !poll (message you want to ask)"""
    if poll_message is not None:
      sendpollmsg = await ctx.send(f"{ctx.author} started a poll: {poll_message}")
      for emoji in pollreactions:
        await sendpollmsg.add_reaction(emoji)
    else:
      await ctx.send("usage: !poll (message you want to ask)")
      return


@bot.command()
async def watten(ctx, befehl, *args):
    """| WATTEN HELPER | usage: !watten"""
    global anzahl_gruppen
    global gruppen_namen
    global gruppen_punkte
    global runde
    global max_runde
    global spiele
    global runden_gleichzeitig
    if befehl == "teamadd":
      if len(args) == 1 :
        anzahl_gruppen += 1
        gruppen_namen.append(args[0])
        gruppen_punkte.append(0)
        await ctx.send("Neue Gruppe " + gruppen_namen[-1] + ": WICHTIG!! GRUPPENNUMMER >> " + str(anzahl_gruppen) + " <<")
        return
      else:
        await ctx.send("befehl: -watten teamadd <teamname>")
        return
      
    if befehl == "ergebnis":
      if len(args):
        if int(args[2]) > int(args[3]):
          gruppen_punkte[int(args[0]) - 1] += 1
          await ctx.send("G"+ str(args) + ":"+ gruppen_namen[int(args[0])- 1]+" wurde als Gewinner eingetragen! Good Job")
        if int(args[2]) < int(args[3]): 
          gruppen_punkte[int(args[1]) - 1] += 1
          await ctx.send("G"+ str(args[1]) + ":"+ gruppen_namen[int(args[1]) - 1]+" wurde als Gewinner eingetragen! Good Job")
      else:
        await ctx.send("befehl: -watten ergebnis <Nr. Gr 1> <Nr. Gr 2> <Punkte Gr 1> <Punkte Gr 2>")
        return

    if befehl == "start":
      ls = list(range(1,anzahl_gruppen+1))
      print(ls)
      spiele = list(combinations(ls, 2))
      print(spiele)
    
      runde += 1
      max_runde = math.floor(anzahl_gruppen / 2)
      runden_gleichzeitig = anzahl_gruppen / max_runde
      await ctx.send("-- RUNDE " + str(runde) + " ---")
      for i in range(0,int(runden_gleichzeitig)):
        await ctx.send("** " +  gruppen_namen[spiele[i][0]] + " : " + gruppen_namen[spiele[i][1]])
      return

    if befehl == "next":
      runde += 1
      await ctx.send("-- RUNDE " + str(runde) + " ---")
      for i in range(0,int(runden_gleichzeitig)):
        await ctx.send("** " +  gruppen_namen[spiele[i * runde][0]] + " : " + gruppen_namen[spiele[i * runde][1]])
      return

    if befehl == "reset":
      anzahl_gruppen = 0
      gruppen_namen = []
      gruppen_punkte = []
      await ctx.send("Spiel und Gruppen wurden zurückgesetzt!")
      return

    if befehl == "neuesspiel":
      for i in range(0,anzahl_gruppen):
        gruppen_punkte[i] = 0
        await ctx.send("Spiel wurden zurückgesetzt!")
      return

    if befehl == "tabelle":
      await ctx.send("------- PUNKTE -------")
      for i in range(0,anzahl_gruppen):
        await ctx.send("Gr[" + str(i + 1) + "] " + gruppen_namen[i] + " Punkte: " + str(gruppen_punkte[i]))
      return

    if befehl == "help":
      await ctx.send("commands:\n-watten\n   -help\n   -teamadd <teamname>\n   -ergebnis <Nr. Gr 1> <Nr. Gr 2> <Punkte Gr 1> <Punkte Gr 2>\n   -start\n   -tabelle\n   -reset\n   -neuesspiel\n")
      return

  


@bot.command()
async def test(ctx):
    await ctx.send("something")
token = os.environ.get("DISCORD_BOT_SECRET")
keep_alive()
bot.run(token)

