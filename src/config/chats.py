import json
from pathlib import Path

CHATS_MAPPING = Path(__file__).parent.parent.parent / "chats_mapping.json"


def load_chats_mapping() -> dict:
    if not CHATS_MAPPING.exists():
        raise FileNotFoundError(f"Файл chats_mapping.json не найден: {CHATS_MAPPING}")

    with open(CHATS_MAPPING, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Валидация
    if "vk" not in data or "telegram" not in data:
        raise ValueError("Файл должен содержать ключи 'vk' и 'telegram'")

    if not isinstance(data["vk"], list) or not isinstance(data["telegram"], list):
        raise ValueError("Значения 'vk' и 'telegram' должны быть списками")

    # Преобразуем всё в int (на случай, если в JSON были строки)
    try:
        vk_ids = [int(x) for x in data["vk"]]
        tg_ids = [int(x) for x in data["telegram"]]
    except (ValueError, TypeError) as e:
        raise ValueError("Все ID должны быть числами (или строками с числами)") from e

    return {
        "vk": vk_ids,
        "telegram": tg_ids
    }
