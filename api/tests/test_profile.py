import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.profile import Profile
from flask_jwt_extended import create_access_token,create_refresh_token
from flask_jwt_extended import jwt_required,get_jwt_identity,unset_jwt_cookies


class ProfileTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])

        self.appctx = self.app.app_context()
        
        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None
    def test_get_all_profile(self):
        token = create_access_token(identity='sirmuso@gmail.com')

        headers = {
            'Authorization':f"Bearer {token}"
        }

        response = self.client.get('/profile/settings',headers =headers)

        assert response.status_code == 200

        assert response.json == []

    def test_create_profile(self):
        data = {
            'lastname':'Ade',
            'firstname':'Muso',
            'othername':'ola',
            'bio':'Admin',
            'gender':'Male',
            'user_id':1
        }
        token = create_access_token(identity='sirmuso@gmail.com')

        headers = {
            'Authorization':f"Bearer {token}"
        }

        response = self.client.post('/profile/settings',json=data,headers =headers)

        assert response.status_code == 200

        profiles = Profile.query.all()

        profile_id = profiles[0].id

        assert profile_id == 1

        assert len(profiles) == 1

        assert response.json['lastname']== 'Ade'

        assert response.json['gender']== 'Male'


    def test_get_profile_by_id(self):
        profile = Profile(
            lastname='Ade',
            firstname='Muso',
            othername='ola',
            bio='Admin',
            gender='Male',
            user_id=1
        )

        profile.save()


        token = create_access_token(identity='sirmuso@gmail.com')

        headers = {
            'Authorization':f"Bearer {token}"
        }

        response = self.client.post('/profile/settings/1',headers =headers)

        assert response.status_code == 200