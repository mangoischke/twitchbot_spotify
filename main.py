from twioBot import Bot
from Cogs.pubsubChannelPoints import PubSubChannelPoints
from Cogs.cmdRequest import CmdRequest
from channelPointRewards import ChannelPointRewards
import json
from pprint import pprint
from gettoken import Token
import os
import atexit
import asyncio

#@atexit.register
#def stopBot():
#    print("Stopping TwioBot...")
#    loop = asyncio.get_event_loop()
#    loop.run_until_complete(channelPointRewards.disable_reward(config['twitch_access_token'], "Song Request"))
#    loop.run_until_complete(channelPointRewards.disable_reward(config['twitch_access_token'], "Add Song to Playlist"))
#    print("TwioBot stopped.")

config = open('config/config.json', 'r')
config = json.load(config)

print("Getting access token...")
twitchBotData = Token(config)
config['twitch_access_token'] = twitchBotData.access_token
config['client_id'] = twitchBotData.client_id
print("Got access token!")

print('Starting TwioBot...')
bot = Bot(config)
#bot.setup()

# Clients
print('Loading cmdRequests...')
cmdRequest = CmdRequest(bot, config)
bot.add_cog(cmdRequest)

print('Loading PubSubChannelPoints...')
pubSubChannelPoints = PubSubChannelPoints(bot, config)
bot.add_cog(pubSubChannelPoints)

bot.run()