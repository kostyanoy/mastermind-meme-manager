from vkbottle.bot import Message, Bot

from config.chats import load_chats_mapping
from config.creds import load_vk_token, load_telegram_token
from src.handlers.vk import VkHandler

VK_TOKEN = load_vk_token()
TELEGRAM_TOKEN = load_telegram_token()
CHATS_MAPPING = load_chats_mapping()

vk_bot = Bot(token=VK_TOKEN)
vk_handler = VkHandler(vk_bot)


@vk_bot.on.chat_message()
async def collect_message(message: Message):
    if message.peer_id not in CHATS_MAPPING["vk"]:
        print("Чат не в списке разрешенных")
        return
    await vk_handler.collect_message(message)


if __name__ == "__main__":
    vk_bot.run_forever()
