from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field, HttpUrl, ConfigDict

from tools.fakers import fake


class OperationType(StrEnum):
    FEE = "FEE"
    TOP_UP = "TOP_UP"
    PURCHASE = "PURCHASE"
    CASHBACK = "CASHBACK"
    TRANSFER = "TRANSFER"
    BILL_PAYMENT = "BILL_PAYMENT"
    CASH_WITHDRAWAL = "CASH_WITHDRAWAL"


class OperationStatus(StrEnum):
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    UNSPECIFIED = "UNSPECIFIED"


class OperationSchema(BaseModel):
    """
    Описание структуры операции.
    """
    id: str
    type: OperationType
    status: OperationStatus
    amount: float
    card_id: str = Field(alias="cardId")
    category: str
    created_at: datetime = Field(alias="createdAt")
    account_id: str = Field(alias="accountId")


class OperationReceiptSchema(BaseModel):
    """
    Описание структуры чека по операции.
    """
    url: HttpUrl
    document: str


class OperationsSummarySchema(BaseModel):
    """
    Описание структуры статистики по операциям.
    """
    spent_amount: float = Field(alias="spentAmount")
    received_amount: float = Field(alias="receivedAmount")
    cashback_amount: float = Field(alias="cashbackAmount")


class GetOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа получения операции.
    """
    operation: OperationSchema


class GetOperationsQuerySchema(BaseModel):
    """
    Структура query параметров запроса для получения списка операций по счёту.
    """
    model_config = ConfigDict(populate_by_name=True)

    account_id: str = Field(alias="accountId")


class GetOperationsResponseSchema(BaseModel):
    """
    Описание структуры ответа получения списка операций.
    """
    operations: list[OperationSchema]


class GetOperationsSummaryQuerySchema(BaseModel):
    """
    Структура query параметров запроса для получения статистики по операциям счёта.
    """
    model_config = ConfigDict(populate_by_name=True)

    account_id: str = Field(alias="accountId")


class GetOperationsSummaryResponseSchema(BaseModel):
    """
    Описание структуры ответа получения статистики по операциям.
    """
    summary: OperationsSummarySchema


class GetOperationReceiptResponseSchema(BaseModel):
    """
    Описание структуры ответа получения чека по операции.
    """
    receipt: OperationReceiptSchema


class MakeOperationRequestSchema(BaseModel):
    """
    Базовая структура тела запроса для создания финансовой операции.
    """
    model_config = ConfigDict(populate_by_name=True)

    status: OperationStatus = Field(default_factory=lambda: fake.enum(OperationStatus))
    amount: float = Field(default_factory=lambda: fake.amount())
    card_id: str = Field(alias="cardId")
    account_id: str = Field(alias="accountId")


class MakeFeeOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции комиссии.
    """
    pass


class MakeFeeOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание операции комиссии.
    """
    operation: OperationSchema


class MakeTopUpOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции пополнения.
    """
    pass


class MakeTopUpOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание операции пополнения.
    """
    operation: OperationSchema


class MakeCashbackOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции кэшбэка.
    """
    pass


class MakeCashbackOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание операции кэшбэка.
    """
    operation: OperationSchema


class MakeTransferOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции перевода.
    """
    pass


class MakeTransferOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание операции перевода.
    """
    operation: OperationSchema


class MakePurchaseOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции покупки.

    Дополнительное поле:
    - category: категория покупки.
    """
    category: str = Field(default_factory=lambda : fake.category())


class MakePurchaseOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание операции покупки.
    """
    operation: OperationSchema


class MakeBillPaymentOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции оплаты по счёту.
    """
    pass


class MakeBillPaymentOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание операции оплаты по счёту.
    """
    operation: OperationSchema


class MakeCashWithdrawalOperationRequestSchema(MakeOperationRequestSchema):
    """
    Структура запроса для создания операции снятия наличных.
    """
    pass


class MakeCashWithdrawalOperationResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание операции снятия наличных.
    """
    operation: OperationSchema
