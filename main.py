import discord
import re
import os
from telegram import Bot

DISCORD_TOKEN = os.getenv("MTQ1MjA1ODg2ODA2NTYzNjUxNg.Gi1kDI.iBKQMlcDI6KFUDmTbArS3UoFDgQmZm_8W8O3Cg")
TELEGRAM_TOKEN = os.getenv("8549541377:AAExR4YXRcTw2Kwzbdj2VCab-Orffn6sYNo")
TELEGRAM_CHAT_ID = os.getenv("5000662704")

telegram_bot = Bot(token=TELEGRAM_TOKEN)
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def clean_for_telegram(text):
    if not text:
        return text
    text = re.sub(r"```[\s\S]*?```", lambda m: m.group(0).replace("```", ""), text)
    text = text.replace("```", "")
    return text

def convert_custom_emojis(text):
    if not text:
        return text
    text = clean_for_telegram(text)
    pattern = r"<a?:\w+:(\d+)>"
    return re.sub(
        pattern,
        lambda m: f"https://cdn.discordapp.com/emojis/{m.group(1)}.png",
        text
    )

@client.event
async def on_ready():
    print(f"✅ Discord bot connected as {client.user}")

@client.event
async def on_message(message):
    parts = []
    if message.content:
        parts.append(convert_custom_emojis(message.content))
    for embed in message.embeds:
        if embed.title:
            parts.append(f"🧷 {clean_for_telegram(embed.title)}")
        if embed.description:
            parts.append(clean_for_telegram(embed.description))
        for field in embed.fields:
            parts.append(
                f"{clean_for_telegram(field.name)}:\n{clean_for_telegram(field.value)}"
            )
        if embed.url:
            parts.append(f"🔗 {embed.url}")
        if embed.image and embed.image.url:
            await telegram_bot.send_photo(
                chat_id=TELEGRAM_CHAT_ID,
                photo=embed.image.url
            )
        if embed.thumbnail and embed.thumbnail.url:
            await telegram_bot.send_photo(
                chat_id=TELEGRAM_CHAT_ID,
                photo=embed.thumbnail.url
            )
    for attachment in message.attachments:
        await telegram_bot.send_document(
            chat_id=TELEGRAM_CHAT_ID,
            document=attachment.url
        )
    if not parts:
        return
    text = (
        f"👤 {message.author}\n"
        f"📍 #{message.channel}\n\n"
        + "\n\n".join(parts)
    )
    for i in range(0, len(text), 4000):
        await telegram_bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=text[i:i + 4000]
        )

client.run(DISCORD_TOKEN)
