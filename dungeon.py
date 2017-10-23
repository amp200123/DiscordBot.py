import discord
import copy
import random

from random import randint


class Dungeon:

    def __init__(self, author_id):
        self.active = True
        self.id = author_id
        
        self._message_id = None
        self._roomNumber = 0
        self._room = []
        self._player_pos = []

        self._gen_room()

    def __repr__(self):
        room = copy.deepcopy(self._room)
        
        room[self._player_pos[0]][self._player_pos[1]] = '@'

        s = '```'
        for i in range(len(room)):
            s = (s + '\n') + ''.join(room[i])

        s += '\n```'
        
        return s
        
    def _gen_room(self, shop=False):
        room = []
        size = 0
        
        if not shop:
            if self._roomNumber == 0:
                size = 25
            # elif roomNumber < 5:

            # Room Sizes
            y_size = randint(int(size / 3), size)
            x_size = randint(int(size / 3), size)

            # Create Room
            room.append(list('#' * (x_size + 2)))
            for y in range(y_size):
                room.append(list('#' + ('_' * x_size) + '#'))
            room.append(list('#' * (x_size + 2)))

            # Create square cutouts for room corners
            cutouts = []
            for i in range(4):
                cutouts.append([randint(0, int(y_size / 2)),
                                randint(0, int(x_size / 2))])

            print(cutouts)
            print('Size: ' + str(x_size) + ' ' + str(len(room[0])))

            # Delete cutouts
            #   Top left
            for i in range(cutouts[0][0]):
                for j in range(cutouts[0][1]):
                    room[i][j] = ' '
                room[i][cutouts[0][1]] = '#'
            for j in range(cutouts[0][1] + 1):
                room[cutouts[0][0]][j] = '#'

            #   Top right
            for i in range(cutouts[1][0]):
                for j in range(cutouts[1][1]):
                    room[i][x_size + 1 - j] = ' '
                room[i][x_size + 1 - cutouts[1][1]] = '#'
            for j in range(cutouts[1][1] + 1):
                room[cutouts[1][0]][x_size + 1 - j] = '#'

            #   Bot left
            for i in range(cutouts[2][0]):
                for j in range(cutouts[2][1]):
                    room[y_size + 1 - i][j] = ' '
                room[y_size + 1 - i][cutouts[2][1]] = '#'
            for j in range(cutouts[2][1] + 1):
                room[y_size + 1 - cutouts[2][0]][j] = '#'

            #   Top right
            for i in range(cutouts[3][0]):
                for j in range(cutouts[3][1]):
                    room[y_size + 1 - i][x_size + 1 - j] = ' '
                room[y_size + 1 - i][x_size + 1 - cutouts[3][1]] = '#'
            for j in range(cutouts[3][1] + 1):
                room[y_size + 1 - cutouts[3][0]][x_size + 1 - j] = '#'

            # Player position
            while 1:
                self._player_pos = [randint(1, y_size), randint(1, x_size)]
                if room[self._player_pos[0]][self._player_pos[1]] == '_':
                    break

            # exit =
            # print(exit)

        else:
            size = 100  # idk

        self._room = room

    def move(self, y, x):
        if y != 0 and 1 < self._player_pos[0] < len(self._room):
            self._player_pos[0] += y
        if x != 0 and 1 < self._player_pos[1] < len(self._room[0]):
            self._player_pos[1] += x

    async def send_room(self, client: discord.Client, channel: discord.Channel):
        if self._message_id is not None:
            await client.delete_message(self._message_id)

        self._message_id = await client.send_message(channel, '<@' + self.id + '>\'s current map:\n' + str(self))

    async def update_room(self, client: discord.Client):
        await client.edit_message(self._message_id, new_content=('<@' + self.id + '>\'s current map:\n' + str(self)))

    async def quit(self, client: discord.Client, channel: discord.Channel, save=False):
        if self._message_id is not None:
            await client.delete_message(self._message_id)
            
        await client.send_message(channel, '<@' + self.id + '>: ' +
                                  ('Saved and quit' if save else 'Quit') + ' game of Dungeons')
