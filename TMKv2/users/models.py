from django.db import models
from sportsdb.models import Team

# Create your models here.

class User(models.Model):
    userid = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=255)
    useremail = models.CharField(max_length=255, unique=True)
    userteams = models.ManyToManyField(Team, related_name = 'teams')

    class Meta:
        app_label = 'users'

    def __str__(self):
        return self.username