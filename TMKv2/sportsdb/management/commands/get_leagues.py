import environ
env = environ.Env()
environ.Env.read_env("TMKv2\\TMKv2\\.env")
import requests
from django.core.management.base import BaseCommand
from sportsdb.models import League


def getLeaguesFromLeague(leagueid: int):
    uniqueleagueids = set()
    uniqueleagueids.add(leagueid)
    print(f"Calling API for {leagueid}")
    response = requests.get(f"https://www.thesportsdb.com/api/v1/json/{env("API_KEY")}/lookup_all_teams.php?id={leagueid}")
    data = response.json()
    for team in data['teams']:
        id_key = 'idLeague'
        league_id = team.get(id_key)
        league_id = int(league_id)
        uniqueleagueids.add(league_id)
        for j in range(2, 8):
            id_key = 'idLeague' + str(j)
            league_id = team.get(id_key)
            if league_id is not None:
                league_id = int(league_id)
                uniqueleagueids.add(league_id)
    print(uniqueleagueids)
    return uniqueleagueids

def filterleagues(leagues: set):
    leagueids = League.objects.values_list('leagueid', flat=True)
    filteredleagues = [league for league in leagues if league not in leagueids]
    print(filteredleagues)
    return filteredleagues

def getLeagueData(leagueids: list):
    for leagueid in leagueids:
        print(f"Calling API for {leagueid}")
        response = requests.get(f"https://www.thesportsdb.com/api/v1/json/{env("API_KEY")}/lookupleague.php?id={leagueid}")
        data = response.json()
        print(f"Parsing JSON for {leagueid}")
        currentLeague = data['leagues'][0]
        instance = League(leagueid = currentLeague['idLeague'], 
                          leaguename = currentLeague['strLeague'],
                          altleaguename = currentLeague['strLeagueAlternate'],
                          leaguedescription = currentLeague['strDescriptionEN'],
                          leaguecountry = currentLeague['strCountry'],
                          seasonformat = currentLeague['strCurrentSeason'],
                          leaguesport = currentLeague['strSport'],
                          leaguebadge = currentLeague['strBadge'])
        instance.save()
        print(f"{instance} is in DB")

class Command(BaseCommand):
    def handle(self, *args, **options):
        leagueids = getLeaguesFromLeague(4485) # One LeagueID, all adjacent leagues will be added
        filterleagues(leagueids)