import discord as d
import dotenv
import scheduler
import os
from pylotus import *

dotenv.load_dotenv()
category_name = "Warframe Companion Bot"
channel_names = ["arbitration", "archon-hunt", "void-trader", "world-timers", "fissures", "sortie", "steel-path"]
bot = d.Bot(intents = d.Intents.default())
wf = wf_api('pc')

@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}!")
    for guild in bot.guilds:
        await make_channels(guild)
    await update_arbitration()

async def clear_channel(guild: d.Guild, channel_name: str):
    channel = await make_channel(guild, channel_name)
    channel.purge()

async def send_to_channel(guild: d.Guild, msg: str, channel_name: str):
    channel = await make_channel(guild, channel_name)
    await channel.send(msg)

async def make_channel(guild, channel_name) -> d.CategoryChannel:
    category = None
    for cat in guild.categories:
        if cat.name == category_name:
            category = cat

    if category is None:
        category = await guild.create_category(category_name)

    channel = None
    for c in category.channels:
        if c.name == channel_name:
            channel = c
            break
    
    if channel == None:
        channel = await category.create_text_channel(channel_name)

    return channel

async def make_channels(guild: d.Guild):
    for channel in channel_names:
        await make_channel(guild, channel)

async def display_fissures(guild: d.Guild, current_fissures):
    information = ""
    fissure_objects = [Fissure(fissure) for fissure in current_fissures]
    for f in fissure_objects:
        information += f"{f.node} | {f.missionType} ({f.tier})" + "\n"
    await send_to_channel(guild, information[:2000], channel_names[4])
        

async def update_arbitration():
    for guild in bot.guilds:
        await clear_channel(guild, "arbitration")
        await send_to_channel(guild, "Arbitration information currently unavailable", channel_names[0])

@bot.slash_command(description = "Creates WC text channels for your server.", name = "make-channels")
async def slash_make_channels(ctx):
    await ctx.respond("Creating channels...")
    await make_channels(ctx.guild)

@bot.slash_command(description = "Updates current void fissure data.", name = "fissures")
async def slash_fissures(ctx):
    await ctx.respond("Gathering fissures data...")
    current_fissures = wf.get_fissure_info()
    await display_fissures(ctx.guild, current_fissures)

token = os.getenv('TOKEN')
if token == None:
    print("TOKEN not found in .env file. Please create a file named .env and add the line TOKEN = {Your bot token here}")
    quit()

try:
    bot.run(token)
except Exception as e:
    print("Bot failed to start:")
    print(e)
