# Импортируем необходимые типы из Pydantic
from pydantic import BaseModel, SecretStr, EmailStr, HttpUrl

# Импортируем базовый класс настроек и конфигурацию из pydantic-settings
from pydantic_settings import BaseSettings, SettingsConfigDict


# Вложенная модель для описания конфигурации тестового пользователя
class TestUserConfig(BaseModel):
    email: EmailStr  # Email с автоматической валидацией формата
    password: SecretStr  # Пароль, который будет скрыт при выводе (безопасность)


# Основная модель конфигурации проекта
class Settings(BaseSettings):
    # Специальный класс-конфигурация, указывающий источники и поведение загрузки
    model_config = SettingsConfigDict(
        env_file=".env.basics",  # Путь до файла с переменными окружения
        env_file_encoding="utf-8",  # Кодировка .env файла
        env_nested_delimiter=".",  # Разделитель для вложенных структур, например TEST_USER.EMAIL
    )

    base_url: HttpUrl  # Главный URL тестируемого сервиса
    test_user: TestUserConfig  # Вложенная конфигурация пользователя (см. выше)


# При запуске скрипта создаётся объект с подгруженными значениями и выводится
print(Settings())
