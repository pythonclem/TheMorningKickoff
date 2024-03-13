from django.db import models
from sportsdb.models import Team
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
# Create your models here.
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True, unique=True)
    teams = models.ManyToManyField(Team, related_name = 'teams')

    class Meta:
        app_label = 'users'

    def __str__(self):
        return str(self.user.username)

