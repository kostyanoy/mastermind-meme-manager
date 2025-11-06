import json
from pathlib import Path

CHATS_MAPPING = Path(__file__).parents[2] / "chats_mapping.json"


def load_chats_mapping() -> dict:
    if not CHATS_MAPPING.exists():
        raise FileNotFoundError(f"Файл chats_mapping.json не найден: {CHATS_MAPPING}")

    with open(CHATS_MAPPING, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Валидация
    if "vk_mapping" not in data:
        raise ValueError("Файл должен содержать ключ 'vk_mapping'")

    vk_mapping = data["vk_mapping"]

    if not isinstance(vk_mapping, dict):
        raise ValueError("'vk_mapping' должен быть объектом (словарём в Python)")

    # Преобразуем всё в int (на случай, если в JSON были строки)
    result = {}
    for vk_key, tg_list in vk_mapping.items():
        try:
            vk_id = int(vk_key)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Некорректный VK ID: {vk_key}") from e

        if not isinstance(tg_list, list):
            raise ValueError(f"Для VK ID {vk_id} значение должно быть списком Telegram ID")

        try:
            tg_ids = [int(tg_id) for tg_id in tg_list]
        except (ValueError, TypeError) as e:
            raise ValueError(f"Некорректные Telegram ID для VK {vk_id}: {tg_list}") from e

        result[vk_id] = tg_ids

    return {
        "vk_mapping": result,
    }
