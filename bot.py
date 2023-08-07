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
                       "Мы — <b>VPN Event</b>, небольшое сообщество организации концертов, квартирников и стендапов " \
                       "в Нови Саде (а когда-нибудь и по всей Сербии или даже по всему миру!).\n" \
                       "Пока мы делаем немного, но планируем расширяться.\n\n" \
                       "Если вдруг у Вас возникли вопросы, что-то не так сработало, а может Вы хотите предложить " \
                       "провести какое-нибудь мероприятие, то пишите в ЛС одному из этих двух людей — " \
                       "<b>@BISGARIK</b> или <b>@RADIATORBLACK</b>"
        await message.answer(info_message)

        links_buttons = types.InlineKeyboardMarkup()
        links_buttons.row(types.InlineKeyboardButton(
            text="Наш Instagram", url="https://instagram.com/vpnevent?igshid=MzRlODBiNWFlZA=="))
        await message.answer("И обязательно подписывайтесь на наши соцсети!",
                             reply_markup=links_buttons)

    # Хэндлер на команду /events
    @dp.message_handler(commands=["events"])
    async def cmd_events(message: types.Message):
        await message.answer("Мы очень извиняемся, но бот пока в разработке 😞\n\n"
                             "В будущем, при нажатии на эту команду, будет появляться список мероприятий.\n\n"
                             "А пока просим Вас просто написать в одном сообщении текстом, на какое из мероприятий "
                             "Вы бы хотели попасть, на чьё имя бронировать, и сколько будет человек.\n\n"
                             "Сообщение дойдёт куда надо, и Вам обязательно ответят!")

    # Обработка ответов от администратора
    @dp.message_handler(lambda message: message.reply_to_message and message.reply_to_message.forward_from,
                        content_types=types.ContentTypes.ANY)
    async def handle_admin_response(message: types.Message):
        user_id = message.reply_to_message.forward_from.id

        # Проверка типа контента, который отправляет администратор, и пересылка его пользователю
        if message.content_type == 'text':
            await bot.send_message(user_id, message.text)
        elif message.content_type == 'photo':
            await bot.send_photo(user_id, photo=message.photo[0].file_id, caption=message.caption)
        elif message.content_type == 'video':
            await bot.send_video(user_id, video=message.video.file_id, caption=message.caption)
        elif message.content_type == 'audio':
            await bot.send_audio(user_id, audio=message.audio.file_id, caption=message.caption)
        elif message.content_type == 'voice':
            await bot.send_voice(user_id, voice=message.voice.file_id, caption=message.caption)
        elif message.content_type == 'video_note':
            await bot.send_video_note(user_id, video_note=message.video_note.file_id)
        else:
            await message.answer('Коля, брат, ну только фото, видео, голосовухи и кружочки. Это уже перебор')

    # Обработка сообщений от пользователя
    @dp.message_handler(content_types=types.ContentTypes.TEXT)
    async def answer(message: types.Message):

        # Отправка сообщения от пользователя в чат
        await bot.send_message(config.group_id.get_secret_value(),
                               f'🔽 Ник человека внизу: <b>@{message.chat.username}</b> 🔽')
        await bot.forward_message(config.group_id.get_secret_value(),
                                  message.chat.id, message.message_id)

    # Пропускаем все накопленные входящие и запускаем процесс поллинга новых апдейтов
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
