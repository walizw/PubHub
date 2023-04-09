from rest_framework.response import Response
from rest_framework import generics, status

from ..models import Activity, Note, Profile
from ..utils import discovery

import json


class InstanceInboxAPIView (generics.GenericAPIView):
    media_type = "application/activity+json"

    def post(self, request, format=None):
        print(f"Instance inbox got activity: {request.data}")
        data_json = json.loads(request.data)

        if data_json["type"] == "Create":
            act = Activity()
            act.id = data_json["id"]
            act.type = data_json["type"]
            act.actor = data_json["actor"]
            act.object = data_json["object"]
            act.to = data_json["to"]
            act.cc = data_json["cc"]
            act.published = data_json["published"]
            act.save()

            act_object = data_json["object"]
            if act_object["type"] == "Note":
                actor_profile = Profile.objects.get(id=act.actor)
                if actor_profile is None:
                    # TODO: Convert the actor url to a profile id
                    # In the format of @username@domain.tld and call discover
                    # on that user, so it creates a profile. For now, return
                    # unimplemented
                    return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

                note = Note()
                note.id = act_object["id"]
                note.actor = actor_profile
                note.content = act_object["content"]
                note.published = act_object["published"]
                note.tags = act_object["tag"]
                note.save()

                return Response("Posted", status=status.HTTP_201_CREATED)
        elif act_json["type"] == "Delete":
            # TODO: Delete external posts
            pass
        return Response("Unimplemented", status=status.HTTP_501_NOT_IMPLEMENTED)
