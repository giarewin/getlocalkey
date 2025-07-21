import time
import hashlib
import hmac
import requests

def tuya_sign(client_id, client_secret, access_token, t, method, path, body=""):
    body_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
    string_to_sign = f"{method}\n{body_hash}\n\n{path}"
    sign_str = client_id + (access_token or "") + str(t) + string_to_sign
    return hmac.new(client_secret.encode("utf-8"), sign_str.encode("utf-8"), hashlib.sha256).hexdigest().upper()

def get_devices(client_id, client_secret, uid, region="us"):
    api_base = f"https://openapi.tuya{region}.com"
    t = int(time.time() * 1000)
    path = "/v1.0/token?grant_type=1"
    sign = tuya_sign(client_id, client_secret, "", t, "GET", path)
    headers = {
        "client_id": client_id,
        "sign": sign,
        "t": str(t),
        "sign_method": "HMAC-SHA256"
    }
    res = requests.get(api_base + path, headers=headers, verify=False)
    access_token = res.json()["result"]["access_token"]

    t = int(time.time() * 1000)
    path = f"/v1.0/users/{uid}/devices"
    sign = tuya_sign(client_id, client_secret, access_token, t, "GET", path)
    headers = {
        "client_id": client_id,
        "access_token": access_token,
        "sign": sign,
        "t": str(t),
        "sign_method": "HMAC-SHA256"
    }
    res = requests.get(api_base + path, headers=headers, verify=False)
    return res.json()
