import discord
import asyncio
import copy
import dungeon

from random import randint
from discord.ext import commands

#### Global variables ###
bot = commands.Bot(command_prefix = '^')
cmdPrefix = '^'

dungeons = [] #List of player dungeons
#########################


### Events ###
@bot.event
async def on_ready():
	print('Ready!')

@bot.event
async def on_message(message):
    if message.author != bot.user:
        content = message.content
        authorId = message.author.id
        
        if inDungeon:
            if content.startswith('quit'):
                inDungeon.remove(authorId)
                await bot.send_message(message.channel, '<@' + authorId + '>: Quit game of Dungeons')
                await bot.delete_message(currentMessage[authorId])
                del currentMessage[authorId]
            elif content.startswith('check'):
                await sendRoom(message.channel, authorId)
            elif content.startswith('help'):
                s =  '```\n'
                s += 'Help for DUNGEONS\n\n'
                s += 'Commands:\n'
                s += '   help - Sends this message\n'
                s += '   quit - Quits game (Note: game NOT saved)\n'
                s += '   save - Exit game and save; Use "^resume" later to resume game\n'
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
                await bot.send_message(message.channel, s)

            elif content.startswith('w') or content.startswith('up'):
                if currentPos[authorId][0] > 1:
                    currentPos[authorId][0] -= 1
                await bot.delete_message(message)
                await updateRoom(authorId)
            elif content.startswith('a') or content.startswith('left'):
                if currentPos[authorId][1] > 1:
                    currentPos[authorId][1] -= 1
                await bot.delete_message(message)
                await updateRoom(authorId)
            elif content.startswith('s') or content.startswith('down'):
                if currentPos[authorId][0] < len(currentRoom[authorId]) - 2:
                    currentPos[authorId][0] += 1
                await bot.delete_message(message)
                await updateRoom(authorId)
            elif content.startswith('d') or content.startswith('right'):
                if currentPos[authorId][1] < len(currentRoom[authorId][0]) - 2:
                    currentPos[authorId][1] += 1
                await bot.delete_message(message)
                await updateRoom(authorId)

        else:
            await bot.process_commands(message)
    
                
#Commands
@bot.command(aliases = ['invite'], help='Retrieves the invite URL for this bot.')
async def url():
    await bot.say('https://discordapp.com/oauth2/authorize?client_id=258031474404491265&scope=bot&permissions=36793353\nAdd me <3')

@bot.command(pass_context=True)
async def dungeons(ctx):
    await bot.say("Welcome to DUNGEONS!\n\n Dungeons is a top down, turn based rpg!\n\nType 'help' at any time to check available commands.\nYou can also type 'quit' to exit the game.")
    d = dungeon.Dungeon(ctx.message.author.id)
    await d.sendRoom(bot, ctx.message.channel)
    dungeons.append(d)

@bot.command(pass_context=True)
async def resume(ctx):
    first(

###############


#Run client
bot.run('MjU4MDMxNDc0NDA0NDkxMjY1.DLaHmA.lhIzwxq4aeHtOe1llCeZ2BluOdA')
