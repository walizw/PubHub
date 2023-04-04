from cryptography.hazmat.backends import default_backend as crypto_default_backend
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from django.conf import settings

import requests
import datetime
from urllib.parse import urlparse
import base64
import json
import hashlib

from ..models import ActivityUser


def build_signed_request(user: ActivityUser, dst_inbox: str, cnt: dict) -> requests.Response:
    """Build a signed request to a remote server.

    :param user: The user to sign the request with.
    :param dst_inbox: The destination inbox.
    :param cnt: The content to send.
    :return: The request.
    """

    if not user:
        return None

    priv_key_txt = user.priv_key
    priv_key = crypto_serialization.load_pem_private_key(
        priv_key_txt.encode("utf-8"),
        password=None,
        backend=crypto_default_backend()
    )

    cur_date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    dst_inbox_parsed = urlparse(dst_inbox)
    dst_host = dst_inbox_parsed.netloc
    dst_path = dst_inbox_parsed.path

    cnt_str = json.dumps(cnt)
    digest = base64.b64encode(hashlib.sha256(cnt_str.encode("utf-8")).digest())

    signature_txt = b'(request-target): post %s\ndigest: SHA-256=%s\nhost: %s\ndate: %s' % (
        dst_path.encode("utf-8"),
        digest,
        dst_host.encode("utf-8"),
        cur_date.encode("utf-8")
    )

    raw_sign = priv_key.sign(
        signature_txt,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    key_id = f"https://{settings.AP_HOST}/api/v1/users/{user.username}#main-key"
    # header_sign = f"keyId=\"{key_id}\",algorithm=\"rsa-sha256\",headers=\"(request-target) digest host date\",signature=\"{base64.b64encode(raw_sign).decode('utf-8')}\""
    header_sign = 'keyId="%s",algorithm="rsa-sha256",headers="(request-target) digest host date",signature="%s"' % (key_id, base64.b64encode(
        raw_sign).decode('utf-8'))

    headers = {
        "Date": cur_date,
        "Content-Type": "application/activity+json",
        "Host": dst_host,
        'Digest': "SHA-256="+digest.decode('utf-8'),
        "Signature": header_sign
    }

    return requests.post(dst_inbox, headers=headers, json=cnt, timeout=15)
