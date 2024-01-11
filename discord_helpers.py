import discord as d

MAX_MSG_LEN = 2000

async def clear_channel(guild: d.Guild, channel_name: str, category_name: str = ""):
    channel = await make_channel(guild, channel_name, category_name)
    await channel.purge()

async def send_to_channel(guild: d.Guild, msg: str, channel_name: str, category_name: str = ""):
    channel = await make_channel(guild, channel_name, category_name)
    remaining = msg
    while len(remaining) > MAX_MSG_LEN and '\n' in remaining: # If msg is too long and there are newlines
        end = remaining[:MAX_MSG_LEN].rfind('\n') # break up the message and send in chunks by line
        await channel.send(remaining[:end])
        remaining = remaining[end:]
    while len(remaining) > MAX_MSG_LEN: # If msg is too long and no newlines
        await channel.send(remaining[:MAX_MSG_LEN]) # break up message anyway
        remaining = remaining[MAX_MSG_LEN:]
    await channel.send(remaining) # finally send the remaining msg that is < MAX_MSG_LEN

async def make_channel(guild: d.Guild, channel_name: str, category_name = "") -> d.CategoryChannel:
    category = None
    channel = None
    if (category_name != ""):
        for cat in guild.categories:
            if cat.name == category_name:
                category = cat

        if category is None:
            category = await guild.create_category(category_name)

        for c in category.channels:
            if c.name == channel_name:
                channel = c
                break
    
    if channel == None:
        channel = await category.create_text_channel(channel_name) if category != None else await guild.create_text_channel(channel_name)

    return channel
