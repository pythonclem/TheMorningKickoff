import requests
from django.core.management.base import BaseCommand
from sportsdb.models import Match, League, Team
from .get_team import teamData
from django.utils.timezone import now
import environ
env = environ.Env()
environ.Env.read_env("TMKv2\\TMKv2\\.env")

def updateScores():
     
    leagues = League.objects.filter(teamData=True)
    for league in leagues:
        season = league.seasonformat
        print(f"Getting matches for {league.leagueid}, {season}")
        response = requests.get(f"https://www.thesportsdb.com/api/v1/json/{env("API_KEY")}/eventsseason.php?id={league.leagueid}&s={season}")
        data = response.json()
        matches_to_update = Match.objects.filter(leagueid=league, date__lt=now(), homescore__isnull=True)
        scores_to_update = []
        for game in matches_to_update:    
            for match in data.get("events", []):
                if game.matchid == match['idEvent']:
                    game.homescore = match['intHomeScore']
                    game.awayscore = match['intAwayScore']
                    game.video = match['strVideo']
                    scores_to_update.append(game)
                    break
        Match.objects.bulk_update(scores_to_update, ['homescore', 'awayscore', 'video'])