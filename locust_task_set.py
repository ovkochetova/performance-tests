from locust import TaskSet, task, HttpUser

class MyTaskSet(TaskSet):
    @task
    def task_one(self):
        self.client.get("/page1")

    @task
    def task_two(self):
        self.client.get("/page2")

class MyUser(HttpUser):
    tasks = [MyTaskSet]


from locust import SequentialTaskSet, task, HttpUser

class MySequentialTasks(SequentialTaskSet):
    @task
    def step_1(self):
        self.client.get("/login")

    @task
    def step_2(self):
        self.client.get("/dashboard")

    @task
    def step_3(self):
        self.client.get("/logout")

class MyUser(HttpUser):
    tasks = [MySequentialTasks]
