import requests
from django.core.management.base import BaseCommand
from sportsdb.models import Match, League, Team, Standing
from django.db.models import Q
from datetime import datetime, timedelta
import environ
from django.db.models import Avg
from users.models import Profile
from emails.email_sender import sendEmails
from django.db import transaction

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


def usersAndTeams():
    profiles = Profile.objects.all()
    profileandteams = {}
    for profile in profiles:
        teams = profile.teams.all()
        team_ids = [team.teamid for team in teams]
        profileandteams[profile.id] = team_ids
    return profileandteams

def weeklyMatchesByTeam(teamid):
    tomorrow = datetime.now() + timedelta(days=1)
    six_days_from_now = datetime.now() + timedelta(days=6)
    matchlist = Match.objects.filter(Q(hometeamid=teamid) | Q(awayteamid=teamid), 
                                   date__range=[tomorrow, six_days_from_now]).values(
                                       'date', 'hometeam','hometeamid', 'awayteam', 'awayteamid', 'league', 'venue', 'time')
    return matchlist

def addDataToMatches(matchlist: list):
    for event in matchlist:
        homestanding = Standing.objects.filter(team=event['hometeamid']).values(
                                    'rank', 'form').latest('standingtime')
        awaystanding = Standing.objects.filter(team=event['awayteamid']).values(
                                    'rank', 'form').latest('standingtime')
        event['homerank'] = homestanding['rank']
        event['homeform'] = homestanding['form']
        event['awayrank'] = awaystanding['rank']
        event['awayform'] = awaystanding['form']

    print(matchlist)


def generateEmailData():
    usersandteams = usersAndTeams()
    for user in usersandteams:
        userinfo = Profile.objects.filter(id=user).values('name', 'email')
        print(userinfo)
        userteamlist = usersandteams[user]
        for team in userteamlist:
            matchlist = weeklyMatchesByTeam(team)
            addDataToMatches(matchlist)
        
        


def generate_html_block(matches_data):
    html = "<div>"
    for match_set in matches_data:
        for match in match_set:
            html += "<div>"
            html += f"<p>Date: {match['date'].strftime('%Y-%m-%d')}</p>"
            html += f"<p>Home Team: {match['hometeam']}</p>"
            html += f"<p>Away Team: {match['awayteam']}</p>"
            html += f"<p>League: {match['league']}</p>"
            html += f"<p>Venue: {match['venue']}</p>"
            html += f"<p>Time: {match['time']}</p>"
            html += f"<p>Home Rank: {match['homerank']}</p>"
            html += f"<p>Home Form: {match['homeform']}</p>"
            html += f"<p>Away Rank: {match['awayrank']}</p>"
            html += f"<p>Away Form: {match['awayform']}</p>"
            html += "</div>"
    html += "</div>"

    with open("match_info.html", "w") as file:
        file.write(html)
    print("Match information has been saved to match_info.html")


import requests
from django.core.management.base import BaseCommand
from sportsdb.models import Match, League, Team
from .get_team import teamData
import environ
env = environ.Env()
environ.Env.read_env("TMKv2\\TMKv2\\.env")

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
            video=match['strVideo'],
            status=match['strStatus'],
            postponed=match['strPostponed'],
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
    


def addStatusPostponed():

    leagues = League.objects.filter(teamdata=True)
    for league in leagues:
        try:
            season = league.seasonformat
            print(f"Populating S&P {league.leagueid}")
            response = requests.get(f"https://www.thesportsdb.com/api/v1/json/{env("API_KEY")}/eventsseason.php?id={league.leagueid}&s={season}")
            data = response.json()
            matches_to_update = Match.objects.all()
            bulk_update = []
            for game in matches_to_update:
                for match in data.get("events", []):
                    if str(game.matchid) == match['idEvent']:
                        game.status = match['strStatus']
                        game.postponed = match['strPostponed']
                        bulk_update.append(game)
                        break
        except:
            print(f"{league.leaguename} is a SHIT LEAGUE")
        if bulk_update:
            with transaction.atomic():
                Match.objects.bulk_update(bulk_update, ['status', 'postponed'])
                print(f"{league.leaguename} succesfully populated S&P")





class Command(BaseCommand):
    def handle(self, *args, **options):
        addStatusPostponed()













