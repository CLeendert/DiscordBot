from pyrez import SmiteAPI
import json
import requests
from DiscordBot.env_vars import devId, authKey

# def connecteren:
smiteAPI = SmiteAPI(devId=devId, authKey=authKey)

player_id = smiteAPI.getPlayerId('cleendert', portalId=None)
print(player_id[0].playerId)
