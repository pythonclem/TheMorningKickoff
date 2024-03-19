from rest_framework import serializers
from sportsdb.models import League, Team
from users.models import User

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["teamid", "teamname", "teambadge", "altteamname", "teamsport"]

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email']