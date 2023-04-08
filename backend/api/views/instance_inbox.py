from rest_framework.response import Response
from rest_framework import generics, status


class InstanceInboxAPIView (generics.GenericAPIView):
    media_type = "application/activity+json"

    def post(self, request, format=None):
        print(f"Instance inbox got activity: {request.data}")
        return Response("Unimplemented", status=status.HTTP_501_NOT_IMPLEMENTED)
