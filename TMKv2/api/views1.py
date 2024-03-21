from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, ProfileSerializer
from users.models import Profile, User

class UserView(APIView):

    def get(self, request, pk=None, *args, **kwargs):
        if pk:
            profile = Profile.objects.filter(id=pk).first()
            if profile:
                serializer = ProfileSerializer(profile)
                return Response(serializer.data)
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
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

    def delete(self, request, pk=None, *args, **kwargs):
        with transaction.atomic():
            if not pk:
                return Response({"message": "Method DELETE is not allowed without an ID."}, status=status.HTTP_400_BAD_REQUEST)
            profile = Profile.objects.filter(id=pk).first()
            if profile:
                profile.delete()
                return Response({"message": "User deleted."}, status=status.HTTP_204_NO_CONTENT)
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)