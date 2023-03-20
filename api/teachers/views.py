from flask_restx import Namespace,Resource,fields
from ..models.teacher import Teacher,StaffID
from ..models.users import User
from ..auth.views import show_user
from ..teacher_course.views import display_course
from http import HTTPStatus
from flask_jwt_extended import jwt_required,get_jwt_identity

teacher_namespace = Namespace("Teacher",description="Namespace for Staff Registration")


teacher_model = teacher_namespace.model(
    'RegisterTeacher', {
       'user_id':fields.Integer(description='Teacher User ID',required = True),
       'email':fields.String(description='Teacher Email',required = True),
       'lastname':fields.String(description='Teacher Surname',required = True),
       'firstname': fields.String(description='Teacher firstname',required = True),
       'othername':fields.String(description='Teacher othername',required = True),   
    }
)



display_teacher = teacher_namespace.model(
    'Teachers', {
       'id':fields.Integer(description='Teacher ID'),
       'lastname':fields.String(description='Teacher Surname',required = True),
       'firstname': fields.String(description='Teacher firstname',required = True),  
    }
)

staff_model= teacher_namespace.model(
    'Staff_id', {
       'teacher_id':fields.Integer(description='Teacher  ID',required = True),
       'email':fields.String(description='Teacher Email',required = True),
       'user_id':fields.Integer(description='Student ID',required = True),
    }
)

show_staffId = teacher_namespace.model(
    'TeacherStaff', {
       'staff_id' :fields.String(description='Teacher Identification Number',required = True),
       'teacher':fields.List(fields.Nested(display_teacher))
    }
)

show_teacher = teacher_namespace.model(
    'Teacher', {
       'id':fields.Integer(description='Teacher ID'),
       'lastname':fields.String(description='Teacher Surname',required = True),
       'firstname': fields.String(description='Teacher firstname',required = True),
       'othername':fields.String(description='Teacher othername',required = True),  
       'user':fields.List(fields.Nested(show_user))
    }
)


teacher_staffId = teacher_namespace.model(
    'StaffId', {
       'user_id':fields.Integer(description='Student User ID',required = True),
       'lastname':fields.String(description='Student Surname',required = True),
       'firstname': fields.String(description='Student firstname',required = True),  
       'matric_no' :fields.String(description='Student Matriculation Number',required = True),
    }
)

teacher_course = teacher_namespace.model(
    'TCourses', {
       'lastname':fields.String(description='Teacher Surname',required = True),
       'firstname': fields.String(description='Teacher firstname',required = True),
       'teacher_course':fields.List(fields.Nested(display_course))
    }
)

@teacher_namespace.route('/teachers')
class RegisterGetTeacher(Resource):
    @teacher_namespace.marshal_with(display_teacher)
    @teacher_namespace.doc(description='Get all Teachers')
    @jwt_required()
    def get(self):
        """
        Get All Teachers
        """
        teachers = Teacher.query.all()

        return teachers, HTTPStatus.OK
    @teacher_namespace.expect(teacher_model)
    @teacher_namespace.marshal_with(show_teacher)
    @teacher_namespace.doc(description='Register Teacher')
    @jwt_required()
    def post(self):
        """
        Register Teacher(Admin)
        """
        data = teacher_namespace.payload
        email = get_jwt_identity()
        users = User.query.all()
        for user in users :
            if user.email == email and user.designation.upper() == 'ADMIN':
                new_teacher = Teacher(
                lastname = data['lastname'],
                firstname = data['firstname'],
                othername = data['othername'],
                email = data['email'],
                user_id = data['user_id'],

            )
                new_teacher.save()
                
                return new_teacher, HTTPStatus.CREATED

            else:
                response_object = {
                    'status':'fail',
                    'message':'You are not authorized to perform this operation.Admin only.'
                }
                return response_object
        

@teacher_namespace.route('/teachers/<int:teacher_id>')
class GetUpdateDeleteTeachers(Resource):
    @teacher_namespace.marshal_with(show_teacher)
    @teacher_namespace.doc(
        description='Retrieve Teacher Information by Student Registration Id',
        params = {
            'teacher_id': 'An ID for Teacher Registration'
        }
    )
    @jwt_required()
    def get(self,teacher_id):
        """
        Get Teacher by ID
        """
        teacher= Teacher.get_by_id(teacher_id)

        return teacher, HTTPStatus.OK
    
    @teacher_namespace.expect(teacher_model)
    @teacher_namespace.marshal_with(show_teacher)
    @teacher_namespace.doc(description='Update Teacher Information')
    @jwt_required()
    def put(self,teacher_id):
        """
        Update Teacher Information by ID(Admin)
        """
        teacher_update = Teacher.get_by_id(teacher_id)
        
        data = teacher_namespace.payload

        email = get_jwt_identity()
        users = User.query.all()
        for user in users :
            if user.email == email and user.designation.upper() == 'ADMIN':
                teacher_update.lastname = data['lastname'],
                teacher_update.firstname = data['firstname'],
                teacher_update.othername = data['othername'],
                teacher_update.email = data['email'],
                teacher_update.user_id = data['user_id'],
                
                teacher_update.update()
                return teacher_update,HTTPStatus.OK

            else:
                response_object = {
                    'status':'fail',
                    'message':'You are not authorized to perform this operation.Admin only.'
                }
                return response_object
            
        
    
    @teacher_namespace.doc(description='Delete Teacher')
    @jwt_required()
    def delete(self,student_id):
        """
        Delete  Teacher by ID(Admin)
        """
        teacher_delete = Teacher.get_by_id(student_id)

        email = get_jwt_identity()
        
        users = User.query.all()
        for user in users :
            if user.email == email and user.designation.upper() == 'ADMIN':
                teacher_delete.delete()

                return {"message":"Teacher Dashboard Delected Successfully"},HTTPStatus.OK


            else:
                response_object = {
                    'status':'fail',
                    'message':'You are not authorized to perform this operation.Admin only.'
                }
                return response_object

        
@teacher_namespace.route('/teachers/course/<int:teacher_id>')
class GetTeachersCourse(Resource):
    @teacher_namespace.marshal_with(teacher_course)
    @teacher_namespace.doc(
        description='Get Teacher Courses by teacher identification Number',
        params = {
            'teacher_id': 'Teacher identification Number'
        }

    )

    @jwt_required()
    def get(self,teacher_id):
        """
        Retrieve Teacher courses 
        """

        teacher_course = Teacher.get_by_id(teacher_id)


        return teacher_course, HTTPStatus.OK

@teacher_namespace.route('/teachers/staff_id')
class GetStaffId(Resource):
    @teacher_namespace.expect(staff_model)
    @teacher_namespace.marshal_with(show_staffId)
    @teacher_namespace.doc(description='Generate Staff identification number')
    @jwt_required()
    def post(self):
        """
        Generate Staff Identification Number(Admin)
        """

        email = get_jwt_identity()
        users = User.query.all()
        for user in users :
            if user.email == email and user.designation == 'ADMIN':
                data = teacher_namespace.payload
                new_staff = StaffID(
                teacher_id = data['teacher_id'],
                email = data['email'],
                staff_id = "ALT/2023/STAFF/" + str(data['teacher_id'])
            )
            
                new_staff.save()
                
                return new_staff, HTTPStatus.CREATED

            else:
                response_object = {
                    'status':'fail',
                    'message':'You are not authorized to perform this operation.Admin only.'
                }
                return response_object
        
@teacher_namespace.route('/teachers/staff_id/<int:user_id>')
class GetStaffIdNO(Resource):
    @teacher_namespace.marshal_with(show_staffId)
    @teacher_namespace.doc(
        description='Get your Staff Identification Number',
    )

    @jwt_required()
    def get(self,user_id):
        """
        Get Staff Identification Number(Teacher)
        """

        staff_ids = StaffID.query.all()

        for staff in staff_ids:
            if staff.user_id == user_id:

                return staff_ids, HTTPStatus.OK

@teacher_namespace.route('/teachers/user/<int:user_id>')
class GetTeacherByUserId(Resource):
    @teacher_namespace.marshal_with(show_teacher)
    @teacher_namespace.doc(
        description='Get Teacher Information by User ID',
        params = {
            'user_id': 'User Identification Number'
        }

    )

    @jwt_required()
    def get(self,user_id):
        """
        Retrieve Teacher by User ID
        """

        teachers = Teacher.query.all()

        for teacher in teachers:
            if teacher.user_id == user_id:

                return teachers, HTTPStatus.OK

