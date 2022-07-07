from discord import Webhook, RequestsWebhookAdapter
from utils.secrets import get_secret

WEBHOOK_URL=get_secret('webhooks.guild-status-discord-url')

def send_discord_message(text: str) -> None:
    Webhook.from_url(WEBHOOK_URL, adapter=RequestsWebhookAdapter()).send(text)
