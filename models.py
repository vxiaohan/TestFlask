from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature)
from sqlalchemy import Column, String, Integer

from TestFlask import app
from database import db_session, Base


class User(Base):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(100))
    user_email = Column(String(100))
    user_pass = Column(String(100))
    user_nic = Column(String(100))
    user_phone = Column(String(100))
    user_name = Column(String(100))

    def __init__(self, user_id=None, user_name=None, user_email=None, user_nic=None, user_phone=None, user_pass=None):
        self.user_id = user_id
        self.user_email = user_email
        self.user_name = user_name
        self.user_pass = user_pass
        self.user_nic = user_nic
        self.user_phone = user_phone

    def __repr__(self):
        return '<User %r>' % self.user_name

    def generate_auth_token(self, key, expiration=600):
        s = Serializer(key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token, key):
        s = Serializer(key)
        try:
            data = s.loads(token,return_header=True)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = db_session.query(User).filter(User.id == data[0]['id']).first()
        return user
