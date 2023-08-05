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

    # Хэндлер на команду /start и /information
    @dp.message_handler(commands=['start', 'information'])
    async def cmd_start_and_information(message: types.Message):
        info_message = "<b>Добро дошли!</b>\n\n" \
                       "Мы небольшое сообщество организации концертов, квартирников и стендапов в Нови Саде " \
                       "(а когда-нибудь и по всей Сербии).\n" \
                       "Пока мы делаем немного, но планируем расширяться.\n\n" \
                       "Если вдруг у Вас возникли вопросы, что-то не так сработало, а может Вы хотите предложить " \
                       "провести какое-нибудь мероприятие, то пишите в ЛС одному из этих двух людей — " \
                       "<b>@BISGARIK</b> или <b>@RADIATORBLACK</b>"
        await message.answer(info_message)
        links_buttons = types.InlineKeyboardMarkup()
        links_buttons.row(types.InlineKeyboardButton(
            text="Наш Instagram", url="https://www.instagram.com/radiatorblack/"))
        await message.answer("И обязательно подписывайтесь на наши соцсети!",
                             reply_markup=links_buttons)

    # Хэндлер на команду /events
    @dp.message_handler(commands=["events"])
    async def cmd_events(message: types.Message):
        await message.answer("Мы очень извиняемся, но бот пока в разработке 😞\n\n"
                             "В будущем, при нажатии на эту команду будет появляться список мероприятий.\n\n"
                             "А пока просим Вас просто написать в одном сообщении текстом, на какое из мероприятий "
                             "Вы бы хотели попасть, на чьё имя бронировать, и сколько будет человек.\n\n"
                             "Сообщение дойдёт куда-надо, и Вам обязательно ответят!")

    # Обработка ответов от администратора
    @dp.message_handler(lambda message: message.reply_to_message and message.reply_to_message.forward_from)
    async def handle_admin_response(message: types.Message):
        user_id = message.reply_to_message.forward_from.id
        admin_response = message.text

        # Отправка ответа пользователю (с вложениями, если они есть)
        # TODO сделать отправку вложений
        if message.reply_to_message.media_group_id:
            media_group = await bot.send_media_group(message.chat.id, message.reply_to_message.message_id)
            for media in media_group:
                if media.photo:
                    await bot.send_photo(user_id, photo=media.photo[-1].file_id, caption=admin_response)
                elif media.video:
                    await bot.send_video(user_id, video=media.video.file_id, caption=admin_response)
                elif media.document:
                    await bot.send_document(user_id, document=media.document.file_id, caption=admin_response)
                # Добавьте обработку других типов вложений по аналогии

        else:
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
