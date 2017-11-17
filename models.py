
import endpoints
import uuid
from google.appengine.ext import ndb
from pybcrypt import bcrypt
from standard_error import StandardError

class User(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    username = ndb.StringProperty()
    email = ndb.StringProperty
    blurb = ndb.StringProperty()
    avatar = ndb.BlobProperty()
    groups_member = ndb.KeyProperty(kind = 'Group', repeated = True)
    groups_invited = ndb.KeyProperty(kind = 'Group', repeated = True)
    credential = ndb.KeyProperty(kind = 'Credential')

    def authenticate_password(self, request):
        if not self.credential.get().verify_password(request):
            raise endpoints.UnauthorizedException("Incorrect password.")
        return True

    def authenticate_token(self, request):
        if not self.credential.get().verify_token(request):
            raise endpoints.UnauthorizedException("Not logged in")
        return True

    @classmethod
    def create_new_user(cls, request):
        if User.query(User.username == request['username']).count() > 0:
            raise StandardError("Username already taken.")
        user_id = str(uuid.uuid4())
        user = User(user_id = user_id, username = request['username'], id = user_id)
        credential = Credential()
        credential.hash_password(request['password'])
        credential.put()
        user.credential = credential.key
        user.put()
        return {"user_id":user.user_id, "token": credential.token}


class Credential(ndb.Model):
    hashed_password = ndb.StringProperty(indexed=False)
    salt = ndb.StringProperty(indexed=False)
    token = ndb.StringProperty(indexed=False)

    def hash_password(self, inputstr):
        s = bcrypt.gensalt()
        h = bcrypt.hashpw(inputstr, s)
        self.hashed_password = h
        self.salt = s
        self.token = bcrypt.gensalt()
    

    def verify_password(self, inputstr):
        if not bcrypt.hashpw(inputstr, self.salt) == self.hashed_password:
            return False
        else:
            return True

    def verify_token(self, inputstr):
        if not inputstr == self.token:
            return False
        else:
            return True

class ChatMessage(ndb.Model):
    user_id = ndb.KeyProperty(kind ='User', required = True)
    username = ndb.StringProperty()
    groupname = ndb.KeyProperty(kind = 'Group', repeated = True)
    message_text = ndb.StringProperty()
    message_media = ndb.BlobProperty()
    message_time = ndb.DateTimeProperty()
    message_expiry = ndb.DateTimeProperty()

class Group(ndb.Model):
    groupname = ndb.StringProperty(required = True)
    members = ndb.KeyProperty(kind = 'User', repeated=True)
    invited_members = ndb.KeyProperty(kind = 'User', repeated = True)
    message_list = ndb.KeyProperty(kind = 'ChatMessage', repeated = True)
    avatar = ndb.BlobProperty()
    blurb = ndb.StringProperty()
    
