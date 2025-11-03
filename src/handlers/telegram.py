import os

from telegram import Bot, InputMediaPhoto, InputMediaVideo

from src.handlers.base import BaseHandler
from src.wrappers.wrappers import MessageWrapper


class TelegramHandler(BaseHandler):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    async def send_message(self, chat_id: int, message: MessageWrapper):
        if not (message.text or message.photos or message.videos):
            print("Пустое сообщение")
            return

        lines = [f"*Автор*: {message.author_name} ({message.author_id})"]
        if message.text:
            lines.append(f"*Сообщение*: {message.text}")
        if message.wall_text:
            lines.append(f"*Пост*:\n{message.wall_text}")
        caption = "\n".join(lines)

        media = []
        if message.photos:
            for photo in message.photos:
                if photo.file and os.path.exists(photo.file):
                    media.append(InputMediaPhoto(media=open(photo.file, "rb")))
        elif message.videos:
            for video in message.videos:
                if video.file and os.path.exists(video.file):
                    media.append(InputMediaVideo(media=open(video.file, "rb")))

        if media:
            await self.bot.send_media_group(
                chat_id=chat_id,
                caption=caption,
                media=media,
                parse_mode="markdown"
            )
        else:
            await self.bot.send_message(
                chat_id=chat_id,
                text=caption,
                parse_mode="markdown"
            )
