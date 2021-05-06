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


    def competition_sample(self):
        data = [
            {"name": "Comp One","date": "2021-02-27 10:00:00","numberOfPlaces": "21"},
            {"name": "Comp Two","date": "2021-11-10 13:30:00","numberOfPlaces": "14"}
        ]
        server.competitions	= data
        return data

    def club_sample(self):
        data = [
            {"name":"Club One", "email":"mail_one@sample.com", "points":"6"},
            {"name":"Club Two", "email":"mail_two@sample.com", "points":"13"},
            {"name":"Club Three", "email":"mail_three@sample.com", "points":"70"}
        ]
        server.clubs = data
        return data


    @task
    def redeem(self):
        # self.default_competitions = server.competitions.copy()
        # self.default_clubs = server.clubs.copy()

        # self.competition_sample()
        # self.club_sample()
        # print(server.competitions)
        self.client.post("/purchasePlaces", data={
            "places": 1,
            "club": "Iron Temple",
            "competition": "Fall Classic",
        })
        # print(server.competitions)
        # print(server.clubs)
        # server.competitions = self.default_competitions.copy()
        # server.clubs = self.default_clubs.copy()

