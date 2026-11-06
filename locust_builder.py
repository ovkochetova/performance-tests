# Импорт фабрики для создания сидера на gRPC-клиентах
from seeds.builder import build_grpc_seeds_builder
from seeds.schema.dumps import save_seeds_result, load_seeds_result

# Импорт схемы плана сида — описывает, какие сущности и в каком количестве нужно создать
from seeds.schema.plan import SeedsPlan, SeedUsersPlan, SeedCardsPlan, SeedAccountsPlan

# Шаг 1: создаём билдер с использованием gRPC-протокола
builder = build_grpc_seeds_builder()

# Шаг 2: вызываем метод .build(), передаём в него план генерации данных
result = builder.build(
    SeedsPlan(
        users=SeedUsersPlan(
            count=500,  # Нужно создать 500 пользователей
            credit_card_accounts=SeedAccountsPlan(
                count=1,  # У каждого пользователя — один кредитный счёт
                physical_cards=SeedCardsPlan(count=1),  # На счёте одна физическая карта
            )
        ),
    )
)

# # Шаг 3: выводим результат — структура, содержащая идентификаторы созданных пользователей, счетов, карт и операций
# print(result)
# Шаг 3. Сохраняем результат сидинга в файл, привязанный к сценарию "test-scenario"
save_seeds_result(result=result, scenario="test-scenario")

# Шаг 4. Загружаем данные из файла и выводим в консоль
print(load_seeds_result(scenario="test-scenario"))
