from rest_framework.response import Response
from rest_framework import generics, status

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
            "id": request.build_absolute_uri("/api/v1/users/" + username),
            "type": "Person",
            "preferredUsername": username,
            "inbox": request.build_absolute_uri("/api/v1/users/" + username + "/inbox"),
            "outbox": request.build_absolute_uri("/api/v1/users/" + username + "/outbox"),
            "followers": request.build_absolute_uri("/api/v1/users/" + username + "/followers"),
            "following": request.build_absolute_uri("/api/v1/users/" + username + "/following"),
            "publicKey": {
                "id": request.build_absolute_uri("/api/v1/users/" + username + "#main-key"),
                "owner": request.build_absolute_uri("/api/v1/users/" + username),
                "publicKeyPem": users[0].pub_key,
            },
            "endpoints": {
                "sharedInbox": request.build_absolute_uri("/api/v1/inbox")
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
        # TODO: Post to outbox
        return Response("TODO: This", status=status.HTTP_200_OK)


class FollowersAPIView (generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # TODO: Get followers
        return Response("TODO: This", status=status.HTTP_200_OK)


class FollowingAPIView (generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # TODO: Get following
        return Response("TODO: This", status=status.HTTP_200_OK)
