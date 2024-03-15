import requests
from django.core.management.base import BaseCommand
from sportsdb.models import Match, League, Team, Standing
from django.db.models import Q
from datetime import datetime, timedelta
import environ
from django.db.models import Avg
from users.models import Profile
from emails.email_sender import sendEmails

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


class Command(BaseCommand):
    def handle(self, *args, **options):
        sendEmails()
