from flask_restx import fields,Api


root_api = Api()


display_student = root_api.model(
    'Student', {
       'id':fields.Integer(description='Student ID'),
       'lastname':fields.String(description='Student Surname',required = True),
       'firstname': fields.String(description='Student firstname',required = True),  
    }
)

display_course = root_api.model(
    'Course', {
       'id':fields.Integer(description='Course ID'),
       'course_title':fields.String(description='Course Title',required = True),
       'course_code':fields.String(description='Course Code',required = True),
       'course_unit':fields.Integer(description='Course Unit',required = True),
    }
)

display_teacher = root_api.model(
    'Teacher', {
       'id':fields.Integer(description='Teacher ID'),
       'lastname':fields.String(description='Teacher Surname',required = True),
       'firstname': fields.String(description='Teacher firstname',required = True),  
       
    }
)


