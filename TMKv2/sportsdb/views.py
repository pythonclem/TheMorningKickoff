import environ
env = environ.Env()
environ.Env.read_env("TMKv2\\TMKv2\\.env")
import requests
from django.shortcuts import render
from django.contrib import messages
from .models import League, Team, Match, Standing
from .forms import AddLeagueForm
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

def addLeague(request):
    form = AddLeagueForm(request.POST)
    if request.method == 'POST':
        form = AddLeagueForm(request.POST)
        if form.is_valid():
            pk = request.POST['teamid']
            messages.success(request, 'Getting Leagues')
            leagues = getLeaguesFromLeague(pk)
            filtered = filterleagues(leagues)
            messages.success(request, 'Getting League Data')
            getLeagueData(filtered)
            messages.success(request, 'Getting Teams Data')
            teamsData(pk)
            messages.success(request, 'Getting Match Data')
            getMatches(pk)
            messages.success(request, 'Getting Standings Data')
            getStandings(pk)
            messages.success(request, 'League Added')
    return render(request, 'sportsdb/addleague.html', {'form': form})

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
            video=match['strVideo']
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
    
