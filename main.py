import discord #, flask_server
import math
import os
import random
from itertools import combinations
from discord.ext import commands
#from flask_server import keep_alive

bot = commands.Bot(command_prefix='-', description='best BOT EUW !')

likereactions = ['👍','👎']
pollreactions = ['👍','👎']
gayreactions = ['🇮','🇲','🇬', '🇦', '🇾']
#gaycandidates = [336588827760132096, 336953197924974595, 337258187751161857, 349635204106944514, 233677953463091200, 280329030715310080, 336574818826715138, 188286395238973440]


anzahl_gruppen = 0
gruppen_namen = []
gruppen_punkte = []
gruppen_punkte_gesamt = []
spiele = []
runde = 0
max_runde = 0
runden_gleichzeitig = 0
ls = []


def rotate(l, x):
  return l[-x:] + l[:-x]


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
    global gruppen_punkte_gesamt
    global runde
    global max_runde
    global spiele
    global runden_gleichzeitig
    global ls
    global rand_teams_bool
    global rand_users
    if befehl == "teamadd":
      if len(args) == 1 :
        anzahl_gruppen += 1
        gruppen_namen.append(args[0])
        gruppen_punkte_gesamt.append(0)
        gruppen_punkte.append(0)
        await ctx.send("Neue Gruppe **" + gruppen_namen[-1] + "**: WICHTIG!! GRUPPENNUMMER >> **" + str(anzahl_gruppen) + "** <<")
        return
      else:
        await ctx.send("befehl: -watten teamadd <teamname>")
        return

    if befehl == "test":
      anzahl_gruppen += 5
      gruppen_namen.append("DieOanser")
      gruppen_namen.append("DieZwoaer")
      gruppen_namen.append("DieDreier")
      gruppen_namen.append("DieVierer")
      gruppen_namen.append("DieFuenfer")
      gruppen_punkte.append(0)
      gruppen_punkte.append(0)
      gruppen_punkte.append(0)  
      gruppen_punkte.append(0)
      gruppen_punkte.append(0)
      gruppen_punkte_gesamt.append(0)
      gruppen_punkte_gesamt.append(0)
      gruppen_punkte_gesamt.append(0)
      gruppen_punkte_gesamt.append(0)
      gruppen_punkte_gesamt.append(0)
      await ctx.send("5 Test Teams hinzugefügt")


    if befehl == "ergebnis":
      if len(args):
        if int(args[2]) > int(args[3]):
          gruppen_punkte[int(args[0]) - 1] += 1
          await ctx.send("G"+ str(args) + ":"+ gruppen_namen[int(args[0])- 1]+" wurde als Gewinner eingetragen! Good Job")
        if int(args[2]) < int(args[3]): 
          gruppen_punkte[int(args[1]) - 1] += 1
          await ctx.send("G"+ str(args[1]) + ":"+ gruppen_namen[int(args[1]) - 1]+" wurde als Gewinner eingetragen! Good Job")
        gruppen_punkte_gesamt[int(args[0]) - 1] += int(args[2])
        gruppen_punkte_gesamt[int(args[1]) - 1] += int(args[3])
      else:
        await ctx.send("befehl: -watten ergebnis <Nr. Gr 1> <Nr. Gr 2> <Punkte Gr 1> <Punkte Gr 2>")
        return

    if befehl == "start":
      ls = list(range(1,anzahl_gruppen+1))
      if len(ls) % 2 != 0:
        ls.append(0)
      print(ls)
      runde += 1
      max_runde = math.floor(anzahl_gruppen / 2)
      runden_gleichzeitig = len(ls) / 2
      text = " -------- :shamrock: :heart:  **RUNDE " + str(runde) + " **  :chestnut: :new_moon: -------- \n"
      for counter in range(0,int(runden_gleichzeitig)):
        print("counter : "+ str(counter) + "len ln: " + str(len(ls)))
        if ls[counter] == 0:
          text += " ~ " +  gruppen_namen[ls[- 1 - counter] - 1] + " hat Spielfrei! \n"
          print(1)
        elif ls[-1 - counter] == 0:
          text += " ~ " +  gruppen_namen[ls[counter] - 1] + " hat Spielfrei! \n"
          print(2)
        else:
          text += " ~ " +  gruppen_namen[ls[counter] -1] + " : " + gruppen_namen[ls[-1 - counter] - 1] + "\n"
          print(3)
      await ctx.send(text)
      return  

    if befehl == "next":
      print(ls)
      runde += 1
      max_runde = math.floor(anzahl_gruppen / 2)
      ls.pop(0)
      print(ls)
      ls = rotate(ls,1)
      print(ls)
      ls2 = [1]
      ls2.extend(ls)
      print(ls2)
      runden_gleichzeitig = len(ls2) / 2
      text = " -------- :shamrock: :heart:  **RUNDE " + str(runde) + " **  :chestnut: :new_moon: -------- \n"
      for counter in range(0,int(runden_gleichzeitig)):
        print("counter : "+ str(counter) + "len ln: " + str(len(ls2)))
        if ls2[counter] == 0:
          text += " ~ " +  gruppen_namen[ls2[- 1 - counter] - 1] + " hat Spielfrei! \n"
          print(1)
        elif ls2[-1 - counter] == 0:
          text += " ~ " +  gruppen_namen[ls2[counter] - 1] + " hat Spielfrei! \n"
          print(2)
        else:
          text += " ~ " +  gruppen_namen[ls2[counter] -1] + " : " + gruppen_namen[ls2[-1 - counter] - 1] + "\n"
          print(3)
      await ctx.send(text)
      ls = ls2
      return  

    if befehl == "reset":
      anzahl_gruppen = 0
      gruppen_namen = []
      gruppen_punkte = []
      runde = 0
      await ctx.send("Spiel und Gruppen wurden zurückgesetzt!")
      return

    if befehl == "neuesspiel":
      for i in range(0,anzahl_gruppen):
        gruppen_punkte[i] = 0
        await ctx.send("Spiel wurden zurückgesetzt!")
      runde = 0
      return

    if befehl == "tabelle":
       text = " -------- :shamrock: :heart:  **PUNKTE " + str(runde) + " **  :chestnut: :new_moon: -------- \n"
       #    await ctx.send("------- PUNKTE -------")
       for i in range(0, anzahl_gruppen):
           text += "Gr[" + str(i + 1) + "] " + gruppen_namen[i] + " Punkte: " + str(gruppen_punkte[i]) + " / " + str(
              gruppen_punkte_gesamt[i]) + "\n"
       await ctx.send(text)
       #embed = discord.Embed(description=text, color=0x049323, )
       #await ctx.send(embed=embed)
       return

    if befehl == "randomteams":
        if len(args):
            print(args[0])
            if args[0] == "start":
                rand_teams_bool = True
                rand_users = []
                await ctx.send("Spielermeldung gestartet!! Melde dich mit **-watten join** an\n")
            elif args[0] == "end":
                if len(rand_users) % 2 == 0:
                    while len(rand_users) > 1:
                        # Using the randomly created indices, respective elements are popped out
                        r1 = random.randrange(0, len(rand_users))
                        elem1 = rand_users.pop(r1)
                        r2 = random.randrange(0, len(rand_users))
                        elem2 = rand_users.pop(r2)

                        anzahl_gruppen += 1
                        gruppen_namen.append(elem1[0:2]+elem2[0:2])
                        gruppen_punkte.append(0)
                        await ctx.send(discord.Embed(title="Teams: ",description='Team: ' + elem1[0:2]+elem2[0:2] + " | " +elem1[:-5]+ " + @"+elem2[:-5]+ "\n" , color=0xffffff))
                else:
                    await ctx.send("Es wird noch ein Spieler gebraucht um Teams zu machen\n")
            else:
                await ctx.send("-watten help for all commands!\n")
        else:
            await ctx.send("-watten help for all commands!\n")
        return

    if befehl == "join":
        if rand_teams_bool == True:
            await ctx.send("Spieler " + str(ctx.author) +" angemeldet\n")
            rand_users.append(str(ctx.author))
        return

    if befehl == "help":
      await ctx.send("*commands:*\n-watten\n   -help\n   -teamadd <teamname>\n   -ergebnis <Nr. Gr 1> <Nr. Gr 2> <Punkte Gr 1> <Punkte Gr 2>\n   -start\n   -tabelle\n   -reset\n   -neuesspiel\n")
      return

@bot.command()
async def test(ctx):
    await ctx.send("something")
#token = os.environ.get("DISCORD_BOT_SECRET")
bot.run("TOKEN")
#keep_alive()