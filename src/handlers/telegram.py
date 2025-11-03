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
        if message.reactor_id:
            lines.append(f"*Одобрил*: {message.reactor_name} ({message.reactor_id})")
        if message.text:
            lines.append(f"*Сообщение*: {message.text}")
        if message.wall_text:
            lines.append(f"*Пост*:\n{message.wall_text}")

        media = []
        if message.photos:
            for photo in message.photos:
                media.append(InputMediaPhoto(media=photo.url))
        elif message.videos:
            for video in message.videos:
                if video.file and os.path.exists(video.file):
                    with open(video.file, "rb") as f:
                        media.append(InputMediaVideo(media=f.read()))
                else:
                    lines.append(f"Не удалось скачать видео: {video.url}")

        caption = "\n".join(lines)
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
