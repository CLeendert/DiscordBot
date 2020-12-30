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
# smiteAPI = SmiteAPI(devId=devId, authKey=authKey)
#
# player_name = "Cleendert"
# player_id = smiteAPI.getPlayerId(player_name, portalId=None)
# tests = []
# # test = json.loads(player_id)
# player_id2 = player_id.get('player_id')
#
# print(player_id2)
import Dict
import Gods


class APIResponseBase(Dict):
    """Superclass for all Pyrez models.
    Keyword Arguments
    -----------------
    json : |DICT| or |LIST|
        The request as JSON, if you prefer.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.json = kwargs or []


class APIResponse(APIResponseBase):
    """Represents a generic Pyrez object. This is a sub-class of :class:`APIResponseBase`.
        Keyword Arguments
        -----------------
        errorMsg : |STR|
            The message returned from the API request.
        """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.errorMsg = kwargs.get("ret_msg", kwargs.get("error", kwargs.get("errors", None))) or None

    @property
    def hasError(self):
        return self.errorMsg is not None


class Winratio:
    def __init__(self, **kwargs):
        self.losses = kwargs.get("Losses", kwargs.get("losses", 0)) or 0
        self.wins = kwargs.get("Wins", kwargs.get("wins", 0)) or 0

    @property
    def winratio(self):
        _w = self.wins / (self.matches_played if self.matches_played > 1 else 1) * 100.0
        return int(_w) if _w % 2 == 0 else round(_w, 2)

    @property
    def matches_played(self):
        return self.wins + self.losses


class KDA:
    def __init__(self, **kwargs):
        self.assists = kwargs.get("Assists", 0) or 0
        self.deaths = kwargs.get("Deaths", 0) or 0
        self.kills = kwargs.get("Kills", 0) or 0

    @property
    def kda(self):
        _k = ((self.assists / 2) + self.kills) / (self.deaths if self.deaths > 1 else 1)
        return int(_k) if _k % 2 == 0 else round(_k, 2)  # + "%";


class GodRank(APIResponse, Winratio, KDA):
    def __init__(self, **kwargs):
        APIResponse.__init__(self, **kwargs)  # super().__init__(**kwargs)
        Winratio.__init__(self, **kwargs)
        KDA.__init__(self, **kwargs)
        try:
            self.godId = Gods(kwargs.get("god_id"))  # if kwargs.get("god_id") else Champions(kwargs.get("champion_id"))
            self.godName = self.godId.getName()
        except ValueError:
            self.godId = kwargs.get("god_id", kwargs.get("champion_id", 0)) or 0
            self.godName = kwargs.get("god", kwargs.get("champion", '')) or ''
        self.godLevel = kwargs.get("Rank", 0) or 0
        self.gold = kwargs.get("Gold", 0) or 0
        self.lastPlayed = kwargs.get("LastPlayed", '') or ''
        self.minionKills = kwargs.get("MinionKills", 0) or 0
        self.minutes = kwargs.get("Minutes", 0) or 0
        self.totalXP = kwargs.get("Worshippers", 0) or 0
        self.playerId = kwargs.get("player_id", 0) or 0
