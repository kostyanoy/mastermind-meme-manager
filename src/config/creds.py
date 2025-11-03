import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent.parent
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(ENV_PATH)


def load_vk_token() -> str:
    token = os.getenv("VK_TOKEN")
    if not token:
        raise ValueError("❌ VK_TOKEN не найден в .env файле!")
    return token.strip()


def load_telegram_token() -> str:
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("❌ TELEGRAM_TOKEN не найден в .env файле!")
    return token.strip()
