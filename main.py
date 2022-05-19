import discord
import os
from riotwatcher import LolWatcher, ApiError
from keep_alive import keep_alive

client = discord.Client()
watcher = LolWatcher(os.environ['RIOT_KEY'])
region = 'eun1'

#Uses Riot's API to get the id of the summoner with specified name
def get_summoner_id(name):
  player_stats = watcher.summoner.by_name(region, name)
  id = player_stats['id']
  return id

#Uses summoner's id to access stats about their League of Legends career. Sometimes Ranked Solo/Duo Queue appears first in the list but sometimes it appears second. This is why I run a check to reveice only Solo/Duo info.
def get_summoner_rank(id):
  player_stats = watcher.league.by_summoner(region, id)
  if player_stats[0]['queueType'] == 'RANKED_SOLO_5x5':
    tier = player_stats[0]['tier']
    rank = player_stats[0]['rank']
    wins = player_stats[0]['wins']
    losses = player_stats[0]['losses']
    lp = player_stats[0]['leaguePoints']
  else:
    tier = player_stats[1]['tier']
    rank = player_stats[1]['rank']
    wins = player_stats[1]['wins']
    losses = player_stats[1]['losses']
    lp = player_stats[1]['leaguePoints']
  
  rank_stats = [tier, rank, wins, losses, lp]
  return rank_stats

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

#User can type $summoner ____ and the Bot will return their Solo/Duo rankings, wins and losses as well as League Points. The Bot will return an exception if no player with specified name exists.
  if message.content.startswith("$summoner"):
    name = message.content.split("$summoner ", 1)[1]
    id = get_summoner_id(name)
    rank_stats = get_summoner_rank(id)
    await message.channel.send("Rank: " + rank_stats[0] + " " + rank_stats[1] + " , Wins/Losses: " + str(rank_stats[2]) + "/" + str(rank_stats[3]) + " , League Points: " + str(rank_stats[4]))
  
#Keep alive is a different file that is required so that I can keep my Bot alive, with the use of Uptime Robot
#even when the repl.it tabs are closed. I currently don't possess specific information about it, I just use it to keep my Bot alive at all times. I will
#upload it to GitHub in case some wants to use it as well.
keep_alive()
client.run(os.environ['TOKEN'])