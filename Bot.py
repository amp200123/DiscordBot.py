import discord
import asyncio

from random import randint

#### Global variables ###
client = discord.Client()
cmdPrefix = '^'

inDungeon = {}
roomNumber = {}
currentRoom = {}
currentMessage = {}
#########################

### Methods ###

def genRoom(roomNumber, shop = False):
    room = []
    size = 0
    
    if not shop:
        if roomNumber == 0:
            size = 21
        #elif roomNumber < 5:

        ySize = randint(size / 3, size)
        xSize = randint(size / 3, size)

        room.append(list('#' * (xSize + 2)))
        for y in range(ySize):
            room.append(list('#' + ('_' * xSize) + '#'))
        room.append(list('#' * (xSize + 2)))
    else:
        size = 100 #idk

    return room

async def sendRoom(channel, authorId):
    room = currentRoom[authorId]
    s = '```'
    for i in range(len(room)):
        s = (s + '\n') + ''.join(room[i])

    s += '\n```'
    
    currentMessage[authorId] = await client.send_message(channel, '<@' + authorId + '>\'s current map:\n' + s)

###############


### Events ###
@client.event
async def on_ready():
	print('Ready!')

@client.event
async def on_message(message):
    if message.author != client.user:
        content = message.content
        authorId = message.author.id
        
        if inDungeon:
            if content.startswith('quit'):
                inDungeon[authorId] = False
                await client.send_message(message.channel, '<@' + authorId + '>: Quit game of Dungeons')
            elif content.startswith('check'):
                await sendRoom(message.channel, authorId)
            elif content.startswith('help'):
                s = '```\n'
                s += 'Commands:\n'
                s += '   help - Sends this message\n'
                s += '   quit - Quits game (Note: game NOT saved)\n'
                s += '   check - Outputs your current map\n'

                s += 'Interactive Commands:
                s += ' > When used, these commands will update the game and then your message will be deleted <
                s += '   '

                s += 'Map Icons:\n'
                s += '   # - Wall\n'
                s += '   _ - Floor / empty space\n'
                s += '   @ - You!\n'

                s += '```'
                await client.send_message(message.channel, s)
                
        elif message.content.startswith(cmdPrefix):
            content = message.content[1:]

            if content.startswith('printText'):
                print(message.content)
            elif content.startswith('dungeons'):
                await client.send_message(message.channel, "Welcome to DUNGEONS!\n\n Dungeons is a top down, turn based rpg!\n\nType 'help' at any time to check available commands.\nYou can also type 'quit' to exit the game.")
                inDungeon[authorId] = True
                roomNumber[authorId] = 0
                currentRoom[authorId] = genRoom(0)

                await sendRoom(message.channel, authorId)
                                
'''
@client.event
async def on_message_delete(message):
    await client.send_message(message.channel, '<@' + message.author.id + '> deleted the message: "' + message.content + '"')
'''
###############


#Run client
client.run('MjU4MDMxNDc0NDA0NDkxMjY1.DLaHmA.lhIzwxq4aeHtOe1llCeZ2BluOdA')
