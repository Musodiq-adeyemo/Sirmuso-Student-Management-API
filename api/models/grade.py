from ..utils import db


class Grade(db.Model):
    __tablename__ = 'grades'
    id = db.Column(db.Integer(), primary_key=True)
    matric_no = db.Column(db.String(100))
    email = db.Column(db.String(100))
    course_id =db.Column(db.Integer(),db.ForeignKey('teacher_courses.id'))
    student_id =db.Column(db.Integer(),db.ForeignKey('students.id'))
    level = db.Column(db.Integer())
    score = db.Column(db.Integer())
    course_unit = db.Column(db.Integer())
    grade = db.Column(db.String(100),nullable=False)
    grade_point = db.Column(db.Integer())
    students = db.relationship("Student", back_populates="student_grade")
    course =db.relationship("TeacherCourse", back_populates="grade")

    def __repr__(self):
        return f"<Grade : {self.course_id} {self.matric_no}>"

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