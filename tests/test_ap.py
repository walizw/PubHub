import requests
import time

random_user = "@kaiiak@mastodon.social"


def get_access() -> str:
    req = requests.post(
        "http://127.0.0.1:8000/api/v1/auth/login",
        json={
            "username": "test",
            "password": "password"
        }, timeout=15)

    res = req.json()
    return res["access"]


def test_follow():
    access = get_access()

    req = requests.get(
        "http://127.0.0.1:8000/api/v1/users/test/following", timeout=15)
    res = req.json()

    assert res["totalItems"] == 0

    req = requests.post(
        "http://127.0.0.1:8000/api/v1/users/test/outbox",
        json={
            "type": "Follow",
            "to": "@alyx"
        }, headers={
            "Authorization": f"Bearer {access}",
            "Content-Type": "application/activity+json"
        }, timeout=15)
    assert req.status_code == 200

    print(f"test_follow: req.json() = {req.json()}")
    time.sleep(5)  # wait for the follow to be processed

    req = requests.get(
        "http://127.0.0.1:8000/api/v1/users/test/following", timeout=15)
    res = req.json()

    assert res["totalItems"] == 1


def test_unfollow():
    access = get_access()

    req = requests.get(
        "http://127.0.0.1:8000/api/v1/users/test/following", timeout=15)
    res = req.json()

    assert res["totalItems"] == 1

    req = requests.post(
        "http://127.0.0.1:8000/api/v1/users/test/outbox",
        json={
            "type": "Unfollow",
            "to": "@alyx"
        }, headers={
            "Authorization": f"Bearer {access}",
            "Content-Type": "application/activity+json"
        }, timeout=15)
    assert req.status_code == 200

    print(f"test_unfollow: req.json() = {req.json()}")
    time.sleep(5)  # wait for the unfollow to be processed

    req = requests.get(
        "http://127.0.0.1:8000/api/v1/users/test/following", timeout=15)
    res = req.json()

    assert res["totalItems"] == 0


def test_follow_external():
    access = get_access()

    req = requests.get(
        "http://127.0.0.1:8000/api/v1/users/test/following", timeout=15)
    res = req.json()

    assert res["totalItems"] == 0

    req = requests.post(
        "http://127.0.0.1:8000/api/v1/users/test/outbox",
        json={
            "type": "Follow",
            "to": random_user
        }, headers={
            "Authorization": f"Bearer {access}",
            "Content-Type": "application/activity+json"
        }, timeout=15)
    assert req.status_code == 200

    print(f"test_follow_external: req.json() = {req.json()}")
    time.sleep(5)  # wait for the follow to be processed

    req = requests.get(
        "http://127.0.0.1:8000/api/v1/users/test/following", timeout=15)
    res = req.json()

    assert res["totalItems"] == 1


def test_unfollow_external():
    access = get_access()

    req = requests.get(
        "http://127.0.0.1:8000/api/v1/users/test/following", timeout=15)
    res = req.json()

    assert res["totalItems"] == 1

    req = requests.post(
        "http://127.0.0.1:8000/api/v1/users/test/outbox",
        json={
            "type": "Unfollow",
            "to": random_user
        }, headers={
            "Authorization": f"Bearer {access}",
            "Content-Type": "application/activity+json"
        }, timeout=15)
    assert req.status_code == 200

    print(f"test_unfollow_external: req.json() = {req.json()}")
    time.sleep(5)  # wait for the unfollow to be processed

    req = requests.get(
        "http://127.0.0.1:8000/api/v1/users/test/following", timeout=15)
    res = req.json()

    assert res["totalItems"] == 0


if __name__ == "__main__":
    test_follow()
    test_unfollow()
    test_follow_external()
    test_unfollow_external()
