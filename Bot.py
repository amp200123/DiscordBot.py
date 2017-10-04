import discord
import asyncio

from random import randint

#### Global variables ###
client = discord.Client()
cmdPrefix = '^'

inDungeon = []
roomNumber = {}
currentRoom = {}
#########################

### Methods ###

def genRoom(roomNumber, shop = False):
    room = []
    size = 0
    
    if not shop:
        if roomRumber == 0:
            size = 21
        #elif roomNumber < 5:

        ySize = randint(size / 3, size)
        zSize = randint(size / 3, size)

        room.append(list('#' * xSize))
        for y in range(ySize):
            room.append([])
            for x in range(xSize):
                room[y] += '#' + ('_' * xSize) + '#'
        room.append(list('#' * xSize))
    else:
        size = 100 #idk

    return room

def sendRoom(channel, room):
    s = '```'
    for i in range(len(room)):
        (s + '\n').join(room[i])

    s += '\n```'
    
    await client.send_message(channel, s)

###############


### Events ###
@client.event
async def on_ready():
	print('Ready!')

@client.event
async def on_message(message):
    if message.author != client.user:
        content = message.content
        
        if inDungeon:
            if content.startswith('quit'):
                inDungeon[message.author.id] = False
            elif content.startswith('check'):
                sendRoom(message.channel, currentRoom[message.author.id])
        elif message.content.startswith(cmdPrefix):
            content = message.content[1:]

            if content.startswith('printText'):
                print(message.content)
            elif content.startswith('dungeons'):
                await client.send_message("Welcome to DUNGEONS!\n\n Dungeons is a top down turn based rpg\nType 'help' at any time to check availible commands. You cna also type 'quit' to exit the game.")
                inDungeon[message.author.id] = True
                roomNumber[message.author.id] = 0
                currentRoom[message.author.id] = genRoom(0)
                
                
'''
@client.event
async def on_message_delete(message):
    await client.send_message(message.channel, '<@' + message.author.id + '> deleted the message: "' + message.content + '"')
'''
###############


#Run client
client.run('MjU4MDMxNDc0NDA0NDkxMjY1.DLaHmA.lhIzwxq4aeHtOe1llCeZ2BluOdA')
