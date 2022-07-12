import requests

from game.guild.dkp_entity_factory import build_summary_from_gateway
from game.guild.entities.dkp_summary import DkpSummary

from utils.http import HttpClient
from utils.config import get_config

OPEN_DKP_ROOT_ENDPOINT = get_config('guild_tracking.open_dkp.root_endpoint')
OPEN_DKP_CLIENT_ID = get_config('guild_tracking.open_dkp.client_id')


class DkpGateway:
    def __init__(self):
        self._client = HttpClient()

    def fetch_dkp_summary(self) -> DkpSummary:
        return build_summary_from_gateway(
            self._client.get(f"{OPEN_DKP_ROOT_ENDPOINT.rstrip('/')}/dkp", headers={"clientid": OPEN_DKP_CLIENT_ID})
                .json())
