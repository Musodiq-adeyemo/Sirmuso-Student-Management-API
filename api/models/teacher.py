from ..utils import db
from datetime import datetime


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer(), primary_key=True)
    othername = db.Column(db.String(100),nullable=True)
    firstname = db.Column(db.String(100),nullable=False)
    lastname = db.Column(db.String(100),nullable=False)
    staff_id = db.relationship("StaffID", back_populates="teacher")
    email = db.Column(db.String(100),nullable=False,unique = True)
    user_id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="teacher")
    teacher_course = db.relationship("TeacherCourse", back_populates="lecturer")

    def __repr__(self):
        return f"<Teacher : {self.lastname} {self.firstname}>"
    
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

class StaffID(db.Model):
    __tablename__ = 'staff_id'
    id = db.Column(db.Integer(), primary_key=True)
    teacher_id =db.Column(db.Integer(),db.ForeignKey('teachers.id'))
    staff_id = db.Column(db.String(100),nullable=False,unique = True)
    email = db.Column(db.String(100),nullable=False,unique = True)
    user_id = db.Column(db.Integer())
    teacher = db.relationship("Teacher", back_populates="staff_id")
    def __repr__(self):
        return f"<StaffID : {self.teacher_id} {self.staff_id}>"

    
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