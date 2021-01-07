import itertools

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
        # conquest = 426
        matchhistory = self.smiteAPI.getMatchHistory(self.player_id())
        matchid = matchhistory[0].matchId
        return matchid

    def last_match_playerNames(self):
        match = self.smiteAPI.getMatch(self.last_match_id())
        names = [dic["hz_player_name"] for dic in match]
        return names

    def last_match_ranks(self):
        names = self.last_match_playerNames()
        ranks = []
        Pranks = {}
        for player in names:
            ranks.append(LastMatch(player).conquest_rank())
        # print(ranks)
        # print(names)
        for name in names:
            for rank in ranks:
                Pranks[name] = rank
                ranks.remove(rank)
                break
        #Divide Teams
        T1p = list(Pranks.keys())[:5]
        T1r = list(Pranks.values())[:5]
        T2p = list(Pranks.keys())[5:]
        T2r = list(Pranks.values())[:5]
        Teams = f"""
        Enemy Team:
        {T1p[0]} is {T1r[0]}
        {T1p[1]} is {T1r[1]}
        {T1p[2]} is {T1r[2]}
        {T1p[3]} is {T1r[3]}
        {T1p[4]} is {T1r[4]}
        Your Team:
        {T2p[0]} is {T2r[0]}
        {T2p[1]} is {T2r[1]}
        {T2p[2]} is {T2r[2]}
        {T2p[3]} is {T2r[3]}
        {T2p[4]} is {T2r[4]}
        """
        return (Teams)


#
# cleendert = LastMatch('Cleendert')
#
# print(cleendert.last_match_ranks())
# cleendert.last_match_ranks()
# print(cleendert.last_match_playerNames())
# print(cleendert.queuestats())
