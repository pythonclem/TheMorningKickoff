from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import TeamSerializer, UserSerializer, MatchSerializer
from sportsdb.models import Team, Match
from users.models import Profile
from datetime import date
from django.db.models import Q

@api_view(['GET'])
def getTeams(request):
    teams = Team.objects.filter(primaryleague__teamdata=True)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def getTeam(request, pk):
    try:
        team = Team.objects.get(teamid=pk)
    except:
        return Response({"error": "Team not found"}, status=404)
    last_10_matches = Match.objects.filter(
        (Q(hometeamid=pk) | Q(awayteamid=pk)) & Q(date__lt=date.today())
        ).order_by('-date')[:10]

    team_serializer = TeamSerializer(team, many=False)
    matches_serializer = MatchSerializer(last_10_matches, many=True)
    response_data = {
        'team': team_serializer.data,
        'last_10_matches': matches_serializer.data
    }
    return Response(response_data)

@api_view(['POST'])
def createUser(request):
    try:
        team_ids = request.data.pop('teams', [])
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            profile = Profile.objects.get(user=user)
            profile.teams.set(team_ids)
            return Response({"message": "User created successfully"})
        else:
            return Response(serializer.errors)
    except Exception as e:
        return Response({"error": str(e)})

