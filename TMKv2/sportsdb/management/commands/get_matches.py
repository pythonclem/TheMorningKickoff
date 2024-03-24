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
    print(f"{len(data.get("events", []))} matches to add")
    for match in data.get("events", []):
        try:
            if Match.objects.get(matchid = match['idEvent']):
                print(f"{match['strEvent']} already in DB")
        except:
            instance = Match(
            matchid=match['idEvent'],
            matchteams=match['strEvent'],
            league=match['strLeague'],
            matchday=match['intRound'],
            hometeam=match['strHomeTeam'],
            awayteam=match['strAwayTeam'],
            homescore=match['intHomeScore'],
            awayscore=match['intAwayScore'],
            season=match['strSeason'],
            date=match['dateEvent'],
            time=match['strTime'],
            venue=match['strVenue'],
            badge=match['strSquare'],
            video=match['strVideo'],
            status=match['strStatus'],
            postponed=match['strPostponed'],
            )
            instance.leagueid = league_instance
            try:
                instance.hometeamid = Team.objects.get(teamid = match['idHomeTeam'])
            except:
                 problemid = match['idHomeTeam']
                 teamData(problemid)
                 instance.hometeamid = Team.objects.get(teamid = match['idHomeTeam'])
            try:
                instance.awayteamid = Team.objects.get(teamid = match['idAwayTeam'])
            except:
                 problemid = match['idAwayTeam']
                 teamData(problemid)
                 instance.awayteamid = Team.objects.get(teamid = match['idAwayTeam'])

            instance.save()
            print(f"{instance} added to DB")
    


class Command(BaseCommand):
    def handle(self, *args, **options):
        getMatches(4337)