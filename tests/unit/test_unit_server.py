import requests
import json
import pytest
from pytest_mock import mocker
from flask import render_template


import server


class TestServer:

    def setup_method(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    def test_load_clubs(self):
        with open('clubs.json') as c:
            listOfClubs = json.load(c)['clubs']
        assert server.loadClubs() == listOfClubs

    def test_load_competitions(self):
        with open('competitions.json') as c:
            listOfCompetitions = json.load(c)['competitions']
        assert server.loadCompetitions() == listOfCompetitions

    def test_index(self):
        response = self.app.get('/')
        assert response.status_code == 200

    def test_board(self):
        rv = self.app.get('/board', follow_redirects=True)
        assert rv.status_code == 200

    def test_logout(self):
        rv = self.app.get('/logout', follow_redirects=True)
        assert rv.status_code == 200
