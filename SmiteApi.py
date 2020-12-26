import pyrez
import os
#from utils import get_env
import json

import pyrez.api
from pyrez.api import PaladinsAPI, SmiteAPI, RealmRoyaleAPI
import pyrez.enumerations
import pyrez.models


smiteAPI = SmiteAPI(devId=get_env('devId'), authKey=get_env('authKey'))

S_PLAYER_NOT_FOUND_STRINGS = {
  'en' : "🚫 ERROR: “{player_name}” doesn't exist or it's hidden! Make sure that your account is marked as “Public Profile”'"}


#player_name = "Cleendert"

def get_player_id(player_name, platform=None):
  if not player_name or player_name in ['$(queryencode%20$(1:)', 'none', '0', 'null', '$(1)', 'query=$(querystring)', '[invalid%20variable]', 'your_ign', '$target']:
    return 0
  player_name = player_name.strip().lower()
  if str(player_name).isnumeric():
    return player_name if len(str(player_name)) > 5 or len(str(player_name)) < 12 else 0
  temp = smiteAPI.getPlayerId(player_name, platform) if platform and str(platform).isnumeric() else smiteAPI.getPlayerId(player_name)
  if not temp:
    return -1
  return temp[0].playerId
def get_in_game_name(player):
  try:
    return (player.hzPlayerName or player.hzGamerTag) or player.playerName
  except Exception:
    pass
  return player.playerName

def get_rank_name(tier):
  if tier >= 1 and tier <= 5:
    return 'Bronze'
  if tier >= 6 and tier <= 10:
    return 'Silver'
  if tier >= 11 and tier <= 15:
    return 'Gold'
  if tier >= 16 and tier <= 20:
    return 'Platinum'
  if tier >= 21 and tier <= 25:
    return 'Diamond'
  if tier == 26:
    return 'Master'
  if tier == 27:
    return 'Grandmaster'
  if tier == 0:
    return 'Unranked'
  return '???'

def print_exception(exc):
  print(f'{type(exc)} : {exc.args} : {exc} : {str(exc)}')