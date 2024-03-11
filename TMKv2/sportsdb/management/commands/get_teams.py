import requests
from django.core.management.base import BaseCommand
from sportsdb.models import League, Team
import environ
env = environ.Env()
environ.Env.read_env("TMKv2\\TMKv2\\.env")

def teamsData(league_id_to_add: int):
    print(f"Calling API for {league_id_to_add}")
    response = requests.get(f"https://www.thesportsdb.com/api/v1/json/{env("API_KEY")}/lookup_all_teams.php?id={league_id_to_add}")
    data = response.json()
    for team in data['teams']:
        try:
            if Team.objects.get(teamid = team['idTeam']):
                print(f"{team['strTeam']} already in DB")
        except:
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
    league_instance = League.objects.get(leagueid=league_id_to_add)
    league_instance.teamdata = True
    league_instance.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        teamsData(4334)