import discord
import copy

from random import randint


class Dungeon:

    def __init__(self, authorId):
        self.active = True
        self.id = authorId
        
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
                size = 15
            # elif roomNumber < 5:

            y_size = randint(size / 3, size)
            x_size = randint(size / 3, size)

            room.append(list('#' * (x_size + 2)))
            for y in range(y_size):
                room.append(list('#' + ('_' * x_size) + '#'))
            room.append(list('#' * (x_size + 2)))

            self._player_pos = [randint(1, y_size), randint(1, x_size)]
        else:
            size = 100  # idk

        self._room = room

    def move(self, y, x):
        if y != 0 and self._player_pos[0] > 1 and self._player_pos[0] < len(self._room):
            self._player_pos[0] += y
        if x != 0 and self._player_pos[1] > 1 and self._player_pos[1] < len(self._room[0]):
            self._player_pos[1] += x

    async def send_room(self, client: discord.Client, channel: discord.Channel):
        if self._message_id is not None:
            await client.delete_message(self._message_id)

        self._message_id = await client.send_message(channel, '<@' + self.id + '>\'s current map:\n' + str(self))

    async def update_room(self, client: discord.Client):
        await client.edit_message(self._message_id, new_content = ('<@' + self.id + '>\'s current map:\n' + str(self)))

    async def pause(self, client : discord.Client, channel: discord.Channel, save=False):
        if self._message_id is not None:
            await client.delete_message(self._message_id)
            
        await client.send_message(channel, '<@' + self.id + '>: ' +
                                  ('Saved and quit' if save else 'Quit') + ' game of Dungeons')
