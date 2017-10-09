import discord
import asyncio
import copy

from random import randint

#### Global variables ###
client = discord.Client()
cmdPrefix = '^'

inDungeon = [] #List of user (ids) playing dungeons
roomNumber = {} #Dict - id:floor
currentRoom = {} #Dict - id:layout (2d array/list)
currentPos = {} # Dict id: (list - x,y)
currentMessage = {} #Dict - id:messageId (to update/edit later)
#########################

### Methods ###

#Generates a sometimes-random size room based on floor number
def genRoom(roomNumber, authorId, shop = False):
    room = []
    size = 0
    
    if not shop:
        if roomNumber == 0:
            size = 15
        #elif roomNumber < 5:

        ySize = randint(size / 3, size)
        xSize = randint(size / 3, size)

        room.append(list('#' * (xSize + 2)))
        for y in range(ySize):
            room.append(list('#' + ('_' * xSize) + '#'))
        room.append(list('#' * (xSize + 2)))

        currentPos[authorId] = [randint(1, ySize), randint(1, xSize)]
    else:
        size = 100 #idk

    currentRoom[authorId] = room

#Gets the users room as a string (to send as message)
def getRoomMessage(authorId):
    room = copy.deepcopy(currentRoom[authorId])

    room[currentPos[authorId][0]][currentPos[authorId][1]] = '@'
    
    s = '```'
    for i in range(len(room)):
        s = (s + '\n') + ''.join(room[i])

    s += '\n```'

    return s

#Sends the room to the user and updates the active map message
async def sendRoom(channel, authorId):
    room = getRoomMessage(authorId)

    if authorId in currentMessage:
        await client.delete_message(currentMessage[authorId])
        
    currentMessage[authorId] = await client.send_message(channel, '<@' + authorId + '>\'s current map:\n' + room)

#Updates map message
async def updateRoom(authorId):
    await client.edit_message(currentMessage[authorId], new_content = ('<@' + authorId + '>\'s current map:\n' + getRoomMessage(authorId)))

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
                inDungeon.remove(authorId)
                await client.send_message(message.channel, '<@' + authorId + '>: Quit game of Dungeons')
                await client.delete_message(currentMessage[authorId])
                del currentMessage[authorId]
            elif content.startswith('check'):
                await sendRoom(message.channel, authorId)
            elif content.startswith('help'):
                s =  '```\n'
                s += 'Help for DUNGEONS\n\n'
                s += 'Commands:\n'
                s += '   help - Sends this message\n'
                s += '   quit - Quits game (Note: game NOT saved)\n'
                s += '   check - Outputs your current map\n'
                s += '\n'

                s += 'Interactive Commands:\n'
                s += '> When used, these commands will update the game and then your message will be deleted (sometimes, I\'m working on it)<\n'
                s += '   w,a,s,d - move your character a direction\n'
                s += '   up,left,down,right - aliases for w,a,s,d\n'
                s += '\n'

                s += 'Note: No commands require a prefix when playing dungeons\n\n'

                s += 'Map Icons:\n'
                s += '   # - Wall\n'
                s += '   _ - Floor / empty space\n'
                s += '   @ - You!\n'

                s += '```'
                await client.send_message(message.channel, s)

            elif content.startswith('w') or content.startswith('up'):
                if currentPos[authorId][0] > 1:
                    currentPos[authorId][0] -= 1
                await client.delete_message(message)
                await updateRoom(authorId)
            elif content.startswith('a') or content.startswith('left'):
                if currentPos[authorId][1] > 1:
                    currentPos[authorId][1] -= 1
                await client.delete_message(message)
                await updateRoom(authorId)
            elif content.startswith('s') or content.startswith('down'):
                if currentPos[authorId][0] < len(currentRoom[authorId]) - 2:
                    currentPos[authorId][0] += 1
                await client.delete_message(message)
                await updateRoom(authorId)
            elif content.startswith('d') or content.startswith('right'):
                if currentPos[authorId][1] < len(currentRoom[authorId][0]) - 2:
                    currentPos[authorId][1] += 1
                await client.delete_message(message)
                await updateRoom(authorId)
                
        elif message.content.startswith(cmdPrefix):
            content = message.content[1:]

            if content.startswith('help'):
                s =  '```\n'
                s += 'Bot Commands:\n'


                
                s += '```'
                await client.send_message(message.channel, s)
            elif content.startswith('url') or content.startswith('invite'):
                await client.send_message(message.channel, 'https://discordapp.com/oauth2/authorize?client_id=258031474404491265&scope=bot&permissions=36793353')
            elif content.startswith('dungeons'):
                await client.send_message(message.channel, "Welcome to DUNGEONS!\n\n Dungeons is a top down, turn based rpg!\n\nType 'help' at any time to check available commands.\nYou can also type 'quit' to exit the game.")
                inDungeon.append(authorId)
                roomNumber[authorId] = 0
                genRoom(0, authorId)

                await sendRoom(message.channel, authorId)
            elif content.startswith('resume'):
                inDungeon.append(authorId)
                                
'''
@client.event
async def on_message_delete(message):
    await client.send_message(message.channel, '<@' + message.author.id + '> deleted the message: "' + message.content + '"')
'''
###############


#Run client
client.run('MjU4MDMxNDc0NDA0NDkxMjY1.DLaHmA.lhIzwxq4aeHtOe1llCeZ2BluOdA')
