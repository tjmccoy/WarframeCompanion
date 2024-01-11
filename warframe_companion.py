import dotenv
import os
import pylotus as pl
import scheduler
from warframe_companion_core import *

bot = d.Bot(intents = d.Intents.default())
wf = pl.wf_api('pc')

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
    current_fissures = wf.get_fissure_info()
    await display_fissures(ctx.guild, current_fissures)

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
