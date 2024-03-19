from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from datetime import datetime, timezone


# Assoziative Tabelle für die Many-to-Many-Beziehung zwischen User-Instanzen
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True)
    email = db.Column(db.String(255), index=True, unique=True)
    password_hash = db.Column(db.String(255))
    about_me = db.Column(db.String(140), default="", nullable=True)  # Optional mit Standardwert ""
    last_seen = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    ratings = db.relationship('Rating', back_populates='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'
    

    # Definition der 'followed' und 'followers' Beziehungen unter Verwendung von 'secondary'
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )
        
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None

    
    def followers_count(self):
        return self.followers.count()

    def following_count(self):
        return self.followed.count()

    def following_posts(self, page, per_page=20):
        followed_posts = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)
        ).filter(followers.c.follower_id == self.id)
        own_posts = Post.query.filter_by(user_id=self.id)
        return followed_posts.union(own_posts).order_by(Post.timestamp.desc()).paginate(page=page, per_page=per_page, error_out=False)

    
          
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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Achten Sie auf den korrekten Fremdschlüssel
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=lambda: datetime.now(timezone.utc))
    ratings = db.relationship('Rating', back_populates='post', lazy='dynamic')
    
        # Repräsentationsmethode
    def average_rating(self):
        ratings = self.ratings.with_entities(db.func.avg(Rating.rating).label('average')).first()
        return round(ratings.average, 2) if ratings.average else None

    def __repr__(self):
        return f'<Post {self.id}>'

    # Beziehung
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))  # Achten Sie auf den korrekten Fremdschlüssel
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Achten Sie auf den korrekten Fremdschlüssel
    content = db.Column(db.Text)

    # Repräsentationsmethode
    def __repr__(self):
        return f'<Comment {self.id}>'
    

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Bewertung zwischen 1 und 10

    post = db.relationship('Post', back_populates='ratings')
    user = db.relationship('User', back_populates='ratings')

    def __repr__(self):
        return f'<Rating {self.rating}>'
