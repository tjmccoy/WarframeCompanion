import discord as d
from discord_helpers import *
from enum import Enum
import pyframe

CATEGORY_NAME = "Warframe Companion Bot"

class ChannelName(Enum):
    archon_hunt = "archon-hunt"
    arbitration = "arbitration"
    void_trader = "void-trader"
    world_timers = "world-timers"
    fissures = "fissures"
    sortie = "sortie"
    steel_path = "steel-path"

async def wc_send_to_channel(guild: d.Guild, msg: str, channel_name: ChannelName):
    await send_to_channel(guild, msg, channel_name.value, CATEGORY_NAME)

async def wc_clear_channel(guild: d.Guild, channel_name: ChannelName):
    await clear_channel(guild, channel_name.value, CATEGORY_NAME)

async def initialize_guild(guild: d.Guild):
    await make_channels(guild)
    await display_arbitration(guild)

async def make_channels(guild: d.Guild):
    for channel_name in ChannelName:
        await make_channel(guild, channel_name.value, CATEGORY_NAME)

async def display_fissures(guild: d.Guild, current_fissures: list[pyframe.Fissure]):
    await wc_clear_channel(guild, ChannelName.fissures)
    information = ""
    for f in current_fissures:
        information += f"{f.node} | {f.mission_type} ({f.tier})" + "\n"
    await wc_send_to_channel(guild, information, ChannelName.fissures)

async def display_arbitration(guild: d.Guild):
    await wc_clear_channel(guild, ChannelName.arbitration)
    await wc_send_to_channel(guild, "Arbitration information currently unavailable", ChannelName.arbitration)

async def display_void_trader(guild: d.Guild, void_trader: pyframe.VoidTrader):
    await wc_clear_channel(guild, ChannelName.void_trader)
    information = ""
    void_trader = pyframe.get_void_trader()
    if not void_trader.active:
        await wc_send_to_channel(guild, f"Void trader is not here. He will return on {str(void_trader.activation).split('+')[0]} UTC.", ChannelName.void_trader)
        return
    
    information += f"Location: {void_trader.location}" + "\n"
    information += f"Next Arrival: {void_trader.activation}" + "\n"
    information += f"Next Departure: {void_trader.expiry}" + "\n"
    information += f"Inventory: " + "\n"
    for i in void_trader.inventory:
        information += f"{i.item} | {i.ducats} ducats | {i.credits} credits" + "\n"

    await wc_send_to_channel(guild, information, ChannelName.void_trader)