from django.core.management.base import BaseCommand
from sportsdb.models import Match, Standing
from users.models import Profile
from django.db.models import Q
from datetime import datetime, timedelta
from .mailjet import sendEmail

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

def usersAndTeams():
    profiles = Profile.objects.all()
    profileandteams = {}
    for profile in profiles:
        teams = profile.teams.all()
        team_ids = [team.teamid for team in teams]
        profileandteams[profile.id] = team_ids
    return profileandteams

def getUserData(id):
    userinfo_queryset = Profile.objects.filter(id=id).values('name', 'email')
    userinfo = userinfo_queryset[0]
    user = {'name': userinfo['name'],
         'email': userinfo['email']}
    return user

def generateEmailData(user, usersandteams):
    emaildata = {}
    emaildata['userinfo'] = getUserData(user)
    userteamlist = usersandteams[user]
    matches = []
    for team in userteamlist:
        matchlist = weeklyMatchesByTeam(team)
        emailcontent = addDataToMatches(matchlist)
        matches.append(emailcontent)
    emaildata['matches'] = matches
    return emaildata


def generate_html_block(matches_data):
    html = "<div>"
    for match_set in matches_data:
        for match in match_set:
            html += "<div>"
            html += f"<h3>{match['hometeam']} ({match['homerank']}) vs {match['awayteam']} ({match['awayrank']})</h3>"
            html += f"<p>{match['homeform']} {match['awayform']}</p>"
            html += f"<p>{match['league']}</p>"
            html += f"<p>Stadium: {match['venue']}</p>"
            html += f"<p>Date: {match['date'].strftime('%d/%m/%Y')}, {match['time']}</p>"
            html += "<hr></div>"
    html += "</div>"

    with open("match_info.html", "w") as file:
        file.write(html)
    print("Match information has been saved to match_info.html")


class Command(BaseCommand):
    def handle(self, *args, **options):
        pass