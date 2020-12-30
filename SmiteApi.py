import pyrez
from pyrez.api import *
from pyrez.exceptions import (
    PlayerNotFound,
    MatchException,
)
from pyrez.exceptions.PrivatePlayer import PrivatePlayer
from pyrez.enumerations import Tier
from pyrez import SmiteAPI
import json
from pyrez.enumerations.QueueSmite import QueueSmite

# from ..utils import get_env
# from ..utils.num import format_decimal
# from langs import *

import requests
from DiscordBot.env_vars import devId, authKey

# def connecteren:
smiteAPI = SmiteAPI(devId=devId, authKey=authKey)


class LastMatch:
    def __init__(self, player_name):
        self.player_name = player_name

    def NameToId(self):
        player_id = smiteAPI.getPlayerId(self.player_name, portalId=None)
        return player_id[0].playerId

    def MatchHistory(self):
        LastGame = smiteAPI.getMatchHistory(playerId=self.player_id)
        return LastGame


cleendert = LastMatch('Cleendert')

print(cleendert.NameToId())
