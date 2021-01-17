import itertools
from pyrez import SmiteAPI
from pyrez.enumerations import Tier
from pyrez.exceptions import PyrezException, PrivatePlayer, PlayerNotFound
from pyrez.enumerations import QueueSmite
from env_vars import devId, authKey
import requests
from bs4 import BeautifulSoup


class LastMatch:

    def __init__(self, player_name):
        self.smiteAPI = SmiteAPI(devId=devId, authKey=authKey)
        self.player_name = player_name
        # print(SmiteAPI.getDataUsed(self.smiteAPI))

    def player_id(self):
        player_id = self.smiteAPI.getPlayerId(self.player_name, portalId=None)
        return player_id[0].playerId

    def conquest_rank(self):
         #TODO: call teveel, moet eruit
        try:
            playerid = self.player_id()
            getplayer = self.smiteAPI.getPlayer(playerid, portalId=None)
            rank_number = getplayer.rankedConquest['Tier']
            #Change rank number to rank text
            rank = Tier(rank_number).name
            return (rank)

        except PrivatePlayer:
            return ('zo een n00b die private heeft opstaan')
        except PyrezException:
            return ('Oei! er is iets misgelopen')

    def god_name(self, match):
        god_names = [dic["Reference_Name"] for dic in match]
        return god_names

    # Gets last Match Id's
    def last_match_id(self):
        conquest = 426
        matchhistory = self.smiteAPI.getMatchHistory(self.player_id())
        matchid = matchhistory[0].matchId
        return matchid

    def last_match_playerNames(self, match):
        names = [dic["hz_player_name"] for dic in match]
        return names

    def last_match_ranks(self):
        match = self.smiteAPI.getMatch(self.last_match_id())
        # print(match)
        Godnames = self.god_name(match)
        names = self.last_match_playerNames(match)
        # print(names)
        ranks = []
        for player in names:
            ranks.append(LastMatch(player).conquest_rank())
            Godnames.append(self.god_name(match))
        print(ranks)
        Pranks = {}
        #TODO: This is the last god played, needs to be connected to the match id
        GodNamesOfPlayers = {}

        for name in names:
            for rank in ranks:
                Pranks[name] = rank
                ranks.remove(rank)
                break
        for name in names:
            for godname in Godnames:
                GodNamesOfPlayers[name] = godname
                Godnames.remove(godname)
                break
        # Divide Teams
        T1p = list(Pranks.keys())[:5]
        T1r = list(Pranks.values())[:5]
        T2p = list(Pranks.keys())[5:]
        T2r = list(Pranks.values())[5:]
        Team1GodName = list(GodNamesOfPlayers.values())[:5]
        Team2GodName = list(GodNamesOfPlayers.values())[5:]
        # TODO Add godnames
        Teams = f"""
    Blue Team:
        {T1p[0]}   is  {T1r[0]} as {Team1GodName[0]}
        {T1p[1]}   is  {T1r[1]} as {Team1GodName[1]}
        {T1p[2]}   is  {T1r[2]} as {Team1GodName[2]}
        {T1p[3]}   is  {T1r[3]} as {Team1GodName[3]}
        {T1p[4]}   is  {T1r[4]} as {Team1GodName[4]}
        
    Red Team:  
        {T2p[0]}   is  {T2r[0]} as {Team2GodName[0]}
        {T2p[1]}   is  {T2r[1]} as {Team2GodName[1]}
        {T2p[2]}   is  {T2r[2]} as {Team2GodName[2]}
        {T2p[3]}   is  {T2r[3]} as {Team2GodName[3]}
        {T2p[4]}   is  {T2r[4]} as {Team2GodName[4]}
        
        """

        return (Teams)


# class TopItems:
#     def __init__(self, god_name):
#         self.god_name = god_name
#
#     def most_build(self):

# URL = f" https://smite.guru/builds/{self.god_name}"
# page = requests.get(URL)
# soup = BeautifulSoup(page.content,('html.parser'))
# build = soup.find(class_='item-img')
# print(build)
# return build
# when returns none, it's not a known god, at error handling


cleendert = LastMatch('Cleendert')
print(cleendert.last_match_ranks())
# cleendert.last_match_ranks()
# cleendert.god_name()
# cleendert = TopItems('anubis')
# cleendert.most_build()
