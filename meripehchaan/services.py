
## meripehchaan/services.py
import requests
from django.conf import settings

TIMEOUT = getattr(settings, "APISETU_REQUEST_TIMEOUT", 10)

def build_auth_url(client_id, redirect_uri, scope, state):
    from urllib.parse import urlencode
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scope,
        "state": state,
    }
    return f"{settings.APISETU_AUTH_URL}?{urlencode(params)}"

def exchange_code_for_token(code):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.APISETU_REDIRECT_URI,
        "client_id": settings.APISETU_CLIENT_ID,
        "client_secret": settings.APISETU_CLIENT_SECRET,
    }
    resp = requests.post(settings.APISETU_TOKEN_URL, data=data, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()

def fetch_aadhaar_ekyc(access_token):
    # Adjust resource path to match API Setu docs
    url = f"{settings.APISETU_RESOURCE_BASE}/aadhaar/ekyc"  # confirm exact path
    headers = {"Authorization": f"Bearer {access_token}"}
    resp = requests.get(url, headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()

def fetch_pan_verify(access_token, pan):
    # confirm exact path & parameters
    url = f"{settings.APISETU_RESOURCE_BASE}/pan/verify"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"pan": pan}
    resp = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()
