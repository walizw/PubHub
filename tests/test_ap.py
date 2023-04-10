import requests


def get_access():
    req = requests.post("http://127.0.0.1:8000/api/v1/auth/login",
                        json={
                            "username": "test",
                            "password": "password"
                        })

    res = req.json()
    return res["access"]


def test_follow():
    access = get_access()

    req = requests.get(
        "http://127.0.0.1:8000/api/v1/users/test/following")
    res = req.json()

    assert res["totalItems"] == 0
    acess = get_access()

    req = requests.post(
        "http://127.0.0.1:8000/api/v1/users/test/outbox",
        json={
            "type": "Follow",
            "to": "@alyx"
        }, headers={
            "Authorization": f"Bearer {access}",
            "Content-Type": "application/activity+json"
        })
    assert req.status_code == 200

    print(f"test_follow: req.json() = {req.json()}")

    req = requests.get(
        "http://127.0.0.1:8000/api/v1/users/test/following")
    res = req.json()

    assert res["totalItems"] == 1


def test_unfollow():
    access = get_access()

    req = requests.get(
        "http://127.0.0.1:8000/api/v1/users/test/following")
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
        })
    assert req.status_code == 200

    print(f"test_unfollow: req.json() = {req.json()}")

    req = requests.get(
        "http://127.0.0.1:8000/api/v1/users/test/following")
    res = req.json()

    assert res["totalItems"] == 0


if __name__ == "__main__":
    test_follow()
    test_unfollow()
