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

    #Gets Match Id's
    # def match_history(self):
    #     conquest = 426
    #     matchhistory = self.smiteAPI.getMatchIds(conquest, hour=1)
    #     return matchhistory
    # def queuestats(self):
    #     queuestats= self.smiteAPI.getQueueStats(playerId=self.player_id())
    #     return queuestats

    def test(self):
        conquest = 426
        test = self.smiteAPI.getMatchIds(conquest)
        return max(test)
#
cleendert = LastMatch('Cleendert')
print(cleendert.test())
# print(QueueSmite(426).name)