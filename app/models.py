from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True)
    email = db.Column(db.String(255), index=True, unique=True)
    password_hash = db.Column(db.String(255))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Repräsentationsmethode
def __repr__(self):
    return f'<User {self.username}>'

# Beziehungen
posts = db.relationship('Post', backref='author', lazy='dynamic')
comments = db.relationship('Comment', backref='commenter', lazy='dynamic')

class Post(db.Model):
    postid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))  # Achten Sie auf den korrekten Fremdschlüssel
    content = db.Column(db.Text)

    # Repräsentationsmethode
    def __repr__(self):
        return f'<Post {self.postid}>'

    # Beziehung
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

class Comment(db.Model):
    commentid = db.Column(db.Integer, primary_key=True)
    postid = db.Column(db.Integer, db.ForeignKey('post.postid'))  # Achten Sie auf den korrekten Fremdschlüssel
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))  # Achten Sie auf den korrekten Fremdschlüssel
    content = db.Column(db.Text)

    # Repräsentationsmethode
    def __repr__(self):
        return f'<Comment {self.commentid}>'




