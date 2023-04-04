# BasicPub

BasicPub is a project meant to be a complete implementation of the ActivityPub
federalisation protocol using the [Django](https://www.djangoproject.com/) web
framework.

## Installation

If you want to install BasicPub to use it locally, you first have to clone the
repository:

```bash
git clone https://github.com/walizw/BasicPub.git
```

Then, you have to install the dependencies:

```bash
pip install -r requirements.txt
```

Finally, you can run the server:

```bash
cd BasicPub/backend
python manage.py runserver
```

Note that before you want to actually use this and communicate with other
servers there are several configurations in the `backend/settings.py` file that
you might want to change:

- `ALLOWED_HOSTS`: This is a list of hosts that are allowed to access the
  server. You should add the domain name of your server here.
- `CSRF_TRUSTED_ORIGINS`: Might not be necessary, but you also might want to
  add the domain name of your server here.
- `AP_HOST`: This is the domain name of your server. It is used to generate
  the `id` of the server.

And you probably want to change the JWT settings as well.

## API

### Authentication

If you want to log-in you can perform a POST request to the
`/api/v1/auth/login/`:

```json
{
    "username": "username",
    "password": "password"
}
```

And the output will follow this format:

```json
{
    "access": "access_token",
    "refresh": "refresh_token"
}
```

If you want to refresh the JWT token you can do so at `api/v1/auth/refresh`:

```json
{
    "refresh": "refresh_token"
}
```

And the output would be:


```json
{
    "access": "new_access_token"
}
```

### ActivityPub

#### Following and Unfollowing

In order for requests to be as simple as possible, you can post to the outbox
of a user and the activity object, and all the necessary steps will be taken
automatically.

If you want to follow a user (regardless if its local or external), you can
post to the outbox of the user that will follow the other user
`/api/v1/users/<username>/outbox/`:

```json
{
    "type": "Follow",
    "to": "@username"
}
```

That if it's a local user, if it's an external user, you'd just enter the
entire URL of the user.

```json
{
    "type": "Follow",
    "to": "@username@domain.tld"
}
```

If you want to unfollow a user, you can do the same, but with the `Unfollow`
activity.

```json
{
    "type": "Unfollow",
    "to": "@username"
}
```