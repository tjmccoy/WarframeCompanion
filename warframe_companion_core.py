import discord as d
from discord_helpers import *
from enum import Enum
import pylotus as pl

CATEGORY_NAME = "Warframe Companion Bot"

class ChannelName(Enum):
    arbitration = "arbitration"
    archon_hunt = "archon-hunt"
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
        await make_channel(guild, channel_name.value)

async def display_fissures(guild: d.Guild, current_fissures: dict):
    await clear_channel(guild, ChannelName.fissures)
    information = ""
    fissure_objects = [pl.Fissure(fissure) for fissure in current_fissures]
    for f in fissure_objects:
        information += f"{f.node} | {f.missionType} ({f.tier})" + "\n"
    await send_to_channel(guild, information, ChannelName.fissures)

async def display_arbitration(guild: d.Guild):
    await clear_channel(guild, ChannelName.arbitration)
    await send_to_channel(guild, "Arbitration information currently unavailable", ChannelName.arbitration)