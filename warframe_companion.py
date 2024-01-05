from pylotus import *
import discord as d
import dotenv 
import os

dotenv.load_dotenv()

print(wf_api.get_platforms()) # It's always possible to retrieve all supported platforms with which to construct the API, even in a static context.
pc = wf_api("pc")
current_fissures = pc.get_fissure_info()

fissure_objects = [Fissure(fissure) for fissure in current_fissures]

for f in fissure_objects:
    print(type(f), f.enemy, f.missionType)

class MyClient(d.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")
    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")
    
client = MyClient(intents = d.Intents.all())
client.run(os.getenv("TOKEN"))
