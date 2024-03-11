from django.db import models

# Create your models here.

class League(models.Model):
    leagueid = models.IntegerField(primary_key=True, unique=True, editable=False)
    leaguename = models.CharField(max_length=500)
    altleaguename = models.CharField(null=True, max_length=500)
    leaguedescription = models.TextField(null=True, max_length = 4000)
    leaguecountry = models.CharField(max_length=500)
    seasonformat = models.CharField(max_length=500)
    leaguesport = models.CharField(max_length=500)
    leaguebadge = models.CharField(null=True, max_length=500)
    teamdata = models.BooleanField(default=False)

    class Meta:
        app_label = 'sportsdb'

    def __str__(self):
        return self.leaguename
    

class Team(models.Model):
    teamid = models.IntegerField(primary_key=True, unique=True, editable=False)
    teamname = models.CharField(max_length=500)
    altteamname = models.CharField(null=True, max_length=500)
    primaryleague = models.ForeignKey(League, on_delete=models.CASCADE, related_name='primary_teams')
    teamdescription = models.TextField(null=True, max_length = 4000)
    teamcountry = models.CharField(max_length=500)
    teamstadium = models.CharField(max_length=500)
    teamgender = models.CharField(max_length=500)
    teamsport = models.CharField(max_length=500)
    teambadge = models.CharField(null=True, max_length=500)
    leagues = models.ManyToManyField(League, related_name = 'teams')
    
    class Meta:
        app_label = 'sportsdb'

    def __str__(self):
        return self.teamname
    

class Match(models.Model):
    matchid = models.IntegerField(primary_key=True, unique=True, editable=False)
    matchteams = models.CharField(max_length=255)
    league = models.CharField(max_length=255)
    leagueid = models.ForeignKey(League, on_delete=models.CASCADE)
    matchday = models.IntegerField()
    hometeam = models.CharField(max_length=255)
    awayteam = models.CharField(max_length=255)
    homescore = models.IntegerField(null=True)
    awayscore = models.IntegerField(null=True)
    season = models.CharField(max_length=255)
    date = models.DateField(null=True)
    time = models.CharField(null=True, max_length=255)
    hometeamid = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    awayteamid = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    venue = models.CharField(null=True, max_length=255)
    badge = models.CharField(null=True, max_length=255)
    video = models.CharField(null=True, max_length=255)

    class Meta:
        app_label = 'sportsdb'

    def __str__(self):
        return self.matchteams