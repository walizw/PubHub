from rest_framework.response import Response
from rest_framework import generics, status

from django.conf import settings

from ..models import ActivityUser

from ..utils import discovery
from ..utils import users as ap_users

import json


class UserAPIView (generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        username = kwargs.get("username")

        # check if the account exists
        users = ActivityUser.objects.filter(username=username)
        if len(users) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # return the user
        res = Response({
            "@context": [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/v1"
            ],
            "id": "https://" + settings.AP_HOST + "/api/v1/users/" + username,
            "type": "Person",
            "preferredUsername": username,
            "inbox": "https://" + settings.AP_HOST + "/api/v1/users/" + username + "/inbox",
            "outbox": "https://" + settings.AP_HOST + "/api/v1/users/" + username + "/outbox",
            "followers": "https://" + settings.AP_HOST + "/api/v1/users/" + username + "/followers",
            "following": "https://" + settings.AP_HOST + "/api/v1/users/" + username + "/following",
            "publicKey": {
                "id": "https://" + settings.AP_HOST + "/api/v1/users/" + username + "#main-key",
                "owner": "https://" + settings.AP_HOST + "/api/v1/users/" + username,
                "publicKeyPem": users[0].pub_key,
            },
            "endpoints": {
                "sharedInbox": "https://" + settings.AP_HOST + "/api/v1/inbox"
            }
        }, status=status.HTTP_200_OK)

        res.content_type = "application/activity+json"
        return res


class InboxAPIView (generics.GenericAPIView):
    media_type = "application/activity+json"

    def get(self, request, *args, **kwargs):
        # TODO: Get inbox
        return Response("TODO: This", status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # print the request
        print(f"Posted to inbox:\n{request.data}")

        username = kwargs.get("username")
        users = ActivityUser.objects.filter(username=username)

        if len(users) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        act = json.loads(request.data.decode("utf-8"))

        if act.get("type") == "Follow":
            users[0].followers += 1
            users[0].save()

            # send an accept request
            if not ap_users.send_accept(users[0], act):
                return Response("Error sending accept", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response("Followed", status=status.HTTP_200_OK)
        elif act.get("type") == "Accept":
            if not ap_users.process_accept(users[0], act):
                return Response("Error processing accept", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response("Accepted", status=status.HTTP_200_OK)
        elif act.get("type") == "Undo":
            if not ap_users.process_undo(users[0], act):
                return Response("Error processing undo", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response("Undo", status=status.HTTP_200_OK)

        return Response("Malformed request", status=status.HTTP_400_BAD_REQUEST)


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

        if request.data.get("type") == "Create":
            return Response("TODO: Create", status=status.HTTP_200_OK)
        elif request.data.get("type") == "Follow":
            user = request.data.get("to")
            user, host = ap_users.parse_user(user)

            if not user:
                return Response("Malformed request", status=status.HTTP_200_OK)

            user_data = discovery.discover_user(user, host)
            if user_data is None:
                return Response("User not found", status=status.HTTP_200_OK)

            if ap_users.follow(users[0], user_data):
                return Response("Followed", status=status.HTTP_200_OK)
        elif request.data.get("type") == "Unfollow":
            user = request.data.get("to")
            user, host = ap_users.parse_user(user)

            if not user:
                return Response("Malformed request", status=status.HTTP_200_OK)

            user_data = discovery.discover_user(user, host)
            if user_data is None:
                return Response("User not found", status=status.HTTP_200_OK)

            if ap_users.unfollow(users[0], user_data):
                return Response("Unfollowed", status=status.HTTP_200_OK)
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
