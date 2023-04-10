from rest_framework import generics, status
from rest_framework.response import Response

from ..models.ActivityUser import ActivityUser

class RegisterAPIVIew (generics.GenericAPIView):
    def post(self, request, format=None):
        data = request.data
        username = data["username"]
        password = data["password"]
        email = data["email"]
        user = ActivityUser.objects.create_user(username, email, password)
        user.save()
        return Response("Registered", status=status.HTTP_201_CREATED)