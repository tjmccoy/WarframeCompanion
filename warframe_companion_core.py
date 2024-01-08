import discord as d
from discord_helpers import *
from enum import Enum
import pylotus as pl

CATEGORY_NAME = "Warframe Companion Bot"
async def wc_send_to_channel(guild: d.Guild, msg: str, channel_name: str):
    await send_to_channel(guild, msg, channel_name, CATEGORY_NAME)

async def wc_clear_channel(guild: d.Guild, channel_name: str):
    await clear_channel(guild, channel_name, CATEGORY_NAME)

class ChannelName(Enum):
    archon_hunt = "archon-hunt"
    arbitration = "arbitration"
    void_trader = "void-trader"
    world_timers = "world-timers"
    fissures = "fissures"
    sortie = "sortie"
    steel_path = "steel-path"

async def initialize_guild(guild: d.Guild):
    await make_channels(guild)
    await display_arbitration(guild)

async def make_channels(guild: d.Guild):
    for channel_name in ChannelName:
        await make_channel(guild, channel_name.value, CATEGORY_NAME)

async def display_fissures(guild: d.Guild, current_fissures: dict):
    await wc_clear_channel(guild, ChannelName.fissures.value)
    information = ""
    fissure_objects = [pl.Fissure(fissure) for fissure in current_fissures]
    for f in fissure_objects:
        information += f"{f.node} | {f.missionType} ({f.tier})" + "\n"
    await wc_send_to_channel(guild, information, ChannelName.fissures.value)

async def display_arbitration(guild: d.Guild):
    await wc_clear_channel(guild, ChannelName.arbitration.value)
    await wc_send_to_channel(guild, "Arbitration information currently unavailable", ChannelName.arbitration.value)