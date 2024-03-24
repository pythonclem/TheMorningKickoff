from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer, TeamSerializer, MatchSerializer, LeagueSerializer
from users.models import Profile, User
from sportsdb.models import Team, Match, League
from sportsdb.views import getMatches
from datetime import date
from django.db.models import Q
from django.shortcuts import get_object_or_404
import requests
from django.utils.timezone import now
import environ
env = environ.Env()
environ.Env.read_env("TMKv2\\TMKv2\\.env")


class UserView(APIView):

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            try:
                profile = Profile.objects.filter(id=pk).first()
            except:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)    

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            try:
                team_ids = request.data.pop('teams', [])
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    user = serializer.save()
                    profile = Profile.objects.get(user=user)
                    profile.teams.set(team_ids)
                    return Response({"message": "User created successfully"}, status=201)
            except Exception as e:
                return Response({"error": str(e)}, status=400)
            
    def put(self, request, pk=None, *args, **kwargs):
        user = get_object_or_404(User, id=pk)        
        with transaction.atomic():
            try:
                team_ids = request.data.pop('teams', [])
                serializer = UserSerializer(instance=user, data=request.data)
                if serializer.is_valid(raise_exception=True):
                    user = serializer.save()
                    profile = Profile.objects.get(user=user)
                    profile.teams.set(team_ids)
                    return Response({"message": "User updated successfully"}, status=200)
            except Exception as e:
                return Response({"error": str(e)}, status=400)

    def delete(self, request, pk=None, *args, **kwargs):
        with transaction.atomic():
            if not pk:
                return Response({"message": "Method DELETE is not allowed without an ID."}, status=status.HTTP_400_BAD_REQUEST)
            profile = Profile.objects.filter(id=pk).first()
            if profile:
                profile.delete()
                return Response({"message": "User deleted."}, status=status.HTTP_204_NO_CONTENT)
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        

class TeamView(APIView):

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
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
        else:
            teams = Team.objects.filter(primaryleague__teamdata=True)
            serializer = TeamSerializer(teams, many=True)
            return Response(serializer.data)
        

class LeagueView(APIView):
    
    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            try:
                league = League.objects.get(leagueid=pk)
            except:
                return Response({"message": "League not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = LeagueSerializer(league)
            return Response(serializer.data)
        leagues = League.objects.all()
        serializer = LeagueSerializer(leagues, many=True)
        return Response(serializer.data)  
    


class ScoreUpdaterView(APIView):

    def put(self, request, *args, **kwargs):
            
        leagues = League.objects.filter(teamdata=True)
        apiresponse = []

        for league in leagues:
            season = league.seasonformat
            print(f"Getting matches for {league.leagueid}, {season}")
            response = requests.get(f"https://www.thesportsdb.com/api/v1/json/{env("API_KEY")}/eventsseason.php?id={league.leagueid}&s={season}")
            data = response.json()
            matches_to_update = Match.objects.filter(leagueid=league, date__lt=now(), homescore__isnull=True)
            print(f"Found {matches_to_update.count()} matches to update")
            scores_to_update = []

            for game in matches_to_update:
                for match in data.get("events", []):
                    if str(game.matchid) == match['idEvent']:
                        game.homescore = match['intHomeScore']
                        game.awayscore = match['intAwayScore']
                        game.video = match['strVideo']
                        scores_to_update.append(game)
                        break

            if scores_to_update:
                with transaction.atomic():
                    Match.objects.bulk_update(scores_to_update, ['homescore', 'awayscore', 'video'])
                    apiresponse.append(f"Updated {len(scores_to_update)} matches for {league.leaguename}")
        return Response({"message": apiresponse})
    


class DateTimeUpdaterView(APIView):

    def put(self, request, *args, **kwargs):
            
        leagues = League.objects.filter(teamdata=True)
        apiresponse = []

        for league in leagues:
            season = league.seasonformat
            print(f"Getting matches for {league.leagueid}, {season}")
            response = requests.get(f"https://www.thesportsdb.com/api/v1/json/{env("API_KEY")}/eventsseason.php?id={league.leagueid}&s={season}")
            data = response.json()
            matches_to_update = Match.objects.filter(leagueid=league, date__gt=now(), homescore__isnull=True)
            print(f"Found {matches_to_update.count()} matches to update")
            scores_to_update = []

            for game in matches_to_update:
                for match in data.get("events", []):
                    if str(game.matchid) == match['idEvent']:
                        if str(game.date) != match['dateEvent'] and str(game.time) != match['strTime']:
                            game.date = match['dateEvent']
                            game.time = match['strTime']
                            scores_to_update.append(game)
                            break

            if scores_to_update:
                with transaction.atomic():
                    Match.objects.bulk_update(scores_to_update, ['date', 'time'])
                    apiresponse.append(f"Updated {len(scores_to_update)} matches for {league.leaguename}")
        return Response({"message": apiresponse})
    

class MatchAdderView(APIView):

    def post(self, request, *args, **kwargs):
            
        leagues = League.objects.filter(teamdata=True)
        for league in leagues:
            getMatches(league.leagueid)
        return Response({"message": "Matches Updated"})