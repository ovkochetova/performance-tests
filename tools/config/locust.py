from locust import User, between
from pydantic import EmailStr, SecretStr


class LocustUserConfig(User):
    """
    Базовый виртуальный пользователь Locust, от которого наследуются все сценарии.
    Содержит общие настройки, которые могут быть переопределены при необходимости.
    """
    wait_time_min: float = 1
    wait_time_max: float = 3
