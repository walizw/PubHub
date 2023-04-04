from rest_framework.response import Response
from rest_framework import generics, status

from django.conf import settings

from ..models import ActivityUser


class WellKnownAPIView (generics.GenericAPIView):
    """The .well-known/webfinger view."""

    def get(self, request):
        """Get the webfinger of a specified user."""
        if request.GET.get("resource") is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # check if the account exists
        acct_name = request.GET.get("resource")[5:].split("@")
        users = ActivityUser.objects.filter(username=acct_name[0])
        if len(users) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # return the webfinger
        res = Response({
            "subject": f"acct:{acct_name[0]}@{acct_name[1]}",
            "links": [
                {
                    "rel": "self",
                    "type": "application/activity+json",
                    "href": f"{settings.AP_HOST}/api/v1/users/{acct_name[0]}"
                }
            ]
        })
        res.headers["Content-Type"] = "application/jrd+json"
        return res
