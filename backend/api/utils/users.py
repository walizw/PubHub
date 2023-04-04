from .discovery import discover_user
from .request import build_signed_request

from ..models import ActivityUser, Activity

from django.conf import settings

import uuid


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

    external_inbox = external_url + \
        "inbox" if external_url[-1] == "/" else external_url + "/inbox"

    req = build_signed_request(
        user, external_inbox, follow_activity)

    if req.status_code < 200 or req.status_code >= 300:
        return False

    # Create the activity
    act = Activity()
    act.id = follow_activity["id"]
    act.type = follow_activity["type"]
    act.actor = follow_activity["actor"]
    act.object = follow_activity["object"]
    act.save()

    # TODO: Following should be updated after receiving the Accept
    # Add one to `following'
    user.following += 1
    user.save()

    # Is the followed user local?
    if external_url.split("/")[2] == settings.AP_HOST:
        # Get the user
        followed_user = ActivityUser.objects.get(
            username=external_url.split("/")[-1])

        # Add the user to the followers
        followed_user.followers += 1
        followed_user.save()

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

    # Remove one from `following'
    user.following -= 1
    user.save()

    # Is the unfollowed user local?
    if external_url.split("/")[2] == settings.AP_HOST:
        # Get the user
        followed_user = ActivityUser.objects.get(
            username=external_url.split("/")[-1])

        # Remove the user from the followers
        followed_user.followers -= 1
        followed_user.save()

    return True
