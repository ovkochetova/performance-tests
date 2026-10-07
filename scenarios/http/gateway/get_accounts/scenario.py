from locust import task

# Импортируем схемы ответов, чтобы типизировать shared state
from clients.http.gateway.accounts.schema import OpenDepositAccountResponseSchema, GetAccountsResponseSchema
from clients.http.gateway.locust import GatewayHTTPTaskSet
from clients.http.gateway.users.schema import CreateUserResponseSchema
from tools.locust.user import LocustBaseUser


class GetAccountsTaskSet(GatewayHTTPTaskSet):
    """
    Нагрузочный сценарий, который последовательно:
    1. Создаёт нового пользователя.
    2. Открывает депозитный счёта для этого пользователя.
    3. Получает список всех счетов, связанных с пользователем

    Использует базовый GatewayHTTPTaskSet и уже созданных в нём API клиентов.
    """

    # Shared state — сохраняем результаты запросов для дальнейшего использования
    create_user_response: CreateUserResponseSchema | None = None
    open_deposit_account_response: OpenDepositAccountResponseSchema | None = None
    get_accounts_response: GetAccountsResponseSchema | None = None

    @task(2)
    def create_user(self):
        """
        Создаём нового пользователя и сохраняем результат для последующих шагов.
        """
        self.create_user_response = self.users_gateway_client.create_user()

    @task(2)
    def open_deposit_account(self):
        """
        Открываем депозитный счёт для пользователя, созданного в предыдущем шаге.
        """
        if not self.create_user_response:
            return
        self.open_deposit_account_response = self.accounts_gateway_client.open_deposit_account(
            user_id=self.create_user_response.user.id)

    @task(6)
    def get_accounts(self):
        """
        Получаем список всех счетов, связанных с пользователем
        """
        if not self.open_deposit_account_response:
            return
        self.get_accounts_response = self.accounts_gateway_client.get_accounts(
            user_id=self.create_user_response.user.id)


class GetAccountsScenarioUser(LocustBaseUser):
    tasks = [GetAccountsTaskSet]
