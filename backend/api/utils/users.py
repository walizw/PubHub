from .discovery import discover_user
from .request import build_signed_request

from ..models import ActivityUser, Activity

from django.conf import settings

import uuid


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

    print(req.status_code)

    if req.status_code < 200 or req.status_code >= 300:
        return False

    # Create the activity
    act = Activity()
    act.id = follow_activity["id"]
    act.type = follow_activity["type"]
    act.actor = follow_activity["actor"]
    act.object = follow_activity["object"]
    act.save()

    return True
