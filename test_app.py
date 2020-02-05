import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class CastingTestCase(unittest.TestCase):
    """This class represents the casting test case"""

    def setUp(self):
            """Define test variables and initialize app."""
            self.app = create_app()
            self.client = self.app.test_client
            self.database_name = "casting_dev"
            self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
            self.producer_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1FUTRNVGczUmtJek1rTkJPVFl6UVRVd09EUkVOalZDTXpFek1FUkdSamxCTkRJNU5ESkdSZyJ9.eyJpc3MiOiJodHRwczovL2Rldi02aWQzOWFvci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUxY2YyOWVmYWNkMDUwZTdiNWE3ODhkIiwiYXVkIjpbImNhc3RpbmdhcGkiLCJodHRwczovL2Rldi02aWQzOWFvci5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTc5NTc4NTc1LCJleHAiOjE1Nzk2NjQ5NzUsImF6cCI6IktkRzdOZ0ZOeUJFZEtvMFNxRTJXUldjaUtteURTVXFlIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.zDS_LbTUh7SBtmmy8wBs0LIIDYbob8cTjurB97OJAqg-nATGPfuwf6gwWuNgSIiADu8gYnBFAE61n6ugrA16l2SXMkj09Ab0NvU5eqdBpjhFU5EsIlPF2k0sQpZJ6IHAujn59oMYERHJ-mOqnFrQvatxfXnX3s-Utj0k7aKg0uAKmTIzbUlVYvKN-JpP_a7o03Iikp0jwQ9DwDGKzubBdl4DoNeKrCnINu_t_PcXzyD_2Zk1esmUy22bzFNjTr-wAdiNhCfmhjfQzcY7JMi3PNSbvKNs4NrBz-UBnrEdRTK5rgRtLpYgChNPLVzK4eoYRrrxa3fdYwdqC6B4XLck-g"
            self.director_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1FUTRNVGczUmtJek1rTkJPVFl6UVRVd09EUkVOalZDTXpFek1FUkdSamxCTkRJNU5ESkdSZyJ9.eyJpc3MiOiJodHRwczovL2Rldi02aWQzOWFvci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUxY2YxN2I2YWMwNTMwZWE3MzU4ZWEzIiwiYXVkIjpbImNhc3RpbmdhcGkiLCJodHRwczovL2Rldi02aWQzOWFvci5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTc5NTc4NDExLCJleHAiOjE1Nzk2NjQ4MTEsImF6cCI6IktkRzdOZ0ZOeUJFZEtvMFNxRTJXUldjaUtteURTVXFlIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.MlAOInUk8uTpp3aj4108s8FF_s4M0hd4_6OKG6O4pj9eFFvub9F22iBjToRZKgim_lGC-UD6DMuwubloiu0RImlHRN7cn3R3uUzRzn-ySf8vhkozxoMxVj8vLaDfRCYHptTYCM2QaHz4O_uDu851CaM4u0QefOYSRefOJj7219Dn0HtLE8STs9ei0T_bK6Jb1JffhmZjaYNkj_ARNYkLtmrFAbIR_BLpgk3tanhYWoUT0-oiCA9yuEVEfB67L4OaS_rWX2S-WKlZBED3ryuy_pfMf47B9OFMd7Cy6Yc1JduS_CWVDB-Ud-vV5q3OaSm3sGtmenOdx72XXklFG-iKOA"
            setup_db(self.app, self.database_path)
            self.headers = {'Content-Type': 'application/json'}
            # binds the app to the current context
            with self.app.app_context():
                self.db = SQLAlchemy()
                self.db.init_app(self.app)
                # create all tables
                self.db.create_all()
        
    def tearDown(self):
        """Executed after reach test"""
        pass
    
# movies table tests using the producer role

    # movies add endpoint tests using producer role
    def test_new_movies(self):
        """Test _____________ """
        info = {"title": "guardians of the galaxy", "release_date": "2014-08-01"}
        self.headers.update({'Authorization': 'Bearer ' + self.producer_token})
        res = self.client().post('/movies_new', data=json.dumps(info), headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_404_new_movies(self):
        """Test _____________ """
        res = self.client().post('/movies_new/100000')
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'Not found')
        self.assertEqual(res.status_code, 404)

     # movies patch endpoint tests using producer role
    def test_patch_movies(self):
        """Test _____________ """
        info = {"title": "guardians of the galaxy 2", "release_date": "2017-05-05"}
        self.headers.update({'Authorization': 'Bearer ' + self.producer_token})
        res = self.client().patch('/movies/1', data=json.dumps(info), headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_422_patch_movies(self):
        """Test _____________ """
        info = {"title": "guardians of the galaxy 2", "release_date": "2017-05-05"}
        self.headers.update({'Authorization': 'Bearer ' + self.producer_token})
        res = self.client().patch('/movies/100000', data=json.dumps(info), headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'unprocessable')
        self.assertEqual(res.status_code, 422)

    # movies endpoint tests 
    def test_movies(self):
        """Test _____________ """
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 200)

    def test_405_movies(self):
        """Test _____________ """
        res = self.client().get('/movies/1')
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'Method Not Allowed')
        self.assertEqual(res.status_code, 405)

    # movies delete endpoint tests using producer role
    def test_delete_movies(self):
        """Test _____________ """
        self.headers.update({'Authorization': 'Bearer ' + self.producer_token})
        res = self.client().delete('/movies/2', headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_422_movies(self):
        """Test _____________ """
        self.headers.update({'Authorization': 'Bearer ' + self.producer_token})
        res = self.client().delete('/movies/10000', headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'unprocessable')
        self.assertEqual(res.status_code, 422)

# actors table tests using the director role

    # actors add endpoint tests using the director role *** age is integer in table ***
    def test_new_actors(self):
        """Test _____________ """
        info = {"name": "Chris Pratt", "age":40, "gender": "male"}
        self.headers.update({'Authorization': 'Bearer ' + self.director_token})
        res = self.client().post('/actors_new', data=json.dumps(info), headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_404_new_actors(self):
        """Test _____________ """
        res = self.client().post('/actors_new/100000')
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'Not found')
        self.assertEqual(res.status_code, 404)

     # actors patch endpoint tests using director role *** age is integer in table ***
    def test_patch_actors(self):
        """Test _____________ """
        info = {"name": "Zoe Saldana", "age":41, "gender": "female"}
        self.headers.update({'Authorization': 'Bearer ' + self.director_token})
        res = self.client().patch('/actors/1', data=json.dumps(info), headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_422_patch_actors(self):
        """Test _____________ """
        info = {"name": "Zoe Saldana", "age":41, "gender": "female"}
        self.headers.update({'Authorization': 'Bearer ' + self.director_token})
        res = self.client().patch('/actors/100000', data=json.dumps(info), headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'unprocessable')
        self.assertEqual(res.status_code, 422)

    # actors endpoint tests 
    def test_actors(self):
        """Test _____________ """
        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 200)

    def test_405_actors(self):
        """Test _____________ """
        res = self.client().get('/actors/1')
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'Method Not Allowed')
        self.assertEqual(res.status_code, 405)

    # actors delete endpoint tests using director role
    def test_delete_actors(self):
        """Test _____________ """
        self.headers.update({'Authorization': 'Bearer ' + self.director_token})
        res = self.client().delete('/actors/2', headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def test_422_actors(self):
        """Test _____________ """
        self.headers.update({'Authorization': 'Bearer ' + self.director_token})
        res = self.client().delete('/actors/1000000', headers=self.headers)
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'unprocessable')
        self.assertEqual(res.status_code, 422)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
