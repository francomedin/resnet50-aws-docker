from locust import HttpUser, TaskSet, task, between


class UserBehavior(TaskSet):
    @task(1)
    def index(self):
        self.client.get("http://localhost/")


    @task(3)
    def predict(self):
        file = [
            ("file", ("dog.jpeg", open("dog.jpeg", "rb"), "image/jpeg"))
        ]
        self.client.post(
            "http://localhost/predict",
            files   = file
        )

class APIUser(HttpUser):
    tasks  = [UserBehavior]
    wait_time = between(1,10)