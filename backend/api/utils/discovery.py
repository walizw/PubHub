import requests
from django.conf import settings


def discover_user(name: str, host: str) -> dict:
    if host is None:
        host = settings.AP_HOST

    req = requests.get(
        f"https://{host}/.well-known/webfinger?resource=acct:{name}@{host}", headers={
            "Accept": "application/activity+json"
        }, timeout=5)

    if req.status_code != 200:
        return None

    # print the response in plain text
    return req.json()
