import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.grade import Grade
from flask_jwt_extended import create_access_token,create_refresh_token
from flask_jwt_extended import jwt_required,get_jwt_identity,unset_jwt_cookies


class StudentGradeTestCase(unittest.TestCase):
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
    
    def test_get_all_student_grade(self):
        token = create_access_token(identity='sirmuso@gmail.com')

        headers = {
            'Authorization':f"Bearer {token}"
        }

        response = self.client.get('Grade/grades',headers =headers)

        assert response.status_code == 200

        assert response.json == []
<<<<<<< HEAD
    
=======


>>>>>>> e1e8c965db80292e5c4638b005e67ab20d97152d
    def test_get_studentgrade_by_id(self):
        grade = Grade(
            course_id = 1,
            email = 'sirmuso@gmail.com',
            student_id = 1,
            level = 101,
            matric_no = 'ALT/2023/STUDENT/1',
            score = 79,
            course_unit = 3,
            grade = 'A',
            grade_point = 12

        )

        grade.save()


        token = create_access_token(identity='sirmuso@gmail.com')

        headers = {
            'Authorization':f"Bearer {token}"
        }

        response = self.client.get('Grade/grade/1',headers =headers)

        assert response.status_code == 200
