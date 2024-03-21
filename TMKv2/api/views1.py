from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from users.models import Profile

class CreateUserView(APIView):
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