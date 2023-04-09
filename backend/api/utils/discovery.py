import requests

from django.conf import settings

from ..models import DiscoveredInstances, Profile


def discover_user(name: str, host: str) -> dict:
    # check if the instance is already discovered
    instances = DiscoveredInstances.objects.filter(url=host)
    instance = None
    if len(instances) == 0:
        # discover the instance
        instance = DiscoveredInstances()
        instance.url = host
        instance.save()

    if host is None:
        host = settings.AP_HOST

    req = requests.get(
        f"https://{host}/.well-known/webfinger?resource=acct:{name}@{host}", headers={
            "Accept": "application/jrd+json"
        }, timeout=5)

    if req.status_code != 200:
        return None

    res = req.json()
    user_link = ""
    for link in res.get("links"):
        if link["rel"] == "self":
            user_link = link["href"]
            break

    if instance != None:
        inbox_req = requests.get(user_link, headers={
            "Accept": "application/activity+json"
        }, timeout=5)
        inbox_res = inbox_req.json()

        instance.inbox = inbox_res.get("endpoints")["sharedInbox"]
        instance.save()

    profile = Profile.objects.filter(id=user_link)
    if len(profile) == 0:
        inbox_req = requests.get(user_link, headers={
            "Accept": "application/activity+json"
        }, timeout=5)
        inbox_res = inbox_req.json()

        # create the profile
        profile = Profile()
        profile.id = user_link
        profile.preferred_username = inbox_res["preferredUsername"]
        profile.followers = inbox_res["followers"]
        profile.following = inbox_res["following"]
        profile.inbox = inbox_res["inbox"]
        profile.outbox = inbox_res["outbox"]
        profile.public_key = inbox_res["publicKey"]["publicKeyPem"]
        profile.shared_inbox = inbox_res.get("endpoints")["sharedInbox"]
        profile.save()

    # print the response
    return res
