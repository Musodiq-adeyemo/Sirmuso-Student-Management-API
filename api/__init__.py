from flask import Flask
from flask_restx import Api
from .students.views import student_namespace
from .student_course.views import course_namespace
from .grading.views import grade_namespace
from .teachers.views import teacher_namespace
from .teacher_course.views import teachercourse_namespace
from .auth.views import auth_namespace
from .config.config import config_dict
from .profile.views import profile_namespace
from dotenv import load_dotenv
from .utils import db
from http import HTTPStatus
from flask_migrate import Migrate
from .models.student_course import StudentCourse
from .models.users import User
from .models.student import Student,StudentMatricNo
from .models.teacher import Teacher,StaffID
from .models.grade import Grade
from .models.teacher_course import TeacherCourse
from .models.profile import Profile,ProfileImage
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound,MethodNotAllowed

def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    load_dotenv()
    app.config.from_object(config)

    jwt = JWTManager(app)

    db.init_app(app)

    migrate = Migrate(app,db)

    
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {
            "message": "The token has expired",
            "error": "token_expired"
        }, HTTPStatus.UNAUTHORIZED
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {
            "message": "Token verification failed",
            "error": "invalid_token"
        }, HTTPStatus.UNAUTHORIZED
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {
            "message": "Request is missing an access token",
            "error": "authorization_required"
        }, HTTPStatus.UNAUTHORIZED
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback():
        return {
            "message": "The token is not fresh",
            "error": "fresh_token_required"
        }, HTTPStatus.UNAUTHORIZED

    authorizations = {
        'Bearer Auth': {
            "type":"apiKey",
            "in":"header",
            "name":"Authorization",
            "description":"Add a JWT token to the header with ** Bearer&Lt;JWT&gt;** token to authorize"
        }
    } 

    api = Api (
        app,
        title = 'Sirmuso Student Management API',
        description="A student management REST API service",
        authorizations= authorizations,
        security="Bearer Auth"
        )

    api.add_namespace(student_namespace)
    api.add_namespace(teacher_namespace)
    api.add_namespace(grade_namespace)
    api.add_namespace(course_namespace)
    api.add_namespace(teachercourse_namespace)
    api.add_namespace(auth_namespace,path='/auth')
    api.add_namespace(profile_namespace,path='/profile')

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error":"Method Not Allowed"}, 404

    @api.errorhandler(NotFound)
    def method_not_allowed(error):
        return {"error":"Not Found"}, 404

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db":db,
            "User":User,
            "Grade":Grade,
            "StudentCourse":StudentCourse,
            "Student":Student,
            "StaffID":StaffID,
            "StudentMatricNo":StudentMatricNo,
            "Teacher":Teacher,
            "TeacherCourse":TeacherCourse,
            "Profile":Profile,
            "ProfileImage":ProfileImage
        }

    return app