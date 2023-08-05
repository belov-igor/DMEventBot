# -*- coding: utf-8 -*-
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Желательно вместо str использовать SecretStr для конфиденциальных данных
    bot_token: SecretStr
    admin_id: SecretStr
    group_id: SecretStr

    # Вложенный класс с дополнительными указаниями для настроек
    class Config:
        # Имя файла, откуда будут прочитаны данные (относительно текущей рабочей директории)
        env_file = '.env'
        # Кодировка читаемого файла
        env_file_encoding = 'utf-8'


# При импорте файла сразу создастся и провалидируется объект конфига, который можно далее импортировать из разных мест
config = Settings()