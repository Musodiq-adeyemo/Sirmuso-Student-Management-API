from flask_restx import Namespace,Resource,fields
from ..models.student import Student,StudentMatricNo
from ..models.users import User
from ..teacher_course.views import display_course
from ..grading.views import display_grade
from ..auth.views import show_user
from http import HTTPStatus
from flask_jwt_extended import jwt_required,get_jwt_identity

student_namespace = Namespace("Student",description="Namespace for Student Registration")

student_model = student_namespace.model(
    'StudentRegister', {
       'user_id':fields.Integer(description='Student User ID',required = True),
       'email':fields.String(description='Student Email',required = True),
       'lastname':fields.String(description='Student Surname',required = True),
       'firstname': fields.String(description='Student firstname',required = True),
       'othername':fields.String(description='Student othername',required = True),   
    }
)


display_student = student_namespace.model(
    'Students', {
       'id':fields.Integer(description='Student ID'),
       'lastname':fields.String(description='Student Surname',required = True),
       'firstname': fields.String(description='Student firstname',required = True),  
    }
)


matricNo = student_namespace.model(
    'Matric', {
       'student_id':fields.Integer(description='Student  ID',required = True),
       'email':fields.String(description='Student Email',required = True),
       'user_id':fields.Integer(description='Student ID',required = True),
    }
)

show_matricNo = student_namespace.model(
    'StudentMatric', {
       'student_id':fields.Integer(description='Student ID',required = True),
       'matric_no' :fields.String(description='Student Matriculation Number',required = True),
       'student':fields.List(fields.Nested(display_student))
    }
)

show_student = student_namespace.model(
    'Student', {
       'id':fields.Integer(description='Student ID'),
       'lastname':fields.String(description='Student Surname',required = True),
       'firstname': fields.String(description='Student firstname',required = True),
       'othername':fields.String(description='Student othername',required = True),  
       'user' :fields.Nested(show_user),
    }
)


student_course = student_namespace.model(
    'StudentCourses', {
       'lastname':fields.String(description='Student Surname',required = True),
       'firstname': fields.String(description='Student firstname',required = True),
       'student_course':fields.List(fields.Nested(display_course))
    }
)

student_grade = student_namespace.model(
    'StudentGrades', {
       'lastname':fields.String(description='Student Surname',required = True),
       'firstname': fields.String(description='Student firstname',required = True),
       'student_grade':fields.List(fields.Nested(display_grade))
    }
)

@student_namespace.route('/students')
class RegisterGetStudent(Resource):
    @student_namespace.marshal_with(display_student)
    @student_namespace.doc(description='Get all Students')
    @jwt_required()
    def get(self):
        """
        Get All Students
        """
        students = Student.query.all()

        return students, HTTPStatus.OK
    @student_namespace.expect(student_model)
    @student_namespace.marshal_with(show_student)
    @student_namespace.doc(description='Register Student')
    @jwt_required()
    def post(self):
        """
        Register Student(Admin)
        """
        data = student_namespace.payload
        email = get_jwt_identity()

        users = User.query.all()
        for user in users :
            if user.email == email and user.designation.upper() == 'ADMIN':
                new_student = Student(
                    lastname = data['lastname'],
                    firstname = data['firstname'],
                    othername = data['othername'],
                    email = data['email'],
                    user_id = data['user_id'],
                )
                
                new_student.save()
                
                return new_student, HTTPStatus.CREATED
            else:
                response_object = {
                    'status':'fail',
                    'message':'You are not authorized to perform this operation.Admin only.'
                }
                return response_object

@student_namespace.route('/students/<int:student_id>')
class GetUpdateDeleteStudents(Resource):
    @student_namespace.marshal_with(show_student)
    @student_namespace.doc(
        description='Retrieve Student Information by Student Registration Id',
        params = {
            'student_id': 'An ID for Student Registration'
        }
    )
    @jwt_required()
    def get(self,student_id):
        """
        Get Student by ID
        """
        student = Student.get_by_id(student_id)

        return student, HTTPStatus.OK
    @student_namespace.expect(student_model)
    @student_namespace.marshal_with(show_student)
    @student_namespace.doc(description='Update Student By ID')
    @jwt_required()
    def put(self,student_id):
        """
        Update Student Information by ID(Admin)
        """
        email = get_jwt_identity()
        student_update = Student.get_by_id(student_id)
        
        data = student_namespace.payload
        
        student_update.lastname = data['lastname'],
        student_update.firstname = data['firstname'],
        student_update.othername = data['othername'],
        student_update.email = data['email'],
        student_update.user_id = data['user_id'],
        
        users = User.query.all()
        for user in users :
            if user.email == email and user.designation.upper() == 'ADMIN':
                student_update.update()
                return student_update,HTTPStatus.OK
            else:
                response_object = {
                    'status':'fail',
                    'message':'You are not authorized to perform this operation.Admin only.'
                }
                return response_object
    
    @student_namespace.doc(description='Delete Student')
    @jwt_required()
    def delete(self,student_id):
        """
        Delete Student by ID(Admin)
        """
        email = get_jwt_identity()
        student_delete = Student.get_by_id(student_id)

        users = User.query.all()
        for user in users :
            if user.email == email and user.designation.upper() == 'ADMIN':
                student_delete.delete()

                return {"message":"Student Dashboard Delected Successfully"},HTTPStatus.OK

            else:
                response_object = {
                    'status':'fail',
                    'message':'You are not authorized to perform this operation.Admin only.'
                }
                return response_object

        
@student_namespace.route('/students/course/<int:student_id>')
class GetStudentC(Resource):
    @student_namespace.marshal_with(student_course)
    @student_namespace.doc(
        description='Get Student Courses by student identification Number',
        params = {
            'student_id': 'Student identification Number'
        }

    )


    @jwt_required()
    def get(self,student_id):
        """
        Retrieve Student courses 
        """

        student_course = Student.get_by_id(student_id)


        return student_course, HTTPStatus.OK

    @student_namespace.marshal_with(student_grade)
    @student_namespace.doc(
        description='Get Student grades by student identification Number',
        params = {
            'student_id': 'Student identification Number'
        }

    )

    @jwt_required()
    def get(self,student_id):
        """
        Retrieve Student courses 
        """

        student_grade = Student.get_by_id(student_id)


        return student_grade, HTTPStatus.OK

@student_namespace.route('/students/matric')
class GetMatricNo(Resource):
    @student_namespace.expect(matricNo)
    @student_namespace.marshal_with(show_matricNo)
    @student_namespace.doc(description='Generate student matric number')
    @jwt_required()
    def post(self):
        """
        Generate Student Matric Number(Admin)
        """
        data = student_namespace.payload

        email = get_jwt_identity()
        users = User.query.all()
        for user in users :
            if user.email == email and user.designation.upper() == 'ADMIN':
                new_matric = StudentMatricNo(
                student_id = data['student_id'],
                email = data['email'],
                matric_no = "ALT/2023/STUDENT/" + str(data['student_id'])
                )
            
                new_matric.save()
                
                return new_matric, HTTPStatus.CREATED

            else:
                response_object = {
                    'status':'fail',
                    'message':'You are not authorized to perform this operation.Admin only.'
                }
                return response_object
        
@student_namespace.route('/students/matric/<int:user_id>')
class GetMatricNumber(Resource):
    @student_namespace.marshal_with(show_matricNo)
    @student_namespace.doc(
        description='Get your Matriculation Number',
    )

    @jwt_required()
    def get(self,user_id):
        """
        Get Student Matriculation Number(Student)
        """
        email = get_jwt_identity()

        matrics = StudentMatricNo.query.all()

        for matric in matrics :
            if matric.user_id == user_id :
                return matrics, HTTPStatus.OK

        

        

@student_namespace.route('/students/users/<int:user_id>')
class GetStudentsByUserId(Resource):
    @student_namespace.marshal_with(show_student)
    @student_namespace.doc(
        description='Get Student Information by User ID',
        params = {
            'user_id': 'User Identification Number'
        }

    )

    @jwt_required()
    def get(self,user_id):
        """
        Retrieve Student by User ID
        """

        students = Student.query.all()
        for student in students:
            if student.user_id ==user_id:

                return students, HTTPStatus.OK

