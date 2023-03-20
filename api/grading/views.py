from flask_restx import Namespace,Resource,fields
from ..models.grade import Grade
from ..models.users import User
from ..teacher_course.views import display_course
from api.relationship import display_student
from http import HTTPStatus
from flask_jwt_extended import jwt_required,get_jwt_identity

grade_namespace = Namespace("Grade",description="Namespace for Students Grading")

grade_model = grade_namespace.model(
    'Register', {
       'email':fields.String(description='Student Email',required = True),
       'student_id':fields.Integer(description='Student ID',required = True),
       'course_id':fields.Integer(description='Course ID',required = True),
       'matric_no': fields.String(description='Student Matriculation Number',required = True),
       'score':fields.Integer(description='Student Score',required = True),
       'level': fields.Integer(description='Student Level',required = True),  
       'course_unit':fields.Integer(description='Course Unit',required = True), 
    }
)

show_grade = grade_namespace.model(
    'Grade', {
       'id':fields.Integer(description='Grade ID'),
       'course_id':fields.Integer(description='Course ID',required = True),
       'matric_no': fields.String(description='Student Matriculation Number',required = True),
       'score':fields.Integer(description='Student Score',required = True),
       'level': fields.Integer(description='Student Level',required = True),
       'grade':fields.String(description='Score Grade',required = True),
       'grade_point':fields.Float(description='Student Score',required = True),
       'students':fields.List(fields.Nested(display_student)),
       'course':fields.Nested(display_course)
    }
)

display_grade = grade_namespace.model(
    'Grades', {
       'course_id':fields.Integer(description='Course ID',required = True),
       'course':fields.Nested(display_course),
       'score':fields.Integer(description='Student Score',required = True),
       'grade':fields.String(description='Score Grade',required = True),
       'grade_point':fields.Float(description='Student Score',required = True),
    }
)

student_grade = grade_namespace.model(
    'StudentGrade', {
       'student_id':fields.Integer(description='Student ID',required = True),
       'matric_no': fields.String(description='Student Matriculation Number',required = True),
       'course':fields.Nested(display_course),
       'score':fields.Integer(description='Student Score',required = True),
       'grade':fields.String(description='Score Grade',required = True),
    }
)



@grade_namespace.route('/grades')
class SubmitGetScores(Resource):
    @grade_namespace.marshal_with(student_grade)
    @grade_namespace.doc(description='Get all Students Grade')
    @jwt_required()
    def get(self):
        """
        Get All Grades
        """
        grades = Grade.query.all()

        return grades, HTTPStatus.OK
    @grade_namespace.expect(grade_model)
    @grade_namespace.marshal_with(display_grade)
    @grade_namespace.doc(description='Submit Scores')
    @jwt_required()
    def post(self):
        """
        Submit Scores(Admin & Teacher)
        """
        data = grade_namespace.payload

        if data['score'] <= 100 and data['score'] >= 70 :
            grade = 'A'
            grade_point = 4 * data['course_unit']
        elif data['score'] <= 69 and data['score'] >= 60 :
            grade = 'B'
            grade_point = 3.5 * data['course_unit']
        elif data['score'] <= 59 and data['score'] >= 50 :
            grade = 'C'
            grade_point = 3 * data['course_unit']
        elif data['score'] <= 49 and data['score'] >= 45 :
            grade = 'CD'
            grade_point = 2 * data['course_unit']
        elif data['score'] <= 44 and data['score'] >= 40 :
            grade = 'D'
            grade_point = 1 * data['course_unit']
        elif data['score'] <= 39 and data['score'] >= 0 :
            grade = 'F'
            grade_point = 0 * data['course_unit']
        else:
            grade_point = 0

        email = get_jwt_identity()
        users = User.query.all()
        for user in users :
            if user.email == email and user.designation.upper() == 'ADMIN' or user.designation.upper() == 'TEACHER' :
                new_grade = Grade( 
                    course_id = data['course_id'],
                    email = data['email'],
                    student_id = data['student_id'],
                    level = data['level'],
                    matric_no = data['matric_no'],
                    score = data['score'],
                    course_unit = data['course_unit'],
                    grade = grade,
                    grade_point = grade_point

                )
                new_grade.save()
                
                return new_grade, HTTPStatus.CREATED
            else:
                response_object = {
                    'status':'fail',
                    'message':'You are not authorized to perform this operation.Admin only.'
                }
                return response_object


        

@grade_namespace.route('/grade/<int:grade_id>')
class GetUpdateDeleteScores(Resource):
    @grade_namespace.marshal_with(show_grade)
    @grade_namespace.doc(
        description='Retrieve Student Grade by ID',
        params = {
            'grade_id': 'An ID for Student Grade'
        }
    )
    @jwt_required()
    def get(self,grade_id):
        """
        Get Grade by ID
        """
        grade= Grade.get_by_id(grade_id)

        return grade, HTTPStatus.OK
    @grade_namespace.expect(grade_model)
    @grade_namespace.marshal_with(show_grade)
    @grade_namespace.doc(description='Update Score')
    @jwt_required()
    def put(self,grade_id):
        """
        Update Score by ID(Admin & Teacher)
        """
        grade_update = Grade.get_by_id(grade_id)
        
        data = grade_namespace.payload

        

        if data['score'] <= 100 and data['score'] >= 70 :
            grade = 'A'
            grade_point = 4 * data['course_unit']
        elif data['score'] <= 69 and data['score'] >= 60 :
            grade = 'B'
            grade_point = 3.5 * data['course_unit']
        elif data['score'] <= 59 and data['score'] >= 50 :
            grade = 'C'
            grade_point = 3 * data['course_unit']
        elif data['score'] <= 49 and data['score'] >= 45 :
            grade = 'CD'
            grade_point = 2 * data['course_unit']
        elif data['score'] <= 44 and data['score'] >= 40 :
            grade = 'D'
            grade_point = 1 * data['course_unit']
        elif data['score'] <= 39 and data['score'] >= 0 :
            grade = 'F'
            grade_point = 0 * data['course_unit']
        else:
            grade_point = 0
        
        email = get_jwt_identity()
        users = User.query.all()
        for user in users :
            if user.email == email and user.designation.upper() == 'ADMIN' or user.designation.upper() == 'TEACHER' :
                grade_update.email = data['email'],
                grade_update.student_id = data['student_id'],
                grade_update.course_unit = data['course_unit'],
                grade_update.level = data['level'],
                grade_update.matric_no = data['matric_no'],
                grade_update.score = data['score'],
                grade_update.grade = grade,
                grade_update.grade_point = grade_point
                grade_update.update()
                
                return grade_update,HTTPStatus.OK
            else:
                response_object = {
                    'status':'fail',
                    'message':'You are not authorized to perform this operation.Admin only.'
                }
                return response_object

        
    
    @grade_namespace.doc(description='Delete Grade')
    @jwt_required()
    def delete(self,course_id):
        """
        Delete  Grade by ID(Admin & Teacher)
        """
        grade_delete = Grade.get_by_id(course_id)

        email = get_jwt_identity()
        users = User.query.all()
        for user in users :
            if user.email == email and user.designation.upper() == 'ADMIN' or user.designation.upper() == 'TEACHER' :
                grade_delete.delete()

                return {"message":f"Grade with id {course_id} Delected Successfully"},HTTPStatus.OK

            else:
                response_object = {
                    'status':'fail',
                    'message':'You are not authorized to perform this operation.Admin only.'
                }
                return response_object


       
@grade_namespace.route('/grade/<int:course_id>')
class GetGradeByCourse(Resource):
    @grade_namespace.marshal_with(student_grade)
    @grade_namespace.doc(
        description='Get All Students Grade for a particular Course',
        params = {
            'course_id': 'Course Registration ID'
        }
        
    )
    @jwt_required()
    def get(self,course_id):
        """
        Retrieve All students Grade for a Course 
        """

        grades= Grade.query.all()

        for grade in grades:
            if grade.course_id == course_id:

                return grades, HTTPStatus.OK

@grade_namespace.route('/grade/grades/<int:student_id>')
class GetStudentGrades(Resource):
    @grade_namespace.marshal_with(display_grade)
    @grade_namespace.doc(
        description='Get Student grades by Identification Number',
        params = {
            'student_id': 'Student Identification Number'
        }

    )

    @jwt_required()
    def get(self,student_id):
        """
        Retrieve Student grades 
        """

        grades = Grade.query.all()

        for grade in grades:
            if grade.student_id == student_id:

                return grades, HTTPStatus.OK



@grade_namespace.route('/grades/gpa/<int:student_id>/level/<int:level>')
class GetStudentGp(Resource):
    @grade_namespace.doc(
        description='Get Student GPA by Student Identification Number and Level',
        params = {
            'student_id': 'Student Identification Number',
            'level': 'Student Level'
        }

    )

    @jwt_required()
    def get(self,student_id,level):
        """
        Student GPA (Student)
        """

        grades = Grade.query.all()

        units = []
        points = []
        total_grade_point = 0
        total_course_unit = 0
        gpa = 0

        for grade in grades:
            if grade.student_id == student_id and grade.level == level:
                units.append(grade.course_unit)
                points.append(grade.grade_point)
                for i in units:
                    total_course_unit += i
                for j in points:
                    total_grade_point += j
                    gpa= total_grade_point/total_course_unit
                
            return gpa


        return {"message":f"Your GPA for Level {level} is : {gpa}"},HTTPStatus.OK

        
