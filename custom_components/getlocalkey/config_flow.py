import voluptuous as vol
from homeassistant import config_entries

@config_entries.HANDLERS.register("getlocalkey")
class GetLocalKeyConfigFlow(config_entries.ConfigFlow, domain="getlocalkey"):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Get LocalKey Tuya", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("client_id"): str,
                vol.Required("client_secret"): str,
                vol.Required("uid"): str,
                vol.Required("region", default="us"): vol.In(["us", "cn", "eu", "in"])
            })
        )
