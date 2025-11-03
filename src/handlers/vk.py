import random
from pathlib import Path

import requests
import yt_dlp
from vkbottle.bot import Message

from src.wrappers.wrappers import MessageWrapper, VideoWrapper, PhotoWrapper

DOWNLOAD_DIR = Path(__file__).parent.parent.parent / "download-vk"
DOWNLOAD_DIR.mkdir(exist_ok=True)


def download_photos_vk(urls):
    photos = []
    for i, url in enumerate(urls):
        try:
            response = requests.get(url)
            response.raise_for_status()
            content = response.content

            filename = str(DOWNLOAD_DIR / f"photo_{random.randint(0, 10000)}.jpg")
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
                'outtmpl': str(DOWNLOAD_DIR / f"video_{random.randint(0, 10000)}.%(ext)s"),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                videos.append(VideoWrapper(url, filename))
        except Exception as e:
            print(f"Не удалось скачать {url}: {e}")
            videos.append(VideoWrapper(url, None))
    return videos


def collect_wall_texts(message: Message) -> list[str]:
    def extract_wall_texts(attachments):
        texts = []
        if not attachments:
            return texts
        for att in attachments:
            if att.type == "wall":
                wall = att.wall
                if wall and wall.text:
                    texts.append(wall.text.strip())
                if wall and wall.attachments:
                    texts.extend(extract_wall_texts(wall.attachments))
        return texts

    all_texts = []
    all_texts.extend(extract_wall_texts(message.attachments))
    for fwd in message.fwd_messages:
        all_texts.extend(extract_wall_texts(fwd.attachments))
    return all_texts


def collect_photos_vk(message: Message) -> list[str]:
    def extract_from_attachments(attachments):
        urls = []
        if not attachments:
            return urls
        for att in attachments:
            if att.type == "photo":
                photo = att.photo
                max_size = max(photo.sizes, key=lambda s: s.width * s.height)
                urls.append(max_size.url)
            elif att.type == "wall" and att.wall and att.wall.attachments:
                urls.extend(extract_from_attachments(att.wall.attachments))
        return urls

    urls = extract_from_attachments(message.attachments)
    for fwd in message.fwd_messages:
        urls.extend(extract_from_attachments(fwd.attachments))
    return urls


def collect_videos_vk(message: Message) -> list[str]:
    def extract_from_attachments(attachments):
        urls = []
        if not attachments:
            return urls
        for att in attachments:
            if att.type == "video":
                video = att.video
                urls.append(f"https://vk.com/video{video.owner_id}_{video.id}")
            elif att.type == "wall" and att.wall and att.wall.attachments:
                urls.extend(extract_from_attachments(att.wall.attachments))
        return urls

    urls = extract_from_attachments(message.attachments)
    for fwd in message.fwd_messages:
        urls.extend(extract_from_attachments(fwd.attachments))
    return urls


class VkHandler:
    def __init__(self, bot):
        self.bot = bot

    async def collect_message(self, message: Message):
        author_id = message.from_id
        author = await self.bot.api.users.get(user_ids=[author_id])
        if author:
            author_name = f'{author[0].first_name} {author[0].last_name}'
        else:
            author_name = "Скрытый пользователь"
        text = message.text
        wall_text = "\n".join(collect_wall_texts(message))
        photo_urls = collect_photos_vk(message)
        videos_urls = collect_videos_vk(message)

        photos = download_photos_vk(photo_urls)
        videos = download_videos_vk(videos_urls)

        print(f"Автор: {author_name} ({author_id})")
        print(f"Текст: {text}")
        print(f"Текст поста: {wall_text}")
        print(f"Фото ({len(photos)}): {photos}")
        print(f"Видео ({len(videos)}): {videos}")

        return MessageWrapper(author_id, author_name, text, wall_text, photos, videos)
