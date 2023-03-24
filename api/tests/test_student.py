import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.student import Student
from flask_jwt_extended import create_access_token,create_refresh_token
from flask_jwt_extended import jwt_required,get_jwt_identity,unset_jwt_cookies


class StudentTestCase(unittest.TestCase):
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
    def test_get_all_student(self):
        token = create_access_token(identity='sirmuso@gmail.com')

        headers = {
            'Authorization':f"Bearer {token}"
        }

        response = self.client.get('/Student/students',headers =headers)

        assert response.status_code == 200

        assert response.json == []

<<<<<<< HEAD


=======
>>>>>>> e1e8c965db80292e5c4638b005e67ab20d97152d
    def test_get_student_by_id(self):
        student = Student(
            lastname='Ade',
            firstname='Muso',
            othername='ola',
            email='sirmuso@gmail.com',
            user_id=1
        )

        student.save()


        token = create_access_token(identity='sirmuso@gmail.com')

        headers = {
            'Authorization':f"Bearer {token}"
        }

        response = self.client.get('/Student/students/1',headers =headers)

        assert response.status_code == 200
