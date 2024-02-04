import dotenv
import os
from warframe_companion_core import *

bot = d.Bot(intents = d.Intents.default())

@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}!")
    for guild in bot.guilds:
        await initialize_guild(guild)

@bot.slash_command(description = "Creates WC text channels for your server.", name = "make-channels")
async def slash_make_channels(ctx):
    await ctx.respond("Creating channels...")
    await make_channels(ctx.guild)

@bot.slash_command(description = "Updates current void fissure data.", name = "fissures")
async def slash_fissures(ctx):
    await ctx.respond("Gathering fissures data...")
    current_fissures = pyframe.get_fissures()
    await display_fissures(ctx.guild, current_fissures)

@bot.slash_command(description = "Updates current void trader data.", name = "void-trader")
async def slash_void_trader(ctx):
    await ctx.respond("Gather void trader data...")
    void_trader = pyframe.get_void_trader()
    await display_void_trader(ctx.guild, void_trader)

@bot.slash_command(description= "Displays current Steel Path information.", name = "steel-path")
async def slash_steel_path(ctx):
    await ctx.respond("Gathering Steel Path data...")
    steel_path = pyframe.get_steel_path()
    await display_steel_path(ctx.guild, steel_path)

@bot.slash_command(description= "Displays world timers.", name= "world-timers")
async def slash_world_timers(ctx):
    await ctx.respond("Gathering current world timers...")
    earth = pyframe.get_earth_cycle()
    cetus = pyframe.get_cetus_cycle()
    vallis = pyframe.get_vallis_cycle()
    cambion = pyframe.get_cambion_cycle()
    await display_world_timers(ctx.guild, earth, cetus, vallis, cambion)

if __name__ == "__main__":
    dotenv.load_dotenv()
    token = os.getenv('TOKEN')
    if token == None:
        print("TOKEN not found in .env file. Please create a file named .env and add the line TOKEN = {Your bot token here}")
        quit()

    try:
        bot.run(token)
    except Exception as e:
        print("Bot failed to start:")
        print(e)
