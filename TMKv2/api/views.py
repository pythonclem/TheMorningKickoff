from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TeamSerializer
from sportsdb.models import Team

@api_view(['GET'])
def getTeams(request):
    teams = Team.objects.filter(primaryleague__teamdata=True)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)