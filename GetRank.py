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
            # print(conquestrank)
            return (rank)

        except PrivatePlayer:
            return('is zo een n00b die private heeft opstaan')
        except PyrezException:
            return('Oei! er is iets misgelopen')

    # Gets last Match Id's
    def last_match_id(self):
        conquest = 426
        matchhistory = self.smiteAPI.getMatchHistory(self.player_id())
        matchid = matchhistory[1].matchId
        return matchid

    def last_match_playerNames(self):
        match = self.smiteAPI.getMatch(self.last_match_id())
        names = [dic["hz_player_name"] for dic in match]
        return names

    def last_match_ranks(self):
        names = self.last_match_playerNames()
        ranks = []
        for player in names:
            ranks.append(LastMatch(player).conquest_rank())
        return(ranks)


#
cleendert = LastMatch('Cleendert')
#
print(cleendert.last_match_ranks())
# cleendert.last_match_ranks()
# print(cleendert.last_match_playerNames())
# print(cleendert.queuestats())