import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.teacher import Teacher
from flask_jwt_extended import create_access_token,create_refresh_token
from flask_jwt_extended import jwt_required,get_jwt_identity,unset_jwt_cookies


class TeacherTestCase(unittest.TestCase):
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
    def test_get_all_teacher(self):
        token = create_access_token(identity='sirmuso@gmail.com')

        headers = {
            'Authorization':f"Bearer {token}"
        }

        response = self.client.get('/Teacher/teachers',headers =headers)

        assert response.status_code == 200

        assert response.json == []



    def test_get_teacher_by_id(self):
        teacher = Teacher(
            lastname='Ade',
            firstname='Muso',
            othername='ola',
            email='sirmuso@gmail.com',
            user_id=1
        )

        teacher.save()


        token = create_access_token(identity='sirmuso@gmail.com')

        headers = {
            'Authorization':f"Bearer {token}"
        }

        response = self.client.get('/Teacher/teachers/1',headers =headers)

        assert response.status_code == 200