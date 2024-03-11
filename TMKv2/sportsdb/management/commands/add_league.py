from django.core.management.base import BaseCommand
from .get_leagues import getLeaguesFromLeague, getLeagueData, filterleagues
from .get_teams import teamsData
from .get_matches import getMatches

def add_leagues_and_teams(leagueid):
    leagues = getLeaguesFromLeague(leagueid)
    filtered = filterleagues(leagues)
    getLeagueData(filtered)
    teamsData(leagueid)
    getMatches(leagueid)


class Command(BaseCommand):
    def handle(self, *args, **options):
        add_leagues_and_teams(4332)