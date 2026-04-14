from locust import HttpUser, task, constant
import random
import time
import uuid


class TestUser(HttpUser):
    """Пользователь для нагрузочного тестирования"""
    wait_time = constant(0)  # Без пауз для максимального RPS

    def on_start(self):
        self.user_ids = []
        self.counter = 0

    @task(15)  # Больше чтения
    def get_all_users(self):
        """GET /users/ - самый быстрый запрос"""
        skip = random.randint(0, 100)
        self.client.get(f"/users/?skip={skip}&limit=20", name="/users/")

    @task(5)
    def get_external_posts(self):
        """GET /external/posts/"""
        self.client.get("/external/posts/?limit=10", name="/external/posts/")

    @task(3)
    def get_user_by_id(self):
        """GET /users/{id}"""
        if self.user_ids:
            user_id = random.choice(self.user_ids)
            self.client.get(f"/users/{user_id}", name="/users/{id}")
        else:
            self.client.get("/users/?limit=5", name="/users/")

    @task(1)  # Меньше записи при высокой нагрузке
    def create_user(self):
        """POST /users/ - создание"""
        self.counter += 1
        # Используем UUID для 100% уникальности
        unique_id = str(uuid.uuid4())[:8]
        timestamp = int(time.time() * 1000)

        payload = {
            "email": f"l{timestamp}{unique_id}@t.com",
            "username": f"u{timestamp}{unique_id}",
            "full_name": f"User"
        }

        with self.client.post("/users/", json=payload, catch_response=True) as resp:
            if resp.status_code in [201, 400]:
                resp.success()
            else:
                resp.failure(f"Status: {resp.status_code}")
