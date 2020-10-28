import discord
from discord.ext.commands import Bot
from discord.ext import tasks, commands
from discord.ext import commands
import asyncio
import time
import pickle
from datetime import datetime, timedelta
import random

Client = discord.Client()
client = commands.Bot(command_prefix = ";")

firstItems = {}

global queue
queue = []

global queueGoing
queueGoing = "false"

global maxQueueTime
maxQueueTime = 1

global QueueTime

global TimeQueued

global Channel

global FirstTime

global lastQueue
lastQueue = []

global LastQueue
LastQueue = ""

global GameMode
GameMode = "Captains Draft"

global Traps
Traps = ["trap.jpg", "trap2.jpg", "trap3.jpg", "trap4.jpg", "trap5.png", "trap7.jpg", "trap8.png"]

global S
S = ["s1.jpg", "s2.jpg", "s3.jpg", "s4.jpg", "s5.jpg", "s6.jpg", "s7.png"]

global Season
Season = ["season1.jpg", "season2.jpg", "season3.jpg", "season4.jpg"]

global Loli
Loli = ["loli1.png", "loli2.png", "loli3.jpg", "loli4.jpg", "loli5.jpg", "loli6.png", "loli7.png", "loli8.png", "loli9.jpg", "loli10.jpg", "loli11.jpg", "loli12.png", "loli13.jpg", "loli14.png", "loli15.jpg", "loli16.jpg", "loli17.jpg", "loli18.jpg"]

global Nou
Nou = ["nou1.png", "nou2.png", "nou3.jpeg", "nou4.png", "nou5.jpg", "nou6.png", "nou7.jpg", "nou8.png"]

global Cuddle
Cuddle = ["cuddle.gif", "cuddle2.gif", "cuddle3.gif", "cuddle4.gif", "cuddle5.gif", "cuddle6.gif", "cuddle7.gif", "cuddle8.gif", "cuddle9.gif", "cuddle10.gif", "cuddle11.gif"]

global LastShank
LastShank = ("", 0)

global Shivs
Shivs = dict.fromkeys(firstItems)

global Jail
Jail = dict.fromkeys(firstItems)

global MMRTable
MMRTable = dict.fromkeys(firstItems)

with open("MaxTime", "rb") as time_int:
    maxQueueTime = pickle.load(time_int)

with open("Shivs", "rb") as shivs_in:
    Shivs = pickle.load(shivs_in)

with open("MMRTable", "rb") as in_file:
    MMRTable = pickle.load(in_file)

with open("Jail", "rb") as in_jail:
    Jail = pickle.load(in_jail)

QueueTime = maxQueueTime

global stream
stream = discord.Streaming(name=GameMode + " - (0/10)", url="https://twitch.tv/Batsphemy")

@tasks.loop(seconds=30.0)
async def checkTime():
    global queueGoing
    global maxQueueTime
    global TimeQueued
    global QueueTime
    global Channel
    global queue
    global GameMode

    if queueGoing == "true":
        start = TimeQueued
        end = datetime.utcnow()
        diff = end - start

        if diff.seconds / 60 >= QueueTime:
            mess = ""
            for player in queue:
                mess += player.mention + " "
            await Channel.send("Queue has been cleared due to a lack of players. Please try again later. \n" + mess)
            await client.change_presence(activity=stream)
            queue = []
            queueGoing = "false"
            QueueTime = maxQueueTime


@client.event
async def on_ready():
    print("Ready to Queue!")
    checkTime.start()

    global GameMode
    await client.change_presence(activity=stream)


@client.event
async def on_message(message):

    global queue
    global queueGoing
    global QueueTime
    global maxQueueTime
    global TimeQueued
    global Channel
    global LastQueue
    global FirstTime
    global GameMode
    global lastQueue
    global sinceQueue
    global LastShank
    global Shivs

    if message.author == client.user:
        return

    newStream = stream
    newStream.name = GameMode + " - (" + str(len(queue)) + "/10)"
    await client.change_presence(activity=newStream)

    args = message.content.split(" ")

    if "JEFF" in message.content.upper() or "<@143799702289121280>" in message.content.upper() or "<@!143799702289121280>" in message.content.upper():
        await message.add_reaction("🍆")

    if args[0].upper() == ";SHANK":
        if message.author.id == 217140657347756033:
            await message.channel.send(":dagger: " + args[1])
        elif message.author.id not in Shivs.keys() or Shivs[message.author.id] < 1:
            await message.channel.send("You don't have any shivs. Ask Nibbles for some!")
        else:
            m = ""
            if LastShank[0] == args[1]:
                if LastShank[1] == 0:
                    m = "Double Kill!"
                elif LastShank[1] == 1:
                    m = "Triple Kill!"
                elif LastShank[1] == 2:
                    m = "Ultra Kill!"
                elif LastShank[1] >= 3:
                    m = "RAMPAGE!"
                LastShank = (LastShank[0], LastShank[1] + 1)
            else:
                LastShank = (args[1], 0)
            await message.channel.send(":dagger: " + args[1] + " " + m)
            Shivs[message.author.id] -= 1
            with open("Shivs", "wb") as shivs_out:
                pickle.dump(Shivs, shivs_out)

    if (args[0].upper() == ";GIVESHIV" and message.author.id == 217140657347756033) or (args[0].upper() == ";GIVESHIV" and message.author.id == 260843280361586688):

        try:
            id = args[1][2:-1]
            if id.startswith('!'):
                id = id[1:]
            x = int(args[2])
            print (Shivs)
            if str(id) in Shivs.keys():
                Shivs[str(id)] = Shivs[str(id)] + x
            else:
                Shivs[str(id)] = x
            with open("Shivs", "wb") as shivs_out:
                pickle.dump(Shivs, shivs_out)
        except:
            await message.channel.send("Dear lord Nibbles. Please provide an integer as shiv amount :)")

    if (args[0].upper() == ";TAKESHIV" and message.author.id == 217140657347756033) or (args[0].upper() == ";TAKESHIV" and message.author.id == 260843280361586688):
        try:
            id = args[1][2:-1]
            if id.startswith('!'):
                id = id[1:]
            x = int(args[2])
            if str(id) in Shivs.keys():
                newShivs = Shivs[str(id)] - x
                if newShivs < 0:
                    newShivs = 0
                Shivs[str(id)] = newShivs
            else:
                await message.channel.send("User " + args[1] + " is not in the Shivlist yet!")
        except:
            await message.channel.send("Dear lord Nibbles. Please provide an integer as shiv amount :)")

    if args[0].upper() == ";SHIVS":
        x = 0
        if message.author.id in Shivs:
            x = str(Shivs[message.author.id])
        if message.author.id == "217140657347756033":
            await message.channel.send("The human shank doesn't need shivs. He IS the shiv!")
        else:
            await message.channel.send("You have **" + str(x) + "** shivs!")


    if message.channel.id == 447862327866425344:
        if message.content.upper() == "EL PSY CONGROO":
            print("Mayushii-des!")
            await message.channel.send(file=discord.File("congroo.jpg"))

        if message.content.upper() == "TUTURUU" or message.content.upper() == "TUTURU":
            await message.channel.send(file=discord.File("mayushii.jpeg"))

        if message.content.upper() == "TRAP" or message.content.upper() == "ITS A TRAP" or message.content.upper() == "IT'S A TRAP":
            await message.channel.send(file=discord.File(random.choice(Traps)))

        if message.content.upper() == "AYY":
            await message.channel.send("Lmao")

        if message.content.upper() == "OMEGALOLI":
            await message.channel.send(file=discord.File("baconz.png"))

        if message.content.upper() == "KAMEHAME":
            await message.channel.send("HAAAAAAAAAAAAAAAAAAAAAAAAAA!!!!")

        if message.content.upper() == "NOBULLY":
            await message.channel.send(file=discord.File("nobully.gif"))

        if message.content.upper() == "NONOBULLY":
            await message.channel.send(file=discord.File("nonobully.jpg"))

        if message.content.upper() == "OMAE WA MOU SHINDEIRU":
            await message.channel.send(file=discord.File("Nani.gif"))

        if message.content.upper() == "SMILE" or message.content.upper() == "SWEET" or message.content.upper() == "SISTER" or message.content.upper() == "SADISTIC" or message.content.upper() == "SURPRISE":
            await message.channel.send(file=discord.File(random.choice(S)))

        if message.content.upper() == "SERVICE":
            await message.channel.send(file=discord.File(S[6]))

        if message.content.upper() == "NARUTO" or message.content.upper() == "NARUTOO" or message.content.upper() == "NARUTOOO":
            await message.channel.send(file=discord.File("sasuke.gif"))

        if message.content.upper() == "NEED SECOND SEASON":
            await message.channel.send(file=discord.File(random.choice(Season)))

        if message.content.upper() == "BAKA":
            await message.channel.send(file=discord.File("baka.jpg"))

        if message.content.upper().startswith("I CHOOSE YOU"):
            if message.content.upper().startswith("I CHOOSE YOU, SANDSLASH"):
                await message.channel.send("Pokémon Sprites/" + "28.png")
            elif message.content.upper().startswith("I CHOOSE YOU, LORD HELIX"):
                await message.channel.send("Pokémon Sprites/" + "139.png")
            elif message.content.upper() == "I CHOOSE YOU <@!419266806264496138>" or message.content.upper() == "I CHOOSE YOU <@419266806264496138>":
                await message.channel.send("Diancie.png")
            else:
                print(message.content)
                await message.channel.send(file=discord.File("Pokémon Sprites/" + str(random.randint(1, 386)) + ".png"))

        if message.content.upper() == "LOLI":
            await message.channel.send(file=discord.File(random.choice(Loli)))


    if args[0].upper() == ";QUEUE":
        if message.author not in queue:
            queue.append(message.author)

            if len(queue) == 1:
                FirstTime = datetime.utcnow()


            TimeQueued = datetime.utcnow()
            Channel = message.channel
            queueGoing = "true"

            players = ""
            for player in queue:
                players += player.name + "\n"

            await message.channel.send("Successfully queued! \n\n__Current Queue (" + str(len(queue)) + "/10): " + GameMode + "__ \n" + players)
            newStream = stream
            newStream.name = GameMode + " - (" + str(len(queue)) + "/10)"
            await client.change_presence(activity=newStream)

            playersInQueue = ""
            for player in queue:
                playersInQueue += player.name + " "
        else:
            await message.channel.send("You're already in the queue. To unqueue type ;unqueue")
        #else:
        #    await client.send_message(message.channel, "Your MMR isn't set. Contact an admin (Ancient Avocados role)")

        if len(queue) == 10:
            QueueTime = maxQueueTime

            mess = ""

            for player in queue:
                mess += player.mention + " "


            await message.channel.send("\nYour queue is ready!\nLobby name should be 'Defense of the Avocados' and password 'scccdota'.\nGame Mode = " + GameMode + "\n\n" + mess)
            logging = client.get_channel("490606042816708609")
            #await logging.send("\nYour queue is ready!\nLobby name should be 'Defense of the Avocados' and password 'scccdota'.\nGame Mode = " + GameMode + "\n\n" + mess)
            sinceQueue = datetime.utcnow()
            LastQueue = "Last full queue: " + playersInQueue
            queueGoing = "false"
            lastQueue = queue

            queue = []

            newStream = stream
            newStream.name = GameMode + " - (" + str(len(queue)) + "/10)"
            await client.change_presence(activity=newStream)

    if args[0].upper() == ";LIST":
        players = ""
        for player in queue:
            players += player.name + "\n"

        await message.channel.send("__Current Queue (" + str(int(len(queue))) + "/10): " + GameMode + "__ \n" + players)

    if args[0].upper() == ";LASTGAME":
        if LastQueue != "":
            if sinceQueue is not None:
                letime = datetime.utcnow() - sinceQueue
                messs = LastQueue  + ". Time since queue filled: " + str(int(letime.seconds / 60)) + " minutes."
                await message.channel.send(messs)

    if args[0].upper() == ";UNQUEUE":
        if message.author in queue:
            queue.remove(message.author)

            if len(queue) == 0:
                queueGoing = "false"
                if random.randint(1,20) == 20:
                    await message.channel.send("DeadHouse")

            await message.channel.send("Succesfully unqueued!")
            newStream = stream
            newStream.name = GameMode + " - (" + str(len(queue)) + "/10)"
            await client.change_presence(activity=newStream)
        else:
            await message.channel.send("You're not in the queue!")

    if args[0].upper() == ";CUDDLE":
        await message.channel.send(args[1])
        await message.channel.send(file=discord.File(random.choice(Cuddle)))

    if args[0].upper() == ";BALANCE":
        if len(lastQueue) < 10:
            await message.channel.send("Please only balance a full queue. :)")
            return

        mmr = []
        queueNames = []
        for i in range(10):
            print(i)
            try:
                id = lastQueue[i].id
                queueNames.append(lastQueue[i].name)
                print(id)
                mmr.append(MMRTable[str(id)])
            except:
                await message.channel.send(queueNames[i] + " doesn't have their mmr in the database, contact an admin.")
                return

        sorted_mmr = sorted(zip(mmr, queueNames), reverse = True)
        mmr, queueNames = map(list, (zip(*sorted_mmr)))

        team1 = []
        team2 = []

        mmr1 = 0
        mmr2 = 0

        team1.append(queueNames[0])
        mmr1 += mmr[0]
        team2.append(queueNames[1])
        mmr2 += mmr[1]
        team1.append(queueNames[9])
        mmr1 += mmr[9]
        team2.append(queueNames[8])
        mmr2 += mmr[8]

        if mmr1 > mmr2:
            team2.append(queueNames[2])
            mmr2 += mmr[2]
            team1.append(queueNames[3])
            mmr1 += mmr[3]
        else:
            team1.append(queueNames[2])
            mmr1 += mmr[2]
            team2.append(queueNames[3])
            mmr2 += mmr[3]

        if mmr1 > mmr2:
            team1.append(queueNames[7])
            mmr1 += mmr[7]
            team2.append(queueNames[6])
            mmr2 += mmr[6]
        else:
            team2.append(queueNames[7])
            mmr2 += mmr[7]
            team1.append(queueNames[6])
            mmr1 += mmr[6]

        if mmr1 > mmr2:
            team2.append(queueNames[4])
            mmr2 += mmr[4]
            team1.append(queueNames[5])
            mmr1 += mmr[5]
        else:
            team1.append(queueNames[4])
            mmr1 += mmr[4]
            team2.append(queueNames[5])
            mmr2 += mmr[5]

        #for i in range(2, 8, 2):
        #    if (((mmr1 / (max(len(team1), 1)))) <= ((mmr2 / (max(len(team2), 1)))) or len(team2) == 5) and len(team1) < 5:
        #        team1.append(queueNames[i])
        #        team2.append(queueNames[i + 1])
        #        print(team1)
        #        print(team2)
        #        mmr1 += mmr[i]
        #        mmr2 += mmr[i + 1]
        #    else:
        #        team2.append(queueNames[i])
        #        team1.append(queueNames[i + 1])
        #        mmr2 += mmr[i]
        #        mmr1 += mmr[i + 1]



        teamnames1 = ["Crispy", "Crusty", "Yellow", "Big", "Terrific", "Gorgeous", "Incredible", "Salty", "Toxic", "Angry", "Jeff's Huge"]
        teamnames2 = ["Bacons", "Baffoons", "Trolls", "Necropickers", "Maniacs", "Slardars", "Weebs", "Uncles", "D", "Grayons"]

        mess = ""
        mess += "__The " + random.choice(teamnames1) + " " + random.choice(teamnames2) + ":__\n"
        for player in team1:
            mess += "- " + player + "\n"
        mess += "*Average MMR: " + str(mmr1 / 5) + "*\n\n"

        mess += "__The " + random.choice(teamnames1) + " " + random.choice(teamnames2) + ":__\n"
        for player in team2:
            mess += "- " + player + "\n"
        mess += "*Average MMR: " + str(mmr2 / 5) + "*"

        await message.channel.send(mess)

    if message.author.id == "160493012298760192" and message.content.startswith("<@&467589310661525524> +6") and random.randint(1,20) == 20:
        await message.channel.send("https://cdn.discordapp.com/attachments/467592445660495882/503553136422682634/ry0ka_ping.png")

    roles = []

    for role in message.author.roles:
        roles.append(role.name)

    if "Ancient Avocados" in roles or message.author.id == "260843280361586688":

        if args[0].upper() == ";ARREST":

            player = args[1]
            id = player[2:-1]
            if id.startswith('!'):
                id = id[1:]

            if id == "260843280361586688":
                Jail[message.author.name] = "Trying to jail the Bat"
                await message.channel.send("Trying to jail the bat? Bold move. Now you're jailed! https://media.giphy.com/media/3rgXBA46zlHxBAPHva/giphy.gif")
            else:
                p = client.get_user(int(id))
                q = " ".join(args[2:])
                Jail[p.name] = q
                await message.channel.send("Arrested " + args[1] + "! https://media.giphy.com/media/3rgXBA46zlHxBAPHva/giphy.gif")
            with open("Jail", "wb") as out_jail:
                pickle.dump(Jail, out_jail)


        if args[0].upper() == ";JAIL":
            m = "```Current Jail: \n\n"
            for player in Jail:
                m += "{:<32}".format(player) + " " + Jail[player] + "\n"
            m += "```"
            await message.channel.send(m)

        if args[0].upper() == ";RELEASE":
            player = args[1]
            if player.upper() == "ALL":
                Jail.clear()
                with open("Jail", "wb") as out_jail:
                    pickle.dump(Jail, out_jail)
            else:
                id = player[2:-1]
                if id.startswith('!'):
                    id = id[1:]
                p = message.guild.get_member(int(id))

                rolesP = []

                for role in p.roles:
                    rolesP.append(role.name)

                if "he/him" in rolesP:
                    word = "boi"
                elif "she/her" in rolesP:
                    word = "gril"
                elif "they/them" in rolesP:
                    word = "thingymajigg"
                else:
                    word = "undefined"

                try:
                    Jail.pop(p.name)
                    with open("Jail", "wb") as out_jail:
                        pickle.dump(Jail, out_jail)
                    await message.channel.send(p.name + " has been released! Be good and stay out of trouble")
                except:
                    await message.channel.send(p.name + " is not in jail.")

        if args[0].upper() == ";CLEARQUEUE":
            queue = []
            await message.channel.send("Queue is cleared!")
            newStream = stream
            newStream.name = GameMode + " - (" + str(len(queue)) + "/10)"
            await client.change_presence(activity=newStream)
            queueGoing = "false"

        if args[0].upper() == ";SETMMR":
            player = args[1]
            try:
                id = player[2:-1]
                if id.startswith('!'):
                    id = id[1:]
                MMRTable[id] = int(args[2])
            except:
                await message.channel.send("Please provide the mmr as a number. ^.^")
            print(MMRTable)
            with open("MMRTable", "wb") as t:
                pickle.dump(MMRTable, t)
            await message.add_reaction("👍")

        #if args[0].upper() == ";CLEARMMR":
        #    MMRTable.clear()
        #    print(MMRTable)
        #    with open("MMRTable", "wb") as t:
        #        pickle.dump(MMRTable, t)

        if args[0].upper() == ";MMRLIST":
            #await message.channel.send("No crying in this server, tyvm.")
            return
            mess = "```"
            players = []
            mmrs = []
            for k,v in MMRTable.items():
                if k.startswith('!'):
                    k = k[1:]
                try:
                    u = client.get_user(int(k))
                    print(u.name)
                    if u is not None:
                        players.append(u.name.capitalize())
                        mmrs.append(str(v))
                    else:
                        print(k)
                except:
                    print(k + " is not a valid int!")

            sorted_players = sorted(zip(players, mmrs))
            players, mmrs = map(list, (zip(*sorted_players)))

            for i in range(0, len(players) / 3):
                m = players[i]
                mess += "{:<32}".format(m) + " " + mmrs[i] + "\n"

            mess += "```"

            await message.channel.send(mess)

            mess = "```"
            for i in range((len(players) / 3), len(players) / 3 + len(players) / 3):
                m = players[i]
                mess += "{:<32}".format(m) + " " + mmrs[i] + "\n"
            mess += "```"

            await message.channel.send(mess)

            mess = "```"
            for i in range(len(players) / 3 + len(players) / 3, len(players)):
                m = players[i]
                mess += "{:<32}".format(m) + " " + mmrs[i] + "\n"
            mess += "```"

            await message.channel.send(mess)

        if args[0].upper() == ";ADDTIME":
            QueueTime += int(args[1])
            await message.channel.send("Increased queue time by " + args[1] + " minutes")

        if args[0].upper() == ";REMOVEID":
            player = args[1]
            MMRTable.pop(player[2:-1])

        if args[0].upper() == ";SETGAMEMODE":
            mode = " ".join(args[1:])
            await message.channel.send("Set gamemode to: " + mode)
            newStream = stream
            newStream.name = GameMode + " - (" + str(len(queue)) + "/10)"
            await client.change_presence(activity=newStream)
            GameMode = mode

        if args[0].upper() == ";SETQUEUETIME":
            maxQueueTime = int(args[1])

            await message.channel.send("Max queue time set to: " + str(maxQueueTime) + " minutes.")

            with open("MaxTime", "wb") as qwetime:
                pickle.dump(maxQueueTime, qwetime)

client.run("---")
#steamClient.run_forever()

