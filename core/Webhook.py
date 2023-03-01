import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed

def SendWebhook(link, base, username, title, color, desc, image = False):
    if not link: return
    webhook = DiscordWebhook(url=link)
    embed = DiscordEmbed(title=title, description=desc, color=color, url=base)
    if image:
        embed.set_image(image)
    embed.set_timestamp()
    webhook.add_embed(embed)
    try:
        res = webhook.execute()
        return True 
    except:
        return

def sendInit(lk, session, base):
    webhook = DiscordWebhook(url=lk)
    embed = DiscordEmbed(title='Webhook initialized', description=f'This is automated message sent by {session["name"]} to notify you that the webhook URL provided is valid and this post succeeded', color='32cd32', url=base)
    embed.set_timestamp()
    webhook.add_embed(embed) 
    try:
        res = webhook.execute()
        return True 
    except:
        return False