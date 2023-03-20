from flask_restx import Namespace,Resource,fields,Api
from flask import request
from ..utils import db
from ..models.users import User
from werkzeug.security import generate_password_hash,check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token,create_refresh_token
from flask_jwt_extended import jwt_required,get_jwt_identity,unset_jwt_cookies

auth_namespace = Namespace("Auth",description="Namespace for authentication")
root_api = Api()
signup_model= auth_namespace.model(
    "signup", {
        'username':fields.String(required=True,description='A username'),
        'email':fields.String(required=True,description='An email'),
        'password':fields.String(required=True,description='A password'),
        'designation': fields.String(description='User Role',required = True,enum=['STUDENT','STAFF','ADMIN']),
    }
)

login_model= auth_namespace.model(
    "Login", {
        'email':fields.String(required=True,description='An email'),
        'password':fields.String(required=True,description='A password')
    }
)

show_user = auth_namespace.model(
    "User", {
        'id':fields.Integer(),
        'username':fields.String(required=True,description='A username'),
        'email':fields.String(required=True,description='An email'),
        'designation': fields.String(description='User Role',required = True),
    }
)

user_model= auth_namespace.model(
    "User", {
        'id':fields.Integer(),
        'username':fields.String(required=True,description='A username'),
        'email':fields.String(required=True,description='An email')
    }
)

@auth_namespace.route('/signup')
class SignUp(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)

    def post(self):
        """
        Users Registration
        """
        data = request.get_json()
        """
        username=data.get('username'),
        email = data.get('email'),
        password = (data.get('password'))

        email_exist = User.query.filter_by(email=email).first()
        username_exist = User.query.filter_by(username=username).first()

        if email_exist :
            response_object = {
                'status':'fail',
                'message':'Email Already exist please log in or use another email.'
            }
            return response_object
        elif username_exist :
            response_object = {
                'status':'fail',
                'message':'Username Already exist please log in or use another username.'
            }
            return response_object
        elif len(password) < 8 :
            response_object = {
                'status':'fail',
                'message':'Password too short, Please use longer password.'
            }
            return response_object
        else:
        """
        new_user = User(
            username=data.get('username'),
            email = data.get('email'),
            password = generate_password_hash(data.get('password')),
            designation = data.get('designation')
        )
        new_user.save()
        return new_user, HTTPStatus.CREATED
   
    @auth_namespace.marshal_with(show_user)
    @jwt_required()
    def get(self):
        """
        Get All Users
        """
        users = User.query.all()

        return users, HTTPStatus.OK

@auth_namespace.route('/signup/<int:user_id>')
class GetUpdateDeleteUser(Resource):
    @auth_namespace.marshal_with(show_user)
    @auth_namespace.doc(
        description='Retrieve User Information by User Id',
        params = {
            'user_id': 'An ID for User Registration'
        }
    )
    @jwt_required()
    def get(self,user_id):
        """
        Get User by ID
        """
        user = User.get_by_id(user_id)

        return user, HTTPStatus.OK
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    @auth_namespace.doc(description='Update User By ID')
    @jwt_required()
    def put(self,user_id):
        """
        Update User Information by ID
        """
        user_update = User.get_by_id(user_id)
        
        data = auth_namespace.payload
        
        user_update.username=data.get('username'),
        user_update.email = data.get('email'),
        user_update.designation = data.get('designation')
        
        user_update.update()
        return user_update,HTTPStatus.OK
    
    @auth_namespace.doc(description='Delete User')
    @jwt_required()
    def delete(self,user_id):
        """
        Delete User by ID
        """
        user_delete = User.get_by_id(user_id)

        user_delete.delete()

        return {"message":"User Dashboard Delected Successfully"},HTTPStatus.OK



@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
        Login Authentication 
        """
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if (user is not None) and check_password_hash(user.password,password):
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)

            response = {
                "access_token":access_token,
                "refresh_token":refresh_token,
            }

            return response, HTTPStatus.CREATED

@auth_namespace.route('/refresh')
class Login_refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
        Generate Refresh Token 
        """
        username = get_jwt_identity()
        
        access_token = create_access_token(identity=username)

        return { "access_token":access_token}, HTTPStatus.OK

@auth_namespace.route('/logout')
class Logout(Resource):
    @jwt_required()
    def post(self):
        """
        Log the User Out 
        """
        unset_jwt_cookies
        db.session.commit()

        return {"message":"Successfully Logged Out"}, HTTPStatus.OK
    

