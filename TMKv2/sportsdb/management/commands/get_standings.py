import requests
from django.core.management.base import BaseCommand
from sportsdb.models import League, Team, Standing
import environ
env = environ.Env()
environ.Env.read_env("TMKv2\\TMKv2\\.env")

def getStandings(id: int):
     
    league_instance = League.objects.get(leagueid=id)
    season = league_instance.seasonformat    
    print(f"Calling API for {league_instance.leaguename}")
    response = requests.get(f"https://www.thesportsdb.com/api/v1/json/{env("API_KEY")}/lookuptable.php?l={id}&s={season}")
    data = response.json()
    for team in data.get("table", []):
        try:
            if Standing.objects.get(standingid = team['idStanding']):
                print(f"Standing already in DB")
        except:
            instance = Standing(
            standingid = team['idStanding'],
            rank = team['intRank'],
            form = team['strForm'],
            played = team['intPlayed'],
            season = team['strSeason'],
            wins = team['intWin'],
            losses = team['intLoss'],
            draws = team['intDraw'],
            goalsfor = team['intGoalsFor'],
            goalsagainst = team['intGoalsAgainst'],
            goaldiff = team['intGoalDifference'],
            points = team['intPoints'],
            standingtime = team['dateUpdated']
            )
            instance.league = League.objects.get(leagueid = team['idLeague'])
            instance.team = Team.objects.get(teamid = team['idTeam'])
            instance.save()
            print(f"{instance.rank}, {instance.team} added to DB")
    


class Command(BaseCommand):
    def handle(self, *args, **options):
        getStandings(4328)