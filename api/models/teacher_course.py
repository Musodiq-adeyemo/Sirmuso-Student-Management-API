from ..utils import db


class TeacherCourse(db.Model):
    __tablename__ = 'teacher_courses'
    id = db.Column(db.Integer(), primary_key=True)
    teacher_id = db.Column(db.Integer(),db.ForeignKey('teachers.id'))
    staff_id = db.Column(db.String(100),nullable=False,unique = True)
    course_title =db.Column(db.String(100))
    course_code = db.Column(db.String(100),nullable=False)
    course_unit = db.Column(db.Integer())
    grade = db.relationship("Grade", back_populates="course")
    student_course = db.relationship("StudentCourse", back_populates="courses")
    lecturer = db.relationship("Teacher", back_populates="teacher_course")

    def __repr__(self):
        return f"<TeacherCourse : {self.course_title} {self.course_code}>"

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