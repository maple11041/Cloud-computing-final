from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db
import app
key = 'secret'


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.Text(), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.secret_key, expires_sec)
        return s.dumps({'user_id': str(self.id)}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.secret_key)
        try:
            user_id = s.loads(token)['user_id']
        except Exception as e:
            print(e)
            return None
        return User.query.get(user_id)


def create_user(request):
    '''
    Create user in the database
    Password is encrypted with SHA256
    '''
    if ('username' in request and
        'password' in request and 'email' in request) and \
       (type(request['username'] == str) and type(request['password'] == str)
           and type(request['email'] == str)):
        duplicate = db.session.query(User).filter(
            User.email == request['email']).first()
        if duplicate is None:
            myctx = CryptContext(schemes=["sha256_crypt"])
            new_user = User(
                username=request['username'],
                email=request['email'],
                password=myctx.hash(request['password'])
            )
            db.session.add(new_user)
            db.session.commit()
            return True
        else:
            print('register failed')
            return False
    else:
        return False


def generate_token(email):
    '''
    Generate token with User ID
    the valid period of the token is 10 mins
    '''
    user = db.session.query(User).filter(User.email == email).first()
    if user is not None:
        payload = {
            'sub': str(user.id),
            'exp': datetime.utcnow() + timedelta(minutes=10),
            'nbf': datetime.utcnow(),
            'iat': datetime.utcnow(),
        }
        token = jwt.encode(payload, key, algorithm='HS256')
        return token
    else:
        return None


def create_token(username):
    '''
    Probably not needed, since we don't store token
    in the database
    '''
    user = db.session.query(User).filter(User.username == username).first()
    if user is not None:
        token = generate_token(user.id)
        user.token = token
        db.session.commit()
        return token
    else:
        return None


def login(request):
    '''
    Verify the password in the request

    Parameters:
        request: request to login
    returns:
        True if password checks out, False vice versa
    '''
    if ('email' in request and 'password' in request) and \
       (type(request['email'] == str) and type(request['password'] == str)):
        print(request)
        myctx = CryptContext(schemes=["sha256_crypt"])
        user = db.session.query(User).filter(
            User.email == request['email']).first()
        if user is None:
            return False
        else:
            return myctx.verify(request['password'], user.password)
    else:
        return False


def get_user(id):
    return db.session.query(User).filter(User.id == id).first()


def row2dict(row):
    dataset = [r.__dict__ for r in row]
    for row in dataset:
        if '_sa_instance_state' in row:
            del row['_sa_instance_state']
        else:
            break
    return dataset


db.drop_all()
db.create_all()
