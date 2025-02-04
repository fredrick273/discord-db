import discord
import os
import pickle
import json
import base64
from dotenv import load_dotenv
from helper import process_query,get_dbinfo_channel

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD = int(os.getenv('GUILD'))



intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('Logged on as', client.user)
    if GUILD not in [i.id for i in client.guilds]:
        print("No Server")
        return
    print(GUILD,"is present \n")
    print("Connected Successfully!! \n")

    channels = client.get_guild(GUILD).text_channels
    if "dbinfo" not in [i.name for i in channels]:
        print("No pre-existing database found")
    else:
        dbinfo_channel = get_dbinfo_channel(client)
        message = [message async for message in dbinfo_channel.history(limit=1, oldest_first=True)][0].content
        data = base64.b64decode(message)
        info = pickle.loads(data)
        print("Connected to",info['db_name'],'Database')
    while True:
        print("Enter queries:")
        print("> ",end=" ")
        query = input()
        await process_query(query,client)



# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content == 'ping':
#         await message.channel.send('pong')




client.run(TOKEN)

