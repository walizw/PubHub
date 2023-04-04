from rest_framework.response import Response
from rest_framework import generics, status

from django.conf import settings

from ..models import ActivityUser


class UserAPIView (generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        username = kwargs.get("username")

        # check if the account exists
        users = ActivityUser.objects.filter(username=username)
        if len(users) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # return the user
        return Response({
            "@context": [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/v1"
            ],
            "id": settings.AP_HOST + "/api/v1/users/" + username,
            "type": "Person",
            "preferredUsername": username,
            "inbox": settings.AP_HOST + "/api/v1/users/" + username + "/inbox",
            "outbox": settings.AP_HOST + "/api/v1/users/" + username + "/outbox",
            "followers": settings.AP_HOST + "/api/v1/users/" + username + "/followers",
            "following": settings.AP_HOST + "/api/v1/users/" + username + "/following",
            "publicKey": {
                "id": settings.AP_HOST + "/api/v1/users/" + username + "#main-key",
                "owner": settings.AP_HOST + "/api/v1/users/" + username,
                "publicKeyPem": users[0].pub_key,
            },
            "endpoints": {
                "sharedInbox": settings.AP_HOST + "/api/v1/inbox"
            }
        }, headers={"Content-Type": "application/activity+json"}, status=status.HTTP_200_OK)


class InboxAPIView (generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # TODO: Get inbox
        return Response("TODO: This", status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # TODO: Post to inbox
        return Response("TODO: This", status=status.HTTP_200_OK)


class OutboxAPIView (generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # TODO: Get outbox
        return Response("TODO: This", status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # check if the account exists
        username = kwargs.get("username")
        users = ActivityUser.objects.filter(username=username)
        if len(users) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # check that the logged-in user is the same as the user in the URL
        if request.user != users[0]:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        # TODO: Post to outbox
        if request.data.get("type") == "Create":
            return Response("TODO: Create", status=status.HTTP_200_OK)
        elif request.data.get("type") == "Follow":
            return Response("TODO: Follow", status=status.HTTP_200_OK)
        elif request.data.get("type") == "Unfollow":
            return Response("TODO: Unfollow", status=status.HTTP_200_OK)
        elif request.data.get("type") == "Accept":
            return Response("TODO: Accept", status=status.HTTP_200_OK)
        elif request.data.get("type") == "Reject":
            return Response("TODO: Reject", status=status.HTTP_200_OK)
        return Response("Malformed request", status=status.HTTP_200_OK)


class FollowersAPIView (generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # TODO: Get followers
        return Response("TODO: This", status=status.HTTP_200_OK)


class FollowingAPIView (generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # TODO: Get following
        return Response("TODO: This", status=status.HTTP_200_OK)
