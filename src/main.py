import asyncio

from telegram.ext import Application, CommandHandler
from vkbottle.bot import Message, Bot

from config.chats import load_chats_mapping
from config.creds import load_vk_token, load_telegram_token
from src.handlers.telegram import TelegramHandler
from src.handlers.vk import VkHandler

VK_TOKEN = load_vk_token()
TELEGRAM_TOKEN = load_telegram_token()
CHATS_MAPPING = load_chats_mapping()


async def run_telegram_bot():
    async def get_chat_id(update, context):
        chat_id = update.effective_chat.id
        await update.message.reply_text(f"ID этого чата: `{chat_id}`", parse_mode="Markdown")

    # tg_bot = telegram.Bot(TELEGRAM_TOKEN)
    tg_app = Application.builder().token(TELEGRAM_TOKEN).build()
    tg_app.add_handler(CommandHandler("chatid", get_chat_id))
    tg_handler = TelegramHandler(tg_app.bot)

    await tg_app.initialize()
    await tg_app.start()
    await tg_app.updater.start_polling()

    return tg_handler


async def run_vk_bot(tg_handler):
    vk_bot = Bot(token=VK_TOKEN)
    vk_handler = VkHandler(vk_bot)

    @vk_bot.on.chat_message(text="/chatid")
    async def get_chat_id(message: Message):
        await message.answer(f"ID этого чата: {message.peer_id}")

    @vk_bot.on.chat_message()
    async def collect_message(message: Message):
        if message.peer_id not in CHATS_MAPPING["vk"]:
            print("Чат не в списке разрешенных")
            return
        message_wrapper = await vk_handler.collect_message(message)
        print(message_wrapper)
        for chat_id in CHATS_MAPPING["telegram"]:
            await tg_handler.send_message(chat_id, message_wrapper)

    try:
        await vk_bot.run_polling()
    except Exception as e:
        print(f"VK ошибка: {e}")


async def main():
    tg_handler = await run_telegram_bot()
    asyncio.create_task(run_vk_bot(tg_handler))

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
