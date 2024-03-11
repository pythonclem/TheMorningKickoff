from django.shortcuts import render
from .models import League, Team
# Create your views here.

leagueList = League.objects.all().order_by('leagueid')

def leagues(request):
    context = {'leagues':leagueList}
    return render(request, 'sportsdb/leagues.html', context)

def league(request, pk):
    leagueObj = League.objects.get(leagueid = pk)
    teamsofleague = leagueObj.teams.all()
    return render(request, 'sportsdb/league.html', {'league': leagueObj, 'teams':teamsofleague})

def team(request, pk):
    teamObj = Team.objects.get(teamid = pk)
    team_matches = (teamObj.home_matches.all() | teamObj.away_matches.all()).order_by('date')
    return render(request, 'sportsdb/team.html', {'team': teamObj, 'matches': team_matches})
