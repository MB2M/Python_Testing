from typing import ByteString
import json

import server


class TestMaxRedeem:

    def setup_method(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()
        self.competitions = self.loadCompetitions()
        self.clubs = self.loadClubs()

    def loadClubs(self):
        with open('clubs.json') as c:
            listOfClubs = json.load(c)['clubs']
            return listOfClubs

    def loadCompetitions(self):
        with open('competitions.json') as comps:
            listOfCompetitions = json.load(comps)['competitions']
            return listOfCompetitions

    def redeem_points(self, club, competition, places_required):
        return self.app.post('/purchasePlaces', data={
            'places' : places_required,
            'club' : club,
            'competition': competition,
        }, follow_redirects=True)

    def test_redeem_over_12(self):
        competition = self.competitions[0]
        club = self.clubs[0]
        places_required = 13
        rv = self.redeem_points(club['name'], competition['name'], places_required)
        assert rv.status_code == 200
        assert competition['numberOfPlaces'] == server.competitions[0]['numberOfPlaces']
        assert "Sorry, you can not redeem more than 12 points" in rv.data.decode('utf-8')