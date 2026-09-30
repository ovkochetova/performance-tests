# from locust import HttpUser, between, task
#
# from tools.fakers import fake  # генератор случайных данных

#
# class GetUserScenarioUser(HttpUser):
#     # Пауза между запросами для каждого виртуального пользователя (в секундах)
#     wait_time = between(1, 3)
#
#     # В этой переменной будем хранить данные созданного пользователя
#     user_data: dict
#
#     def on_start(self) -> None:
#         """
#         Метод on_start вызывается один раз при запуске каждой сессии виртуального пользователя.
#         Здесь мы создаем нового пользователя, отправляя POST-запрос к /api/v1/users.
#         """
#         request = {
#             "email": fake.email(),
#             "lastName": fake.last_name(),
#             "firstName": fake.first_name(),
#             "middleName": fake.middle_name(),
#             "phoneNumber": fake.phone_number()
#         }
#         response = self.client.post("/api/v1/users", json=request)
#
#         # Сохраняем полученные данные, включая ID пользователя
#         self.user_data = response.json()
#
#     @task
#     def get_user(self):
#         """
#         Основная нагрузочная задача: получение информации о пользователе.
#         Здесь мы выполняем GET-запрос к /api/v1/users/{user_id}.
#         """
#         self.client.get(
#             f"/api/v1/users/{self.user_data['user']['id']}",
#             name="/api/v1/users/{user_id}"  # Явное указание имени группы запросов
#         )

from locust import User, between, task

from clients.http.gateway.users.client import UsersGatewayHTTPClient, build_users_gateway_locust_http_client
from clients.http.gateway.users.schema import CreateUserResponseSchema


class GetUserScenarioUser(User):  # Наследуемся от User вместо HttpUser
    # Обязательное поле, требуемое Locust. Будет проигнорировано, но его нужно указать, иначе будет ошибка запуска.
    host = "localhost"
    wait_time = between(1, 3)

    # Поле, в котором будет храниться экземпляр нашего API клиента
    users_gateway_client: UsersGatewayHTTPClient
    # Поле, куда мы сохраним ответ после создания пользователя
    create_user_response: CreateUserResponseSchema

    def on_start(self) -> None:
        """
        Метод on_start вызывается один раз при запуске каждой сессии виртуального пользователя.
        Здесь мы создаем нового пользователя, отправляя POST-запрос к /api/v1/users.
        """
        # Шаг 1: создаем API клиент, встроенный в экосистему Locust (с хуками и поддержкой сбора метрик)
        self.users_gateway_client = build_users_gateway_locust_http_client(self.environment)

        # Шаг 2: создаем пользователя через API
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def get_user(self):
        """
        Основная нагрузочная задача: получение информации о пользователе.
        Здесь мы выполняем GET-запрос к /api/v1/users/{user_id}.
        """
        # Шаг 3: получаем пользователя через API
        self.users_gateway_client.get_user(self.create_user_response.user.id)
