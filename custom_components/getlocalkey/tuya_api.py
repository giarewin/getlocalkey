import requests
import time
import hashlib
import hmac
import json

API_BASE = "https://openapi.tuya{region}.com"

def get_sign(client_id, access_token, secret, method, url, t, body=""):
    string_to_sign = f"{method}\n{hashlib.sha256(body.encode()).hexdigest()}\n\n{url}"
    str_to_hash = client_id + access_token + str(t) + string_to_sign
    signature = hmac.new(secret.encode(), str_to_hash.encode(), hashlib.sha256).hexdigest().upper()
    return signature

def fetch_device_localkeys(conf, logger):
    client_id = "trje9tpqve9m54gdqypy"
    secret = "1b71a8b6c103448dae65f138f60a9e0e"
    region = conf.get("region", "us")
    uid = "az1536401329492bM2vA"
    api = API_BASE.format(region=region)

    try:
        # Get token
        t = str(int(time.time() * 1000))
        sign = get_sign(client_id, "", secret, "GET", "/v1.0/token?grant_type=1", t)
        headers = {
            "client_id": client_id,
            "sign": sign,
            "t": t,
            "sign_method": "HMAC-SHA256"
        }
        r = requests.get(f"{api}/v1.0/token?grant_type=1", headers=headers)
        token_data = r.json().get("result", {})
        access_token = token_data.get("access_token")
        if access_token:
            logger.info("✅ Đăng nhập Tuya Cloud thành công!")
        else:
            logger.error("❌ Đăng nhập Tuya Cloud thất bại! Không có access_token.")
        if not access_token:
            logger.error("❌ Failed to get access token.")
            return

        # Get devices
        t = str(int(time.time() * 1000))
        path = f"/v1.0/users/{uid}/devices"
        sign = get_sign(client_id, access_token, secret, "GET", path, t)
        headers.update({
            "access_token": access_token,
            "sign": sign,
        })
        r = requests.get(f"{api}{path}", headers=headers)
        result = r.json()
        if not result.get("success"):
            logger.error(f"❌ Error fetching devices: {result}")
            return

        logger.info("📦 Device List with LocalKey:")
        devices = result.get("result", [])
        lines = []
        for dev in devices:
            line = f"{dev.get('name')} | {dev.get('product_name')} | {dev.get('id')} | {dev.get('local_key')} | {dev.get('node_id')} | {dev.get('ip')}"
            lines.append(line)
            logger.info(line)

        # Write to data.txt
        with open('/config/custom_components/getlocalkey/data.txt', 'w') as f:
            f.write("\n".join(lines))

    except Exception as e:
        logger.exception(f"❌ Exception during localkey fetch: {e}")
