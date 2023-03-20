from ..utils import db
from datetime import datetime


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer(), primary_key=True)
    othername = db.Column(db.String(100),nullable=True)
    firstname = db.Column(db.String(100),nullable=False)
    lastname = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique = True)
    user_id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    matric_no = db.relationship("StudentMatricNo", back_populates="student")
    user = db.relationship("User", back_populates="student")
    student_course = db.relationship("StudentCourse", back_populates="students")
    student_grade = db.relationship("Grade", back_populates="students")

    def __repr__(self):
        return f"<Student : {self.lastname} {self.firstname}>"
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

class StudentMatricNo(db.Model):
    __tablename__ = 'students_matric'
    id = db.Column(db.Integer(), primary_key=True)
    student_id =db.Column(db.Integer(),db.ForeignKey('students.id'))
    matric_no = db.Column(db.String(100),nullable=False,unique = True)
    email = db.Column(db.String(100),nullable=False,unique = True)
    user_id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    student = db.relationship("Student", back_populates="matric_no")
    user_id = db.Column(db.Integer())
    def __repr__(self):
        return f"<Student : {self.student_id} {self.matric_no}>"

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