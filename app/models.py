from app import db 

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True)
    email = db.Column(db.String(255), index=True, unique=True)
    password_hash = db.Column(db.String(255))

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




