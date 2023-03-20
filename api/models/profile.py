from ..utils import db
from datetime import datetime


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer(), primary_key=True)
    othername = db.Column(db.String(100),nullable=True)
    firstname = db.Column(db.String(100),nullable=False)
    lastname = db.Column(db.String(100),nullable=False)
    bio = db.Column(db.Text(),nullable=False)
    gender = db.Column(db.String(20),nullable=False)
    created_at = db.Column(db.DateTime(),default=datetime.utcnow)
    profile_picture = db.relationship("ProfileImage", back_populates="profile")
    user_id = db.Column(db.Integer(),db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<Profile : {self.lastname} {self.firstname}>"

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
        
class ProfileImage(db.Model):
    __tablename__ = 'profileimages'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200))
    img = db.Column(db.String(70))
    minetype = db.Column(db.String(100))
    profile_id = db.Column(db.Integer(),db.ForeignKey('profiles.id'))
    profile = db.relationship("Profile", back_populates="profile_picture")

    def __repr__(self):
        return f"UserImage {self.name}"