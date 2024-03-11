from rest_framework import serializers
from sportsdb.models import League, Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["teamid", "teamname"]