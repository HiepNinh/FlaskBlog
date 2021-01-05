from flask import current_app, url_for
from . import db
from extensions import login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except: 
            return None
        return User.query.get(user_id)
    
    def __repr__ (self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'username': self.username,
            'email': self.email,
            'image_file': self.password
        }
    

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__ (self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.content}', '{self.image_file}')"
    
    @property
    def serialized(self):
        """Return object data in serializeable format"""
        return {
            'title': self.title,
            'date_posted': str(self.date_posted),
            'content': self.content,
            'image_file': None if self.image_file is None else url_for('static', filename='post_pics/' + self.image_file),
            'author': self.author.username
        }
    
    
    
