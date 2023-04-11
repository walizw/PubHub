import requests
import time

random_user = "@Midnight_SEA@blob.cat"

OUTBOX_URL = "http://127.0.0.1:8000/api/v1/users/test/outbox"

# TODO Improve tests
# This tests should be much better (some things might require changes in the
# backend), for example, when following we should retrieve the follow activity
# id and query it to see if it was accepted and it exists. Also, when
# unfollowing we should query the follow activity id and see if it was deleted.


def get_access() -> str:
    req = requests.post(
        "http://127.0.0.1:8000/api/v1/auth/login",
        json={
            "username": "test",
            "password": "password"
        }, timeout=15)

    res = req.json()
    return res["access"]


def get_total_following():
    req = requests.get(
        "http://127.0.0.1:8000/api/v1/users/test/following", timeout=15)
    res = req.json()

    return res["totalItems"]


def follow_unfollow(user: str, follow=True):
    access = get_access()

    req = requests.post(
        OUTBOX_URL,
        json={
            "type": "Follow" if follow else "Unfollow",
            "to": user
        }, headers={
            "Authorization": f"Bearer {access}",
            "Content-Type": "application/activity+json"
        }, timeout=15)
    assert req.status_code == 200


def test_follow():
    assert get_total_following() == 0
    follow_unfollow("@alyx")
    time.sleep(5)  # wait for the follow to be processed
    assert get_total_following() == 1


def test_unfollow():
    assert get_total_following() == 1
    follow_unfollow("@alyx", follow=False)
    time.sleep(5)  # wait for the unfollow to be processed
    assert get_total_following() == 0


def test_follow_external():
    assert get_total_following() == 0
    follow_unfollow(random_user)
    time.sleep(5)  # wait for the follow to be processed
    assert get_total_following() == 1


def test_unfollow_external():
    assert get_total_following() == 1
    follow_unfollow(random_user, follow=False)
    time.sleep(5)  # wait for the unfollow to be processed
    assert get_total_following() == 0


if __name__ == "__main__":
    test_follow()
    test_unfollow()
    test_follow_external()
    test_unfollow_external()
