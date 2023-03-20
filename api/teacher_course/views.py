from flask_restx import Namespace,Resource,fields
from ..models.users import User
from ..models.teacher_course import TeacherCourse
from api.relationship import display_teacher
from http import HTTPStatus
from flask_jwt_extended import jwt_required,get_jwt_identity

teachercourse_namespace = Namespace("TeacherCourse",description="Namespace for Teacher Course Registration")

teachercourse_model = teachercourse_namespace.model(
    'TeacherRegister', {
       'teacher_id':fields.Integer(description='Teacher Identification Number',required = True),
       'course_title':fields.String(description='Course Title',required = True),
       'course_code':fields.String(description='Course Code',required = True),
       'course_unit':fields.Integer(description='Course Unit',required = True),
       'staff_id': fields.String(description='Staff Identification Number',required = True),
          
    }
)

show_course = teachercourse_namespace.model(
    'TeacherCourse', {
       'id':fields.Integer(description='Course ID'),
       'course_title':fields.String(description='Course Title',required = True),
       'course_code':fields.String(description='Course Code',required = True),
       'course_unit':fields.Integer(description='Course Unit',required = True),
       'staff_id': fields.String(description='Staff Identification Number',required = True),
       'lecturer':fields.Nested(display_teacher)
    }
)

display_course = teachercourse_namespace.model(
    'TeacherCourse', {
       'id':fields.Integer(description='Course ID'),
       'course_title':fields.String(description='Course Title',required = True),
       'course_code':fields.String(description='Course Code',required = True),
       'course_unit':fields.Integer(description='Course Unit',required = True),
    }
)



course_lecturer = teachercourse_namespace.model(
    'Lecturer', {
       'course_title':fields.String(description='Course Title',required = True),
       'course_code':fields.String(description='Course Code',required = True),
       'lecturer':fields.Nested(display_teacher)
    }
)

@teachercourse_namespace.route('/teacher/courses')
class RegisterGetTeacherCourse(Resource):
    @teachercourse_namespace.marshal_with(display_course)
    @teachercourse_namespace.doc(description='Get all Courses')
    @jwt_required()
    def get(self):
        """
        Get All Courses
        """
        courses = TeacherCourse.query.all()

        return courses, HTTPStatus.OK
    @teachercourse_namespace.expect(teachercourse_model)
    @teachercourse_namespace.marshal_with(show_course)
    @teachercourse_namespace.doc(description='Register Course')
    @jwt_required()
    def post(self):
        """
        Register Course(Teacher)
        """
        data = teachercourse_namespace.payload
        email = get_jwt_identity()
        users = User.query.all()
        for user in users :
            if user.email == email and user.designation.upper() == 'TEACHER':
                new_course = TeacherCourse(
                teacher_id = data['teacher_id'],
                course_title = data['course_title'],
                course_code = data['course_code'],
                course_unit = data['course_unit'],
                staff_id = data['staff_id'],

                )
                new_course.save()
                
                return new_course, HTTPStatus.CREATED
            else:
                response_object = {
                    'status':'fail',
                    'message':'You are not authorized to perform this operation.Admin only.'
                }
                return response_object
        

@teachercourse_namespace.route('/teacher/course/<int:course_id>')
class GetUpdateDeleteTeacherCourses(Resource):
    @teachercourse_namespace.marshal_with(show_course)
    @teachercourse_namespace.doc(
        description='Retrieve Teacher Course by id',
        params = {
            'course_id': 'An ID for Course Registration'
        }
    )
    @jwt_required()
    def get(self,course_id):
        """
        Get Teacher Course by ID
        """
        course= TeacherCourse.get_by_id(course_id)

        return course, HTTPStatus.OK
    @teachercourse_namespace.expect(teachercourse_model)
    @teachercourse_namespace.marshal_with(show_course)
    @teachercourse_namespace.doc(description='Update Course')
    @jwt_required()
    def put(self,course_id):
        """
        Update Course by ID(Teacher)
        """
        course_update = TeacherCourse.get_by_id(course_id)
        
        data = teachercourse_namespace.payload

        email = get_jwt_identity()
        users = User.query.all()
        for user in users :
            if user.email == email and user.designation.upper() == 'TEACHER':
                course_update.teacher_id = data['teacher_id'],
                course_update.course_title = data['course_title'],
                course_update.course_code = data['course_code'],
                course_update.course_unit = data['course_unit'],
                course_update.staff_id = data['staff_id'],
                course_update.update()
                
                return course_update,HTTPStatus.OK
            else:
                response_object = {
                    'status':'fail',
                    'message':'You are not authorized to perform this operation.Admin only.'
                }
                return response_object
        
    
    @teachercourse_namespace.doc(description='Delete Course')
    @jwt_required()
    def delete(self,course_id):
        """
        Delete  Course by ID(Teacher)
        """
        course_delete = TeacherCourse.get_by_id(course_id)

        email = get_jwt_identity()
        users = User.query.all()
        for user in users :
            if user.email == email and user.designation.upper() == 'TEACHER':
                course_delete.delete()

                return {"message":f"Course with id {id} Delected Successfully"},HTTPStatus.OK

            else:
                response_object = {
                    'status':'fail',
                    'message':'You are not authorized to perform this operation.Admin only.'
                }
                return response_object


@teachercourse_namespace.route('/teacher/course/courses/<int:course_id>')
class GetLecturerCourses(Resource):
    @teachercourse_namespace.marshal_with(course_lecturer)
    @teachercourse_namespace.doc(
        description='Get the Lecturer for a Course',
        params = {
            'course_id': 'Course Registration ID'
        }
        
    )
    @jwt_required()
    def get(self,course_id):
        """
        Retrieve Lecturer for a Course 
        """

        course= TeacherCourse.get_by_id(course_id)

        return course, HTTPStatus.OK


@teachercourse_namespace.route('/course/teacher/<int:teacher_id>')
class GetTeacherCourses(Resource):
    @teachercourse_namespace.marshal_with(display_course)
    @teachercourse_namespace.doc(
        description='Get Lecturer all Courses by teacher ID',
        params = {
            'teacher_id': 'Staff Identification Number'
        }

    )

    @jwt_required()
    def get(self,teacher_id):
        """
        Retrieve All Lecturer courses 
        """

        courses = TeacherCourse.query.all()
        for course in courses:
            if course.teacher_id == teacher_id:

                return courses, HTTPStatus.OK

    