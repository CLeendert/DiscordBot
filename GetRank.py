from pyrez import SmiteAPI
from pyrez.enumerations import Tier
from pyrez.exceptions import PyrezException, PrivatePlayer, PlayerNotFound
from pyrez.enumerations import QueueSmite
from env_vars import devId, authKey


class LastMatch:

    def __init__(self, player_name):
        self.smiteAPI = SmiteAPI(devId=devId, authKey=authKey)
        self.player_name = player_name

    def player_id(self):
        player_id = self.smiteAPI.getPlayerId(self.player_name, portalId=None)
        return player_id[0].playerId

    def conquest_rank(self):
        try:
            conquestrank = self.smiteAPI.getPlayer(self.player_id(), portalId=None)
            rank_number = conquestrank.rankedConquest['Tier']
            rank = Tier(rank_number).name
            return rank
        except PyrezException:
            return('is zo een n00b die private heeft opstaan')

#TODO private player error handling
    # def match_history(self):
    #     matchhistory = self.smiteAPI.getMatchids(426)
    #     return matchhistory


# cleendert = LastMatch('Cleendert')
# print(cleendert.match_history())
# print(QueueSmite(426).name)