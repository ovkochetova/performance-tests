from locust import User, between, task

# Импортируем схемы ответов, чтобы типизировать shared state
from clients.grpc.gateway.locust import GatewayGRPCTaskSet

from contracts.services.gateway.accounts.rpc_open_deposit_account_pb2 import OpenDepositAccountResponse
from contracts.services.gateway.accounts.rpc_get_accounts_pb2 import GetAccountsResponse
from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserResponse


class GetAccountsTaskSet(GatewayGRPCTaskSet):
    """
    Нагрузочный сценарий, который последовательно:
    1. Создаёт нового пользователя.
    2. Открывает сберегательный счёт.
    3. Получает документы по счёту (тариф и контракт).

    Использует базовый GatewayGRPCSequentialTaskSet и уже созданных в нём API клиентов.
    """

    # Shared state — сохраняем результаты запросов для дальнейшего использования
    create_user_response: CreateUserResponse | None = None
    open_deposit_account_response: OpenDepositAccountResponse | None = None
    get_accounts_response: GetAccountsResponse | None = None

    @task
    def create_user(self):
        """
        Создаём нового пользователя и сохраняем результат для последующих шагов.
        """
        self.create_user_response = self.users_gateway_client.create_user()

    @task
    def open_deposit_account(self):
        """
        Открываем сберегательный счёт для пользователя.
        """
        if not self.create_user_response:
            return
        self.open_deposit_account_response = self.accounts_gateway_client.open_deposit_account(
            user_id=self.create_user_response.user.id
        )

    @task
    def get_accounts(self):
        """
        Получаем документы по счёту (тариф и контракт).
        """
        if not self.open_deposit_account_response:
            return
        self.get_accounts_response = self.accounts_gateway_client.get_accounts(
            user_id= self.create_user_response.user.id
        )

class GetAccountsScenarioUser(User):
    host = "localhost"
    tasks = [GetAccountsTaskSet]
    max_wait = between(1, 3)

