import requests

from django.conf import settings

from ..models import DiscoveredInstances


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
    if instance != None:
        user_link = ""
        for link in res.get("links"):
            if link["rel"] == "self":
                user_link = link["href"]
                break

        inbox_req = requests.get(user_link, headers={
            "Accept": "application/activity+json"
        }, timeout=5)
        instance.inbox = inbox_req.json().get("endpoints")["sharedInbox"]
        instance.save()

    # print the response in plain text
    return res
