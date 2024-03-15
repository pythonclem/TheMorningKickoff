from django.core.management.base import BaseCommand
from sportsdb.models import Match, League, Team, Standing
from django.db.models import Q
import environ
from django.db.models import Avg

env = environ.Env()
environ.Env.read_env("TMKv2\\TMKv2\\.env")

def teamScorePosition(teamid):
    teamstanding = Standing.objects.filter(team=teamid).latest('standingtime')
    if teamstanding.rank == 1:
        stakes = 100
    else:
        stakes = 100 - (teamstanding.rank - 1)*4
    average_goalsfor = Standing.objects.filter(standingtime=teamstanding.standingtime, league=teamstanding.league
                                        ).aggregate(avg_goalsfor=Avg('goalsfor'))['avg_goalsfor']
    if teamstanding.goalsfor / average_goalsfor >= 1.3:
         attfootball = 100
    else:
         attfootball = 75 * (teamstanding.goalsfor / average_goalsfor)

    teamScore = stakes * 0.7 + attfootball * 0.3
    league_multipliers = {
        4328: 1,
        4335: 0.97,
        4331: 0.95,
        4332: 0.95,
        4334: 0.93,
        4337: 0.9,
        4344: 0.87
    }
    league_id = teamstanding.league_id
    league_multiplier = league_multipliers.get(league_id)
    
    teamScore = stakes * 0.7 + attfootball * 0.3
    teamScore *= league_multiplier
    
    teamScore = round(teamScore, 1)
    return teamScore

def teamScorePoints(teamid):
    teamstanding = Standing.objects.filter(team=teamid).latest('standingtime')
    rankoneteam = Standing.objects.filter(league_id = teamstanding.league, rank = 1).latest('standingtime')
    if teamstanding.points / rankoneteam.points  == 1:
        stakes = 100
    else:
        stakes = 100*(teamstanding.points/rankoneteam.points)
    average_goalsfor = Standing.objects.filter(standingtime=teamstanding.standingtime, league=teamstanding.league
                                        ).aggregate(avg_goalsfor=Avg('goalsfor'))['avg_goalsfor']
    if teamstanding.goalsfor / average_goalsfor >= 1.3:
         attfootball = 100
    else:
         attfootball = 75 * (teamstanding.goalsfor / average_goalsfor)
    teamScore = stakes * 0.7 + attfootball * 0.3
    teamScore = round(teamScore, 1)
    return teamScore


def generateMatchScores(startdate, enddate):
    matches = Match.objects.filter(date__range=[startdate, enddate], leagueid__in=[4328])
    for game in matches:
        hometeamscore = teamScorePosition(game.hometeamid)
        awayteamscore = teamScorePosition(game.awayteamid)
        matchscore = round((hometeamscore + awayteamscore)/2, 1)
        print(f"{matchscore}: {game.hometeam}, {hometeamscore} - {game.awayteam}, {awayteamscore}")

def sortedMatchScoresPosition(startdate, enddate):
    matches = Match.objects.filter(date__range=[startdate, enddate], leagueid__in=[4328, 4331, 4332, 4334, 4335, 4337, 4344])
    match_scores = []
    for game in matches:
        hometeamscore = teamScorePosition(game.hometeamid)
        awayteamscore = teamScorePosition(game.awayteamid)
        if hometeamscore > awayteamscore:
            matchscore = round((hometeamscore*0.7 + awayteamscore*0.3), 1)
            match_scores.append((game, matchscore))
        else:
            matchscore = round((hometeamscore*0.3 + awayteamscore*0.7), 1)
            match_scores.append((game, matchscore))
    sorted_matches = sorted(match_scores, key=lambda x: -x[1])
    for game, matchscore in sorted_matches:
        print(f"{matchscore}: {game.hometeam} - {game.awayteam}")


class Command(BaseCommand):
    def handle(self, *args, **options):
        sortedMatchScoresPosition('2024-03-01', '2024-03-31')