from flask_restx import Namespace,Resource,fields,abort
from ..models.student_course import StudentCourse
from ..models.users import User
from api.relationship import display_student
from ..teacher_course.views import display_course
from http import HTTPStatus
from flask_jwt_extended import jwt_required,get_jwt_identity

course_namespace = Namespace("Course",description="Namespace for Course Registration")


course_model = course_namespace.model(
    'CourseRegister', {
       'course_id':fields.Integer(description='Course ID'),
       'email':fields.String(description='Student Email',required = True),
       'student_id':fields.Integer(description='Student ID',required = True),
       'matric_no': fields.String(description='Student Matriculation Number',required = True),
       'level': fields.Integer(description='Student Level',required = True),   
    }
)


show_course = course_namespace.model(
    'Course', {
       'id':fields.Integer(description='Course ID'),
       'matric_no': fields.String(description='Student Matriculation Number',required = True),
       'level': fields.Integer(description='Student Level',required = True),
       'courses':fields.Nested(display_course)
    }
)

student_course = course_namespace.model(
    'Courses', {
       'matric_no': fields.String(description='Student Matriculation Number',required = True),
       'courses':fields.Nested(display_course)
    }
)
course_display = course_namespace.model(
    'Course', {
       'students':fields.List(fields.Nested(display_student)),
       'courses':fields.Nested(display_course)
    }
)

student_list = course_namespace.model(
    'StudentList', {
       'course_id':fields.Integer(description='Course Unit',required = True),
       'courses':fields.Nested(display_course),
       'students':fields.List(fields.Nested(display_student))
    }
)

@course_namespace.route('/courses')
class RegisterGetCourse(Resource):
    @course_namespace.marshal_with(student_course)
    @course_namespace.doc(description='Get all Courses')
    @jwt_required()
    def get(self):
        """
        Get All Courses
        """
        courses = StudentCourse.query.all()

        return courses, HTTPStatus.OK
    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(show_course)
    @course_namespace.doc(description='Register Course')
    @jwt_required()
    def post(self):
        """
        Register Course(Student)
        """
        data = course_namespace.payload
        user_id = get_jwt_identity()

        user = User.get_by_id(user_id)
        if user.designation.upper() != "STUDENT":
            abort(401,desription='You are not authorized to perform this operation.Student only.')
        new_course = StudentCourse(
        course_id = data['course_id'],
        student_id = data['student_id'],
        email = data['email'],
        level = data['level'],
        matric_no = data['matric_no'],

        )
        new_course.save()
        
        return new_course, HTTPStatus.CREATED

        
@course_namespace.route('/course/<int:id>')
class GetUpdateDelete(Resource):
    @course_namespace.marshal_with(show_course)
    @course_namespace.doc(
        description='Retrieve Student Course',
        params = {
            'course_id': 'An ID for Course Registration'
        }
    )
    @jwt_required()
    def get(self,id):
        """
        Get Course by ID
        """
        course= StudentCourse.get_by_id(id)

        return course, HTTPStatus.OK
    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(show_course)
    @course_namespace.doc(description='Update Course')
    @jwt_required()
    def put(self,id):
        """
        Update Course by ID(Student)
        """
        course_update = StudentCourse.get_by_id(id)
        
        data = course_namespace.payload

        user_id = get_jwt_identity()

        user = User.get_by_id(user_id)
        if user.designation.upper() != "STUDENT":
            abort(401,desription='You are not authorized to perform this operation.Student only.')
        course_update.course_id = data['course_id'],
        course_update.student_id = data['student_id'],
        course_update.email = data['email'],
        course_update.level = data['level'],
        course_update.matric_no = data['matric_no'],
        course_update.update()
        
        return course_update,HTTPStatus.OK

        
    
    @course_namespace.doc(description='Delete Course')
    @jwt_required()
    def delete(self,id):
        """
        Delete  Course by ID(Student)
        """
        course_delete = StudentCourse.get_by_id(id)

        user_id = get_jwt_identity()

        user = User.get_by_id(user_id)
        if user.designation.upper() != "STUDENT":
            abort(401,desription='You are not authorized to perform this operation.Student only.')
        course_delete.delete()

        return {"message":f"Course with id {id} Delected Successfully"},HTTPStatus.OK



@course_namespace.route('/course/students/<int:course_id>')
class GetCourses(Resource):
    @course_namespace.marshal_with(student_list)
    @course_namespace.doc(
        description='Get All students Registered for the Course',
        params = {
            'course_id': 'Course Registration ID'
        }
        
    )
    @jwt_required()
    def get(self,course_id):
        """
        Retrieve All students Registered for the Course 
        """

        courses= StudentCourse.all()

        for course in courses:
            if course.course_id == course_id:

                return courses, HTTPStatus.OK

@course_namespace.route('/course/student/courses/<int:student_id>')
class GetStudentsCoursesID(Resource):
    @course_namespace.marshal_with(course_display)
    @course_namespace.doc(
        description='Get Student Courses by Student Identification Number',
        params = {
            'student_id': 'Student Identification Number'
        }

    )

    @jwt_required()
    def get(self,student_id):
        """
        Retrieve Student courses 
        """

        courses = StudentCourse.all()

        for course in courses:
            if course.student_id == student_id:

                return courses, HTTPStatus.OK


@course_namespace.route('/student/<int:student_id>/course/<int:course_id>')
class GetStudentCourseS(Resource):
    @course_namespace.marshal_with(course_display)
    @course_namespace.doc(
        description='Get Particular Course for a speciffic Student',
        params = {
            'student_id': 'Student Identification Number',
            'course_id':'Course Id'
        }

    )

    @jwt_required()
    def get(self,student_id,course_id):
        """
        Retrieve Student courses 
        """

        courses = StudentCourse.query.all()

        for course in courses:
            if course.student_id == student_id and course.course_id == course_id:

                return courses, HTTPStatus.OK
