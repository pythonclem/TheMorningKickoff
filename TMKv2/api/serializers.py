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
        fields = ['username', 'useremail', 'userteams']

    def create(self, validated_data):
        team_ids = validated_data.pop('userteams', []) 
        user = User.objects.create(**validated_data)
        user.userteams.set(team_ids)
        return user