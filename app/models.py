from app import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

'''
Allow login manager to access user id
'''
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

'''
User data model
'''
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    first_name = db.Column(db.String(60), nullable=True)
    last_name = db.Column(db.String(60), nullable=True)
    state = db.Column(db.String(60), nullable=True)
    city = db.Column(db.String(60), nullable=True)
    address = db.Column(db.String(60), nullable=True)
    zip_code = db.Column(db.String(5), nullable=True)

    '''
    generate a reset token that expires after 30 minutes
    '''
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    '''
    verify a reset token
    '''
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

'''
Food data model
'''
class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    cost = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(300), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    department = db.Column(db.String(30), nullable=True)
    image_file = db.Column(db.String(20), nullable=True, default="default.jpg")

    def __repr__(self):
        return f"Food('{self.name}', '{self.cost}', '{self.image_file}')"
