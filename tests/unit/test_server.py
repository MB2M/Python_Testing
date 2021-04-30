import json
import pytest

import server




class TestServer:

    def setup_method(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()
        self.default_competitions = server.competitions.copy()
        self.default_clubs = server.clubs.copy()

    def clean_up(self):
        server.competitions = self.default_competitions.copy()
        server.clubs = self.default_clubs.copy()


    @pytest.fixture(scope='function')
    def competition_sample(self):
        data = [
            {"name": "Comp One","date": "2021-02-27 10:00:00","numberOfPlaces": "21"},
            {"name": "Comp Two","date": "2021-11-10 13:30:00","numberOfPlaces": "14"}
        ]
        server.competitions	= data
        return data

    @pytest.fixture(scope='function')
    def club_sample(self):
        data = [
            {"name":"Club One", "email":"mail_one@sample.com", "points":"6"},
            {"name":"Club Two", "email":"mail_two@sample.com", "points":"13"},
            {"name":"Club Three", "email":"mail_three@sample.com", "points":"70"}
        ]
        server.clubs = data
        return data

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

    def redeem_points(self, club, competition, places_required):
        return self.app.post('/purchasePlaces', data={
            'places' : places_required,
            'club' : club,
            'competition': competition,
        }, follow_redirects=True)

    def test_points_update(self, club_sample, competition_sample):
        competition = competition_sample[1].copy()
        club = club_sample[0].copy()
        places_required = 1
        rv = self.redeem_points(club['name'], competition['name'], places_required)
        assert rv.status_code == 200
        assert int(server.clubs[0]['points']) == int(club['points']) - places_required * 3
        assert "Points available: " + str(int(club['points']) - places_required * 3) in rv.data.decode('utf-8')

    def test_book_old(self, club_sample, competition_sample):
        competition = competition_sample[0].copy()
        club = club_sample[0].copy()
        places_required = 1
        rv = self.redeem_points(club['name'], competition['name'], places_required)
        assert rv.status_code == 200
        assert competition['numberOfPlaces'] == server.competitions[0]['numberOfPlaces']
        assert "Sorry, past competition cannot be booked" in rv.data.decode('utf-8')

    def test_redeem_over_12(self, club_sample, competition_sample):
        competition = competition_sample[1].copy()
        club = club_sample[2].copy()
        places_required = 13
        rv = self.redeem_points(club['name'], competition['name'], places_required)
        assert rv.status_code == 200
        assert competition['numberOfPlaces'] == server.competitions[1]['numberOfPlaces']
        assert "Sorry, you can not redeem more than 12 points" in rv.data.decode('utf-8')

    def test_board(self):
        rv = self.app.get('/board', follow_redirects=True)
        assert rv.status_code == 200

    def post_email(self, email):
        return self.app.post('/showSummary', data={
            'email' : email
        }, follow_redirects=True)

    def test_unknow_login(self):
        email = 'email@unknow.test'
        rv = self.post_email(email)
        assert rv.status_code == 200
        print(rv.data.decode('utf-8'))
        assert "Sorry, that email was not found." in rv.data.decode('utf-8')

    def test_know_login(self, club_sample):
        email = 'mail_one@sample.com'
        rv = self.post_email(email)
        assert rv.status_code == 200
        assert 'Welcome, ' + email in rv.data.decode('utf-8')