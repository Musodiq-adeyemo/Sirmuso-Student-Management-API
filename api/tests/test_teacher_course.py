import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.teacher_course import TeacherCourse
from flask_jwt_extended import create_access_token,create_refresh_token
from flask_jwt_extended import jwt_required,get_jwt_identity,unset_jwt_cookies


class TeacherCourseTestCase(unittest.TestCase):
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
    def test_get_all_teacher_courses(self):
        token = create_access_token(identity='sirmuso@gmail.com')

        headers = {
            'Authorization':f"Bearer {token}"
        }

        response = self.client.get('/TeacherCourse/teacher/courses',headers =headers)

        assert response.status_code == 200

        assert response.json == []


    def test_get_teachercourse_by_id(self):
        teachercourse = TeacherCourse(
            teacher_id = 1,
            course_title = 'Mathematic',
            course_code=  'mth101',
            course_unit = 3,
            staff_id = 'ALT/2023/STAFF/1'
        )

        teachercourse.save()


        token = create_access_token(identity='sirmuso@gmail.com')

        headers = {
            'Authorization':f"Bearer {token}"
        }

        response = self.client.get('/TeacherCourse/teacher/course/1',headers =headers)

        assert response.status_code == 200
