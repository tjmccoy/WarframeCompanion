from pylotus import *
import discord as d
import dotenv 
import os

dotenv.load_dotenv()
category_name = "Warframe Companion Bot"
channel_names = ["arbitration", "archon-hunt", "void-trader", "world-timers", "fissures", "sortie", "steel-path"]

class MyClient(d.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")
        for guild in self.guilds:
            category = None
            for cat in guild.categories: 
                 if cat.name == category_name:
                     category = cat

            if category is None:
                category = await guild.create_category(category_name)

            for channel in channel_names:
                if channel not in [channel.name for channel in category.channels]:
                    await category.create_text_channel(channel)
    
    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")
    
client = MyClient(intents = d.Intents.all())
client.run(os.getenv("TOKEN"))
