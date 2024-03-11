import requests
from django.core.management.base import BaseCommand
from sportsdb.models import League, Team
from .get_leagues import getLeagueData
import environ
env = environ.Env()
environ.Env.read_env("TMKv2\\TMKv2\\.env")

def teamData(teamid_to_add: int):
    print(f"Calling API for {teamid_to_add}")
    response = requests.get(f"https://www.thesportsdb.com/api/v1/json/{env("API_KEY")}/lookupteam.php?id={teamid_to_add}")
    data = response.json()
    for team in data['teams']:
        instance = Team(teamid = team['idTeam'],
                        teamname = team['strTeam'],
                        altteamname = team['strAlternate'],
                        teamdescription = team['strDescriptionEN'],
                        teamcountry = team['strCountry'],
                        teamstadium = team['strStadium'],
                        teamgender = team['strGender'],
                        teamsport = team['strSport'],
                        teambadge = team['strTeamBadge'],
                        )
        id_key = 'idLeague'
        league_id = team.get(id_key)
        try:
            primaryleague = League.objects.get(leagueid=league_id)
        except:
            listid = [league_id]
            getLeagueData(listid)
            primaryleague = League.objects.get(leagueid=league_id)
        instance.primaryleague = primaryleague
        instance.save()
        print(f"{instance} inserted in DB")
        instance.leagues.add(primaryleague)
        print(f"{primaryleague} added to {instance}")
        for j in range(2, 8):
            id_key = 'idLeague' + str(j)
            league_id = team.get(id_key)
            if league_id is not None:
                league = League.objects.get(leagueid=league_id)
                instance.leagues.add(league)
                print(f"{league} added to {instance}")

class Command(BaseCommand):
    def handle(self, *args, **options):
        teamData(137947)