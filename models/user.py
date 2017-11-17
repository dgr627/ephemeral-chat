import uuid
from google.appengine.ext import ndb
from standard_error import StandardError
from models.credential import Credential


class User(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    username = ndb.StringProperty()
    email = ndb.StringProperty
    blurb = ndb.StringProperty()
    avatar = ndb.BlobProperty()
    groups_member = ndb.KeyProperty(kind='Group', repeated=True)
    groups_invited = ndb.KeyProperty(kind='Group', repeated=True)
    credential = ndb.KeyProperty(kind='Credential')

    def authenticate_password(self, request):
        if not self.credential.get().verify_password(request):
            raise StandardError("Incorrect password.")
        return True

    def authenticate_token(self, request):
        if not self.credential.get().verify_token(request):
            raise StandardError("Not logged in")
        return True

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

    def to_auth_output(self):
        return {
            'user_id': self.user_id,
            'token': self.credential.get().token
        }