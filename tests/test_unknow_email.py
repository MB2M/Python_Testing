import os
from flask import session
from typing import ByteString
import pytest

import server



class TestEmail:

    def setup_method(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

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

    def test_know_login(self):
        email = 'admin@irontemple.com'
        rv = self.post_email(email)
        assert rv.status_code == 200
        assert 'Welcome, ' + email in rv.data.decode('utf-8')