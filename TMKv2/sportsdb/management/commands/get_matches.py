import requests
from django.core.management.base import BaseCommand
from sportsdb.models import Match, League, Team
from .get_team import teamData
import environ
env = environ.Env()
environ.Env.read_env("TMKv2\\TMKv2\\.env")

def getMatches(id: int):
     
    league_instance = League.objects.get(leagueid=id)
    season = league_instance.seasonformat
    print(f"Getting matches for {id}, {season}")
    response = requests.get(f"https://www.thesportsdb.com/api/v1/json/{env("API_KEY")}/eventsseason.php?id={id}&s={season}")
    data = response.json()
    entries = len(data.get("events", []))
    for x in range(entries):
            currentMatch = response.json()['events'][x]
            instance = Match(
            matchid=currentMatch['idEvent'],
            matchteams=currentMatch['strEvent'],
            league=currentMatch['strLeague'],
            matchday=currentMatch['intRound'],
            hometeam=currentMatch['strHomeTeam'],
            awayteam=currentMatch['strAwayTeam'],
            homescore=currentMatch['intHomeScore'],
            awayscore=currentMatch['intAwayScore'],
            season=currentMatch['strSeason'],
            date=currentMatch['dateEvent'],
            time=currentMatch['strTime'],
            venue=currentMatch['strVenue'],
            badge=currentMatch['strSquare'],
            video=currentMatch['strVideo']
            )
            instance.leagueid = league_instance
            try:
                instance.hometeamid = Team.objects.get(teamid = currentMatch['idHomeTeam'])
            except:
                 problemid = currentMatch['idHomeTeam']
                 teamData(problemid)
                 instance.hometeamid = Team.objects.get(teamid = currentMatch['idHomeTeam'])
            try:
                instance.awayteamid = Team.objects.get(teamid = currentMatch['idAwayTeam'])
            except:
                 problemid = currentMatch['idAwayTeam']
                 teamData(problemid)
                 instance.awayteamid = Team.objects.get(teamid = currentMatch['idAwayTeam'])

            instance.save()
            print(f"{x}/{entries} done")
    

class Command(BaseCommand):
    def handle(self, *args, **options):
        getMatches(4328)