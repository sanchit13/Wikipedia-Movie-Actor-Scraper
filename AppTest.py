import unittest
import requests

class AppTest(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:5000"

    def test_getAllActorsTest(self):
        response = requests.get(self.base_url + "/actors/all")
        self.assertTrue(len(response.json()["Actors"]) > 309)

    def test_getActorByName(self):
        response = requests.get(self.base_url + "/actors/Danny%20McBride")
        self.assertEqual(response.status_code, 200)

    def test_getActorThatDoesntExist(self):
        response = requests.get(self.base_url + "/actors/Sanchita%20McBride")
        self.assertEqual(response.status_code, 404)

    def test_deleteActorThatDoesNotExist(self):
        response = requests.delete(self.base_url + "/actors/Sanchita%20McBride")
        self.assertEqual(response.status_code, 404)

    def test_getAllActorsTest(self):
        response = requests.get(self.base_url + "/movies/all")
        self.assertTrue(len(response.json()["Movies"]) > 100)

    def test_getActorsByFilter(self):
        response = requests.get(self.base_url + "/actors?age=45")
        self.assertTrue(len(response.json()["Success"]) > 2)

if __name__ == "__main__":
	unittest.main()