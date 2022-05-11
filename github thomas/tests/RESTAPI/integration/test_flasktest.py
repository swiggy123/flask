import HogwartsREST
import unittest
import json

class TestCaseIndexRoute(unittest.TestCase):

    def setUp(self):
        HogwartsREST.app.testing = True
        self.app = HogwartsREST.app.test_client()

    def test_home(self):
        result = self.app.get('/')
        # Make your assertions
        self.assertEqual(result.get_data(), b'Hello World! I feel good')

class TestCaseGetHouse(unittest.TestCase):

    def setUp(self):
        HogwartsREST.app.testing = True
        self.app = HogwartsREST.app.test_client()

    def test_house_route(self):
        response = self.app.get('/House/2')
        
        assert response.status_code == 200
        assert response.get_data()== b'[{"animal":"Badger","founder":"Helga Hufflepuff","ghost":"Fat Friar","house_id":2,"location":"Basement","name":"Hufflepuff"}]\n'
        assert json.loads(response.get_data()) == {'house_id':'2', 'name': 'Hufflepuff', 'founder':'Helga Hufflepuff', 'animal':'Badger', 'ghost':'Fat Friar', 'location':'Basement'}

class TestCaseCreatePersonwithoutbirthdate(unittest.TestCase):

    def setUp(self):
        HogwartsREST.app.testing = True
        self.app = HogwartsREST.app.test_client()

    def test_person_route(self):
        response=self.app.post('/NewStudent', data=json.dumps(dict({"person_id":0,"first_name":"Seamus","name":"Finnigan","gender":"male","blood_purity":"half-blood"})), content_type='application/json')
                
        assert response.status_code != 200


if __name__ == '__main__':
    unittest.main()