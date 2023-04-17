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
                actor_profile = Profile.objects.filter(id=act.actor)
                if len(actor_profile) == 0:
                    discovery.discover_by_user_link(act.actor)

                actor_profile = Profile.objects.get(id=act.actor)
                actor = actor_profile

                note = Note()
                note.id = act_object["id"]
                note.actor = actor
                note.content = act_object["content"]
                note.published = act_object["published"]
                note.tags = act_object["tag"]
                note.save()

                return Response("Posted", status=status.HTTP_201_CREATED)
        elif data_json["type"] == "Delete":

            # if it's not a dict
            if type(data_json["object"]) != dict:
                # check if it's a user
                profile = Profile.objects.filter(id=data_json["object"])
                if len(profile) > 0:
                    profile.delete()
                    return Response("Deleted", status=status.HTTP_200_OK)

                # it's not a user, can it be anything else?
                return Response("Not found", status=status.HTTP_404_NOT_FOUND)

            # get the type of the object
            object_type = data_json["object"]["type"]

            if object_type == "Tombstone":
                post_id = data_json["object"]["id"]
                post = Note.objects.filter(id=post_id)
                if len(post) == 0:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                # create and store the delete activity
                act = Activity()
                act.id = data_json["id"]
                act.type = data_json["type"]
                act.actor = data_json["actor"]
                act.object = data_json["object"]
                act.save()

                # delete the post
                post[0].delete()

                return Response("Deleted", status=status.HTTP_200_OK)
        return Response("Unimplemented", status=status.HTTP_501_NOT_IMPLEMENTED)
