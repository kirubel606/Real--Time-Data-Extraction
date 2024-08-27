import unittest
from app import app

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_successful_post(self):
        response = self.app.post('/api', json={
            "_id": 123,
            "formhub/uuid": "uuid123",
            "_submission_time": "2024-08-27T12:00:00",
            "_status": "submitted",
            "meta/instanceID": "instance123",
            "_xform_id_string": "form123"
        })
        # Assert the response code is 200 OK
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Data saved successfully", response.data)

    def test_post_with_missing_fields(self):
        response = self.app.post('/api', json={
            "_id": 123,
            "_submission_time": "2024-08-27T12:00:00"
        })
        # Assert the response code is 400 Bad Request
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing field", response.data)

    def test_post_with_no_json(self):
        response = self.app.post('/api', content_type='application/json', data="{}")
        # Assert the response code is 400 Bad Request, not 415 Unsupported Media Type
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Invalid data format", response.data)

if __name__ == '__main__':
    unittest.main()
