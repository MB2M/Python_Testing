import time
from locust import HttpUser, task, between

import server


class User(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def index(self):
        self.client.get("/")

    @task
    def welcome(self):
        self.client.post("/showSummary", json={"email":"kate@shelifts.co.uk"})

    @task
    def book(self):
        for competition in server.competitions:
            for club in server.clubs:
                self.client.get("/book/" + competition['name'] + "/" + club['name'])
                time.sleep(1)

    @task
    def board(self):
        self.client.get("/board")

    # @task
    # def redeem(self):
    #     self.client()
