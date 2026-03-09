from locust import HttpUser, task, between

class TinycloudUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def get_url_mapping(self):
        self.client.get("/url-mapping/")