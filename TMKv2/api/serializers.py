from rest_framework import serializers
from sportsdb.models import League, Team, Match
from users.models import User, Profile

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["teamid", "teamname", "teambadge", "altteamname", "teamsport"]

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate_email(self, value):
        value = serializers.EmailField().run_validation(value)
        if User.objects.filter(email__iexact=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['username', 'email', 'teams']


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['hometeam', 'awayteam', 'homescore', 'awayscore', 'league', 'date']