from ..utils import db

class StudentCourse(db.Model):
    __tablename__ = 'student_courses'
    id = db.Column(db.Integer(), primary_key=True)
    course_id =db.Column(db.Integer(),db.ForeignKey('teacher_courses.id'))
    student_id =db.Column(db.Integer(),db.ForeignKey('students.id'))
    email = db.Column(db.String(100),nullable=False)
    matric_no = db.Column(db.String(100),nullable=False)
    level = db.Column(db.Integer())
    courses = db.relationship("TeacherCourse", back_populates="student_course")
    students = db.relationship("Student", back_populates="student_course")

    def __repr__(self):
        return f"<StudentCourse : {self.course_id}"

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