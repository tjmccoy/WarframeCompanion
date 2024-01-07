from pylotus import *
import discord as d
import dotenv 
import os

dotenv.load_dotenv()
category_name = "Warframe Companion Bot"
channel_names = ["arbitration", "archon-hunt", "void-trader", "world-timers", "fissures", "sortie", "steel-path"]
bot = d.Bot(intents = d.Intents.default())

@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}!")
    for guild in bot.guilds:
        await make_channels(guild)

async def make_channels(guild):
    category = None
    for cat in guild.categories: 
        if cat.name == category_name:
            category = cat

    if category is None:
        category = await guild.create_category(category_name)

    for channel in channel_names:
        if channel not in [channel.name for channel in category.channels]:
            await category.create_text_channel(channel)
    
@bot.slash_command(description = "Creates WC text channels for your server.", name = "make-channels")
async def slash_make_channels(ctx):
    await ctx.respond("Creating channels...")
    await make_channels(ctx.guild)
        
bot.run(os.getenv("TOKEN"))
