import uuid
from google.appengine.ext import ndb
from standard_error import StandardError
from models.credential import Credential


class User(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    username = ndb.StringProperty()
    email = ndb.StringProperty()
    blurb = ndb.StringProperty()
    avatar = ndb.BlobProperty()
    groups_member = ndb.KeyProperty(kind='Group', repeated=True)
    groups_invited = ndb.KeyProperty(kind='Group', repeated=True)
    credential = ndb.KeyProperty(kind='Credential')

    @classmethod
    def return_by_user_id(cls, user_id):
        return ndb.Key(User, user_id).get()

    @classmethod
    def return_by_username(cls, username):
        return User.query(User.username == username).get()

    @classmethod
    def authenticate_password(cls, username, password):
        user = User.return_by_username(username)
        if not user.credential.get().verify_password(password):
            raise StandardError("Incorrect password.")
        return user

    @classmethod
    def authenticate_token(cls, user_id, token):
        user = User.return_by_user_id(user_id)
        if not user.credential.get().verify_token(token):
            raise StandardError("Not logged in")
        return user

    @classmethod
    def create_new_user(cls, username, password):
        if User.query(User.username == username).count() > 0:
            raise StandardError("Username already taken.")
        user_id = str(uuid.uuid4())
        credential = Credential()
        credential.hash_password(password)
        credential.put()
        user = User(user_id=user_id, username=username, id=user_id, credential=credential.key)
        user.put()
        return user

    def update_profile(self, data):
        for field in ['username', 'email', 'blurb', 'avatar']:
            if field in data:
                setattr(self, field, data[field])
        self.put()
        return self


    def login_output(self):
        return {
            'user_id': self.user_id,
            'token': self.credential.get().token
        }

    def public_output(self):
        return {
            'username': self.username,
            'blurb': self.blurb,
            'avatar': self.avatar
        }

    def owner_output(self):
        return {
            'username': self.username,
            'blurb': self.blurb,
            'avatar': self.avatar,
            'email': self.email
        }
