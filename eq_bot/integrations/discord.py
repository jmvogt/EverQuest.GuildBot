from discord import Webhook, RequestsWebhookAdapter

# TODO: Move to secrets store
WEBHOOK_URL="https://discord.com/api/webhooks/994527718693666816/qpr2S9GNmCd0VfTpNWMDa-Md2ctpMvtJld0SpsDXWgMjnG33XCwry-pdC5QkoZsA72d4"

def send_discord_message(text: str) -> None:
    Webhook.from_url(WEBHOOK_URL, adapter=RequestsWebhookAdapter()).send(text)
