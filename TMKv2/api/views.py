from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TeamSerializer, UserSerializer
from sportsdb.models import Team

@api_view(['GET'])
def getTeams(request):
    teams = Team.objects.filter(primaryleague__teamdata=True)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTeam(request, pk):
    team = Team.objects.get(teamid = pk)
    serializer = TeamSerializer(team, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createUser(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"})
        else:
            return Response(serializer.errors)
    except Exception as e:
        return Response({"error": str(e)})

