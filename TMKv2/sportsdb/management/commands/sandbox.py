import requests
from django.core.management.base import BaseCommand
from sportsdb.models import Match, League, Team, Standing
from django.db.models import Q
from datetime import datetime, timedelta
import environ
from django.db.models import Avg

env = environ.Env()
environ.Env.read_env("TMKv2\\TMKv2\\.env")

     

def teamScore1(points, points1, goalsscored, averagegoals):
    if points/points1 == 1:
        stakes = 100
    else:
        stakes = 100*(points/points1)
    if goalsscored / averagegoals >= 1.3:
         attfootball = 100
    else:
         attfootball = 75 * (goalsscored / averagegoals)
    teamScore = stakes * 0.7 + attfootball * 0.3
    print (teamScore)
     

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

def getMatchesfromDB(leagueid, startdate, enddate):
    matches = Match.objects.filter(date__range=[startdate, enddate], leagueid__in=[4480])
    for game in matches:
        print(game)


class Command(BaseCommand):
    def handle(self, *args, **options):
        pass