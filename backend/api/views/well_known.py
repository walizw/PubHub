from rest_framework.response import Response
from rest_framework import generics, status

from ..models import ActivityUser


class WellKnownAPIView (generics.GenericAPIView):
    """The .well-known/webfinger view."""

    def get(self, request):
        """Get the webfinger of a specified user."""
        if request.GET.get("resource") is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # check if the account exists
        acct_name = request.GET.get("resource")[5:].split("@")[0]
        users = ActivityUser.objects.filter(username=acct_name)
        if len(users) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # return the webfinger
        return Response({
            "subject": "acct:" + acct_name + "@" + request.get_host(),
            "links": [
                {
                    "rel": "self",
                    "type": "application/activity+json",
                    "href": request.build_absolute_uri("/api/v1/users/" + acct_name)
                }
            ]
        }, headers={"Content-Type": "application/jrd+json"}, status=status.HTTP_200_OK)
