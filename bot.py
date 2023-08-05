# -*- coding: utf-8 -*-
import asyncio
import logging

from aiogram import Bot, Dispatcher, types

from config_reader import config


async def main():
    # Запуск логгирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # Объект бота и диспетчер
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
    dp = Dispatcher(bot=bot)

    # Хэндлер на команду /start
    @dp.message_handler(commands=['start'])
    async def cmd_start(message: types.Message):
        await message.answer(f'Добро пожаловать!')

    # Хэндлер на команду /events
    @dp.message_handler(commands=["events"])
    async def cmd_events(message: types.Message):
        await message.answer("Заглушка. Бот в разработке 😞\n\n"
                             "В будущем, при нажатии на эту команду будет появляться список мероприятий.\n\n"
                             "А пока просим Вас просто написать сообщение текстом в бота, на какое мероприятие "
                             "Вы бы хотели попасть, на чьё имя бронировать, и сколько будет человек.\n\n"
                             "Сообщение дойдёт куда-надо, и Вам обязательно ответят!")

    # Хэндлер на команду /information
    @dp.message_handler(commands=["information"])
    async def cmd_information(message: types.Message):
        await message.answer("Добро дошли!\n\n"
                             "Мы небольшое сообщество организации концертов, квартирников и стендапов в Нови Саде. "
                             "Мы делаем пока немного, но планируем расширяться")
        links_buttons = types.InlineKeyboardMarkup()
        links_buttons.row(types.InlineKeyboardButton(
            text="Ссылка на Instagram", url="https://www.instagram.com/radiatorblack/"))
        await message.answer("И подписывайтесь на наши соцсети!",
                             reply_markup=links_buttons)

    # Обработка ответов от администратора
    @dp.message_handler(lambda message: message.reply_to_message and message.reply_to_message.forward_from)
    async def handle_admin_response(message: types.Message):
        user_id = message.reply_to_message.forward_from.id
        admin_response = message.text

        # Отправка ответа пользователю
        await bot.send_message(user_id, admin_response)

    # Обработка сообщений от пользователя
    @dp.message_handler(content_types=types.ContentTypes.TEXT)
    async def answer(message: types.Message):

        # Отправка сообщения от пользователя в чат
        await bot.forward_message(config.group_id.get_secret_value(), message.chat.id, message.message_id)

    # Пропускаем все накопленные входящие и запускаем процесс поллинга новых апдейтов
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
