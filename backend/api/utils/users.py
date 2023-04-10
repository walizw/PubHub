from .discovery import discover_user
from .request import build_signed_request

from ..models import ActivityUser, Activity, DiscoveredInstances, Note, Profile, Follow

from django.conf import settings

import uuid
from datetime import datetime


def parse_user(user: str) -> tuple:
    host = None

    if user is None:
        return (None, None)

    # check if the user is @name@host or just @name
    if len(user.split("@")) == 3:
        host = user.split("@")[2]
        user = user.split("@")[1]
    elif len(user.split("@")) == 2:
        user = user.split("@")[1]
    else:
        return (None, None)

    return (user, host)


def follow(user: ActivityUser, user_data: dict) -> bool:
    external_url = ""

    for link in user_data["links"]:
        if link["rel"] == "self":
            external_url = link["href"]
            break

    follow_activity = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": f"https://{settings.AP_HOST}/api/v1/users/{user.username}/follow/{str(uuid.uuid4())}",
        "type": "Follow",
        "actor": f"https://{settings.AP_HOST}/api/v1/users/{user.username}",
        "object": external_url
    }

    if is_following(follow_activity["actor"], follow_activity["object"]):
        return False

    external_inbox = external_url + \
        "inbox" if external_url[-1] == "/" else external_url + "/inbox"

    # Create the activity
    act = Activity()
    act.id = follow_activity["id"]
    act.type = follow_activity["type"]
    act.actor = follow_activity["actor"]
    act.object = follow_activity["object"]
    act.save()

    req = build_signed_request(
        user, external_inbox, follow_activity)

    if req.status_code < 200 or req.status_code >= 300:
        return False

    return True


def unfollow(user: ActivityUser, user_data: dict) -> bool:
    external_url = ""

    for link in user_data["links"]:
        if link["rel"] == "self":
            external_url = link["href"]
            break

    # Get the activity where `user' followed `external_url'
    act = Activity.objects.filter(
        actor=f"https://{settings.AP_HOST}/api/v1/users/{user.username}", object=external_url)

    if len(act) == 0:
        return False

    unfollow_activity = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": f"https://{settings.AP_HOST}/api/v1/users/{user.username}/unfollow/{str(uuid.uuid4())}",
        "type": "Undo",
        "actor": f"https://{settings.AP_HOST}/api/v1/users/{user.username}",
        "object": {
            "id": act[0].id,
            "type": act[0].type,
            "actor": act[0].actor,
            "object": act[0].object
        }
    }

    external_inbox = external_url + \
        "inbox" if external_url[-1] == "/" else external_url + "/inbox"

    req = build_signed_request(
        user, external_inbox, unfollow_activity)

    if req.status_code < 200 or req.status_code >= 300:
        return False

    # Delete the activity
    act[0].delete()

    # delete the follow activity
    # actor_profile = Profile.objects.filter(id=unfollow_activity["actor"])
    # object_profile = Profile.objects.filter(
    #    id=unfollow_activity["object"]["object"])
    # if len(actor_profile) == 0 or len(object_profile) == 0:
    #    return False

    # follow = Follow.objects.filter(
    #    actor=actor_profile[0], object=object_profile[0])
    # if len(follow) == 0:
    #    return False
    # follow.delete()

    # Remove one from `following'
    user.following -= 1
    user.save()

    return True


def post(user: ActivityUser, data: dict, to: str) -> str:
    post_id = f"https://{settings.AP_HOST}/api/v1/users/{user.username}/post/{str(uuid.uuid4())}"
    context_id = f"https://{settings.AP_HOST}/api/v1/users/{user.username}/context/{str(uuid.uuid4())}"
    published = datetime.now().isoformat()

    post_activity = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "actor": f"https://{settings.AP_HOST}/api/v1/users/{user.username}",
        "cc": to,
        "context": context_id,
        "directMessage": False,  # TODO: Direct message
        "id": post_id,
        "type": "Create",
        "object": {
            "actor": f"https://{settings.AP_HOST}/api/v1/users/{user.username}",
            "attachment": [
                # TODO: Attachments
            ],
            "tag": data["tags"] if "tags" in data else [],
            "attributedTo": f"https://{settings.AP_HOST}/api/v1/users/{user.username}",
            "cc": to,
            "content": data["content"],
            "context": context_id,
            "conversation": context_id,
            "id": post_id,
            "published": published,
            "type": "Note"
        },
        "published": published,
        "to": [
            "https://www.w3.org/ns/activitystreams#Public"
        ]
    }

    # Get actor profile
    actor_profile = Profile.objects.filter(id=post_activity["object"]["actor"])
    if len(actor_profile) == 0:
        return ""

    actor_profile = actor_profile[0]

    note = Note()
    note.id = post_activity["object"]["id"]
    note.actor = actor_profile
    note.content = post_activity["object"]["content"]
    note.published = post_activity["object"]["published"]
    note.save()

    discovered_instances = DiscoveredInstances.objects.all()
    for instance in discovered_instances:
        req = build_signed_request(user, instance.inbox, post_activity)
        print(req.text, req.status_code)

    return post_id


def delete_post(user: ActivityUser, post_id: str) -> bool:
    post = Note.objects.filter(id=post_id)
    if len(post) == 0:
        return False

    post = post[0]

    # check that `user' is the author of the post
    if post.actor.id != f"https://{settings.AP_HOST}/api/v1/users/{user.username}":
        return False

    delete_activity = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": f"{post_id}#delete",
        "type": "Delete",
        "actor": f"https://{settings.AP_HOST}/api/v1/users/{user.username}",
        "object": {
            "id": post_id,
            "type": "Tombstone",
        },
        "to": [
            "https://www.w3.org/ns/activitystreams#Public"
        ]
    }

    act = Activity()
    act.id = delete_activity["id"]
    act.type = delete_activity["type"]
    act.actor = delete_activity["actor"]
    act.object = delete_activity["object"]
    act.save()

    post.delete()

    discovered_instances = DiscoveredInstances.objects.all()
    for instance in discovered_instances:
        req = build_signed_request(user, instance.inbox, delete_activity)
        print(req.text, req.status_code)

    return True


def send_accept(user: ActivityUser, activity: dict) -> bool:
    act = Activity.objects.filter(id=activity["id"])

    if len(act) == 0:
        act = Activity()
        act.id = activity["id"]
        act.type = activity["type"]
        act.actor = activity["actor"]
        act.object = activity["object"]
        act.save()

    accept_activity = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": f"https://{settings.AP_HOST}/api/v1/users/{user.username}/accept/{str(uuid.uuid4())}",
        "type": "Accept",
        "actor": f"https://{settings.AP_HOST}/api/v1/users/{user.username}",
        "object": activity
    }

    external_inbox = activity["actor"] + \
        "inbox" if activity["actor"][-1] == "/" else activity["actor"] + "/inbox"

    req = build_signed_request(
        user, external_inbox, accept_activity)

    if req.status_code < 200 or req.status_code >= 300:
        return False

    # Create the activity
    act = Activity()
    act.id = accept_activity["id"]
    act.type = accept_activity["type"]
    act.actor = accept_activity["actor"]
    act.object = accept_activity["object"]
    act.save()

    return True


def process_accept(user: ActivityUser, activity: dict) -> bool:
    act = Activity.objects.filter(id=activity["object"]["id"])

    if len(act) == 0:
        act = Activity()
        act.id = activity["object"]["id"]
        act.type = activity["object"]["type"]
        act.actor = activity["object"]["actor"]
        act.object = activity["object"]["object"]
        act.save()

    # when the user receives a follow accept, add one to following.
    if activity["object"]["type"] == "Follow":
        actor_profile = Profile.objects.filter(id=activity["object"]["actor"])
        object_profile = Profile.objects.filter(
            id=activity["object"]["object"])
        if len(actor_profile) == 0 or len(object_profile) == 0:
            return False

        actor_profile = actor_profile[0]
        object_profile = object_profile[0]

        follow = Follow()
        follow.id = activity["object"]["id"]
        follow.actor = actor_profile
        follow.object = object_profile
        follow.save()

        # Add one to `following'
        user.following += 1
        user.save()
    else:
        return False

    return True


def process_undo(user: ActivityUser, activity: dict) -> bool:
    # Get the activiy we want to undo
    act = Activity.objects.filter(id=activity["object"]["id"])

    if len(act) == 0:
        return False

    if activity["object"]["type"] == "Follow":
        actor_profile = Profile.objects.filter(id=activity["object"]["actor"])
        object_profile = Profile.objects.filter(
            id=activity["object"]["object"])
        if len(actor_profile) == 0 or len(object_profile) == 0:
            return False

        actor_profile = actor_profile[0]
        object_profile = object_profile[0]
        follow = Follow.objects.filter(
            actor=actor_profile, object=object_profile)
        if len(follow) == 0:
            return False

        follow = follow[0]
        follow.delete()

        # Remove one from `followers'
        user.followers -= 1
        user.save()

        act.delete()
    else:
        return False

    return True


def is_following(actor: str, object: str) -> bool:
    # Get the activity where `actor' followed `object'
    act = Activity.objects.filter(actor=actor, object=object, type="Follow")
    if len(act) == 0:
        return False

    return True
