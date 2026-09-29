from locust import HttpUser, between, task


# Класс виртуального пользователя, который будет выполнять наши задачи
class BasicScenarioUser(HttpUser):
    # Устанавливаем время ожидания между задачами: случайное значение от 5 до 15 секунд
    wait_time = between(5, 15)

    # Задача с весом 2: GET-запрос на /get будет вызываться в два раза чаще, чем остальные
    @task(2)
    def get_data(self):
        self.client.get("/get")

    # Задача с весом 1: POST-запрос на /post
    @task(1)
    def post_data(self):
        self.client.post("/post")

    # Задача с весом 1: DELETE-запрос на /delete
    @task(1)
    def delete_data(self):
        self.client.delete("/delete")


