import discord
import dungeon

from discord.ext import commands

# Global variables #
bot = commands.Bot(command_prefix='^')
cmdPrefix = '^'

players = []  # List of player dungeons
#########################


# Events #
@bot.event
async def on_ready():
    print('Ready!')


@bot.event
async def on_message(message):
    if message.author != bot.user:
        content = message.content
        author_id = message.author.id

        try: 
            player = next(x for x in players if x.id == author_id)

        except:
            player = None
        
        if player is not None and player.active:
            if content.startswith('quit'):
                players.remove(player)
                await player.quit(bot, message.channel)
            elif content.startswith('save'):
                player.quit(bot, message.channel, save=True)
            elif content.startswith('check'):
                await player.sendRoom(bot, message.channel)
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
                player.move(-1, 0)
                await player.update_room(bot)
            elif content.startswith('a') or content.startswith('left'):
                player.move(0, -1)
                await player.update_room(bot)
            elif content.startswith('s') or content.startswith('down'):
                player.move(1, 0)
                await player.update_room(bot)
            elif content.startswith('d') or content.startswith('right'):
                player.move(0, 1)
                await player.update_room(bot)

        else:
            await bot.process_commands(message)
    
                
# Commands
@bot.command(aliases=['invite'], help='Retrieves the invite URL for this bot.')
async def url():
    await bot.say('https://discordapp.com/oauth2/authorize?client_id=258031474404491265&scope=bot&permissions=36793353\nAdd me <3')


@bot.command(pass_context=True)
async def dungeons(ctx):
    await bot.say("Welcome to DUNGEONS!\n\n Dungeons is a top down, turn based rpg!\n\nType 'help' at any time to check available commands.\nYou can also type 'quit' to exit the game.")
    d = dungeon.Dungeon(ctx.message.author.id)
    await d.send_room(bot, ctx.message.channel)
    players.append(d)


@bot.command(pass_context=True)
async def resume(ctx):
    pass

###############


# Run client
# noinspection SpellCheckingInspection
bot.run('MjU4MDMxNDc0NDA0NDkxMjY1.DLaHmA.lhIzwxq4aeHtOe1llCeZ2BluOdA')
