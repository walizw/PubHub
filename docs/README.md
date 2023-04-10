# BasicPub

BasicPub is a project meant to be a complete implementation of the ActivityPub
federalisation protocol using the [Django](https://www.djangoproject.com/) web
framework.

## Running

Note that before you want to actually use this and communicate with other
servers there are several configurations in the `backend/settings.py` file that
you might want to change:

- `ALLOWED_HOSTS`: This is a list of hosts that are allowed to access the
  server. You should add your domain name here.
- `CSRF_TRUSTED_ORIGINS`: Might not be necessary, but you also might want to
  add your domain name here.
- `AP_HOST`: This is the domain name of your server. It is used to generate
  its `id`. This is probably the most important setting you have to change.
- `CORS_ORIGIN_ALLOW_ALL`: This is a boolean that determines if all origins
  are allowed to access the API. You probably want to change this to `False`
  and add your domain name to the `CORS_ORIGIN_WHITELIST` setting.

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

### Posting

If you want to publish a post, you can perform a POST request to the outbox of
the user that will create the post, with the following format:

```json
{
    "type": "Note",
    "content": "The note content goes here",
    "tags": [
      "tags",
      "are",
      "an",
      "array"
    ]
}
```

The response will look like this, in case the post was successfully created:

```json
{
  "status": "success",
  "id": "post-id-goes-here"
}
```

**Note:** There are some things that are still pendant to implement. Like polls
and attachments.

You can also delete a post, by posting the *Delete* activity type to a user's
outbox with the post id:

```bash
{
  "status": "Delete",
  "id": "post-id-goes-here"
}
```