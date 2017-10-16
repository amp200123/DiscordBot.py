import discord
import copy
import asyncio

from random import randint

class Dungeon:

    def __init___(self, authorId):
        self.active = True
        self.id = authorId
        
        self._messageId = None
        self._roomNumber = 0
        self._room = []
        self._playerPos = []

        self._genRoom()
        

    def __repr__(self):
        room = copy.deepcopy(self.room)
        
        room[self._playerPos[0]][self._playerPos[1]] = '@'

        s = '```'
        for i in range(len(room)):
            s = (s + '\n') + ''.join(room[i])

        s += '\n```'
        
        return s
        
    def _genRoom(self, shop = False):
        room = []
        size = 0
        
        if not shop:
            if self._roomNumber == 0:
                size = 15
            #elif roomNumber < 5:

            ySize = randint(size / 3, size)
            xSize = randint(size / 3, size)

            room.append(list('#' * (xSize + 2)))
            for y in range(ySize):
                room.append(list('#' + ('_' * xSize) + '#'))
            room.append(list('#' * (xSize + 2)))

            self._playerPos = [randint(1, ySize), randint(1, xSize)]
        else:
            size = 100 #idk

        self._room = room

    async def sendRoom(self, client : discord.Client, channel : discord.Channel):
        if self._messageId != None:
            await client.delete_message(self._messageId)

        self._messageId = await client.send_message(channel, '<@' + authorId + '>\'s current map:\n' + self)

    async def updateRoom(self, client : discord.Client)
        await client.edit_message(slef._messageId, new_content = ('<@' + authorId + '>\'s current map:\n' + self)
