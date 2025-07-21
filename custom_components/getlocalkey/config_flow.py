import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_CLIENT_ID, CONF_CLIENT_SECRET

import requests
import time
import hashlib
import hmac

from homeassistant.data_entry_flow import FlowResult

DOMAIN = "getlocalkey"

CONF_UID = "uid"
CONF_REGION = "region"

REGIONS = {
    "us": "United States",
    "cn": "China",
    "eu": "Europe",
    "in": "India"
}

def tuya_sign(client_id, client_secret, access_token, t, method, path, body=""):
    body_hash = hashlib.sha256(body.encode()).hexdigest()
    string_to_sign = f"{method}\n{body_hash}\n\n{path}"
    sign_str = client_id + (access_token or "") + str(t) + string_to_sign
    return hmac.new(client_secret.encode(), sign_str.encode(), hashlib.sha256).hexdigest().upper()

class GetLocalKeyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            client_id = user_input[CONF_CLIENT_ID]
            client_secret = user_input[CONF_CLIENT_SECRET]
            uid = user_input[CONF_UID]
            region = user_input[CONF_REGION]
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

            try:
                response = requests.get(api_base + path, headers=headers)
                data = response.json()

                if "result" not in data or "access_token" not in data["result"]:
                    errors["base"] = "auth_failed"
                else:
                    return self.async_create_entry(
                        title="Get LocalKey Tuya",
                        data={
                            CONF_CLIENT_ID: client_id,
                            CONF_CLIENT_SECRET: client_secret,
                            CONF_UID: uid,
                            CONF_REGION: region
                        }
                    )
            except Exception:
                errors["base"] = "auth_failed"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_CLIENT_ID): str,
                vol.Required(CONF_CLIENT_SECRET): str,
                vol.Required(CONF_UID): str,
                vol.Required(CONF_REGION, default="us"): vol.In(REGIONS)
            }),
            errors=errors
        )