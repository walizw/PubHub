import requests


def test_registration():
    req = requests.get(
        f"http://127.0.0.1:8000/.well-known/webfinger?resource=acct:test@127.0.0.1")

    print(f"test_registration: req.status_code = {req.status_code}")

    if req.status_code == 200:
        assert req.status_code == 200  # test ends here
        return

    req = requests.post(
        f"http://127.0.0.1:8000/api/v1/auth/register",
        json={
            "username": "test",
            "email": "test@test.org",
            "password": "password"
        }
    )

    assert req.status_code == 200


def test_login():
    req = requests.post(
        f"http://127.0.0.1:8000/api/v1/auth/login",
        json={
            "username": "test",
            "password": "password"
        }
    )

    print(f"test_login: req.status_code = {req.status_code}")
    assert req.status_code == 200

    res = req.json()
    assert "access" in res
    assert "refresh" in res


if __name__ == "__main__":
    test_registration()
    test_login()
