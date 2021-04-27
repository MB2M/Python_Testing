from typing import ByteString
import json

import server


class TestPointBoard:

    def setup_method(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    def point_board(self):
        return self.app.get('/board', follow_redirects=True)

    def test_redeem_over_12(self):
        rv = self.point_board()
        assert rv.status_code == 200