from django.core.management.base import BaseCommand
from sportsdb.models import Match, Standing
from users.models import Profile
from django.db.models import Q
from datetime import datetime, timedelta

def usersAndTeams():
    profiles = Profile.objects.all()
    usersandteams = {}
    for profile in profiles:
        teams = profile.teams.all()
        team_ids = [team.teamid for team in teams]
        team_names = [team.teamname for team in teams]
        usersandteams[profile.id] = {
            'team_ids': team_ids,
            'team_names': team_names
        }
    return usersandteams

def getUserData(id):
    userinfo_queryset = Profile.objects.filter(id=id).values('name', 'email')
    userinfo = userinfo_queryset[0]
    user = {'name': userinfo['name'],
         'email': userinfo['email']}
    return user

def weeklyMatchesByTeam(teamid):
    tomorrow = datetime.now() + timedelta(days=1)
    six_days_from_now = datetime.now() + timedelta(days=18)
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

    return matchlist



def generateEmailData(user, usersandteams):
    emaildata = {}
    emaildata['userinfo'] = getUserData(user)
    userteamlist = usersandteams[user]['team_ids']
    userteamnames = usersandteams[user]['team_names']
    emaildata['userteams'] = userteamnames
    matches = []
    for team in userteamlist:
        matchlist = weeklyMatchesByTeam(team)
        emailcontent = addDataToMatches(matchlist)
        matches.append(emailcontent)
    emaildata['matches'] = matches
    return emaildata