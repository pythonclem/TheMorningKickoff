import requests
from django.core.management.base import BaseCommand
from sportsdb.models import Match, League, Team
from django.db.models import Q
from datetime import datetime, timedelta
import environ

env = environ.Env()
environ.Env.read_env("TMKv2\TMKv2\.env")

def getLeaguesFromLeague(leagueid: int):
    uniqueleagueids = set()
    uniqueleagueids.add(leagueid)
    print(f"Calling API for {leagueid}")
    response = requests.get(f"https://www.thesportsdb.com/api/v1/json/{env("API_KEY")}/lookup_all_teams.php?id={leagueid}")
    data = response.json()
    print(data)

def findGamesPerTeam(teamname):
    six_days_from_now = datetime.now() + timedelta(days=6)

    team_id = Team.objects.get(teamname = teamname)
    matches = Match.objects.filter(
    (Q(hometeamid=team_id) | Q(awayteamid=team_id)) & Q(date__range = (datetime.now(), six_days_from_now))
    )
    for match in matches:
        print(f"{match.league}, {match}, {match.date}")


def getgoodteams():
    teams = Team.objects.filter(primaryleague__teamdata=True)
    print(len(teams))
    for team in teams:
        print(team)


class Command(BaseCommand):
    def handle(self, *args, **options):
        getLeaguesFromLeague(4335)


