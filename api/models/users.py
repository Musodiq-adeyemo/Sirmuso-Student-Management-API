from ..utils import db
from enum import Enum
from datetime import datetime


class Roles(Enum):
    STUDENT = 'student'
    STAFF = 'staff'
    ADMIN = 'admin'
    


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(200), unique=True,nullable=False)
    username = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(100),nullable=False)
    designation =db.Column(db.Enum(Roles),default=Roles.STUDENT)
    profile = db.relationship("Profile", back_populates="user")
    student = db.relationship("Student", back_populates="user")
    teacher = db.relationship("Teacher", back_populates="user")
    
    def __repr__(self):
        return f"<User : {self.username}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)