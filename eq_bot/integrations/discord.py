from discord import Webhook, RequestsWebhookAdapter
from utils.config import get_secret

WEBHOOK_URL=get_secret('webhooks.guild-status-discord-url')

def send_discord_message(text: str) -> None:
    if not text:
        return
    Webhook.from_url(WEBHOOK_URL, adapter=RequestsWebhookAdapter()).send(text)
