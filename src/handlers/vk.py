import os
import random

import requests
import yt_dlp
from vkbottle.bot import Message, Bot

from src.handlers.base import BaseHandler
from src.wrappers.wrappers import MessageWrapper, VideoWrapper, PhotoWrapper

DOWNLOAD_DIR = "download-vk"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_photos_vk(urls):
    photos = []
    for i, url in enumerate(urls):
        try:
            response = requests.get(url)
            response.raise_for_status()
            content = response.content

            filename = os.path.join(DOWNLOAD_DIR, f"photo_{random.randint(0, 10000)}.jpg")
            with open(filename, "wb") as f:
                f.write(content)

            photos.append(PhotoWrapper(url, filename))
        except Exception as e:
            print(f"Не удалось скачать {url}: {e}")
    return photos


def download_videos_vk(urls):
    videos = []
    for i, url in enumerate(urls):
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'format': 'best',
                'noplaylist': True,
                'extract_flat': False,
                'outtmpl': os.path.join(DOWNLOAD_DIR, f"video_{random.randint(0, 10000)}.%(ext)s"),
                # Сохраняем сразу на диск
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                videos.append(VideoWrapper(url, filename))
        except Exception as e:
            print(f"Не удалось скачать {url}: {e}")
            videos.append(VideoWrapper(url, None))
    return videos


def collect_photos_vk(message: Message) -> list[str]:
    def extract_from_attachments(attachments):
        urls = []
        if not attachments:
            return urls
        for att in attachments:
            if att.type == "photo":
                photo = att.photo
                print(photo)
                max_size = max(photo.sizes, key=lambda s: s.width * s.height)
                urls.append(max_size.url)
            elif att.type == "wall":
                wall = att.wall
                if wall and wall.attachments:
                    urls.extend(extract_from_attachments(wall.attachments))
        return urls

    photos = []
    photos.extend(extract_from_attachments(message.attachments))
    for fwd in message.fwd_messages:
        photos.extend(extract_from_attachments(fwd.attachments))
    return photos


def collect_videos_vk(message: Message) -> list[str]:
    def extract_from_attachments(attachments):
        urls = []
        if not attachments:
            return urls
        for att in attachments:
            if att.type == "video":
                video = att.video
                urls.append(f"https://vk.com/video{video.owner_id}_{video.id}")
            elif att.type == "wall":
                wall = att.wall
                if wall and wall.attachments:
                    urls.extend(extract_from_attachments(wall.attachments))
        return urls

    videos = []
    videos.extend(extract_from_attachments(message.attachments))
    for fwd in message.fwd_messages:
        videos.extend(extract_from_attachments(fwd.attachments))
    return videos


class VkHandler(BaseHandler):
    def __init__(self, bot):
        self.bot = bot

    def send_message(self, message: MessageWrapper):
        pass

    async def collect_message(self, message: Message):
        author_id = message.from_id
        author = await self.bot.api.users.get(user_ids=[author_id])
        if author:
            author_name = f'{author[0].first_name} {author[0].last_name}'
        else:
            author_name = "Скрытый пользователь"
        text = message.text
        photo_urls = collect_photos_vk(message)
        videos_urls = collect_videos_vk(message)

        photos = download_photos_vk(photo_urls)
        videos = download_videos_vk(videos_urls)

        print(f"Автор: {author_name} ({author_id})")
        print(f"Текст: {text}")
        print(f"Фото ({len(photos)}): {photos}")
        print(f"Видео ({len(videos)}): {videos}")

        return MessageWrapper(author_id, author_name, text, photos, videos)
