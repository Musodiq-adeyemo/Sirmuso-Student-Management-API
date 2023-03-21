import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.student_course import StudentCourse
from flask_jwt_extended import create_access_token,create_refresh_token
from flask_jwt_extended import jwt_required,get_jwt_identity,unset_jwt_cookies


class StudentCourseTestCase(unittest.TestCase):
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
    def test_get_all_student_courses(self):
        token = create_access_token(identity='sirmuso@gmail.com')

        headers = {
            'Authorization':f"Bearer {token}"
        }

        response = self.client.get('Course/courses',headers =headers)

        assert response.status_code == 200

        assert response.json == []

    
    def test_get_studentcourse_by_id(self):
        studentcourse = StudentCourse(
            student_id = 1,
            email = 'sirmuso@gmail.com',
            level=  101,
            course_id = 1,
            matric_no = 'ALT/2023/STUDENT/1'
        )

        studentcourse.save()


        token = create_access_token(identity='sirmuso@gmail.com')

        headers = {
            'Authorization':f"Bearer {token}"
        }

        response = self.client.get('Course/course/1',headers =headers)

        assert response.status_code == 200
