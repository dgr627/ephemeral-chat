import uuid
from google.appengine.ext import ndb
from responses.standard_error import StandardError
from models.credential import Credential

class User(ndb.Model):
    user_id = ndb.StringProperty(required = True)
    username = ndb.StringProperty(required = True)
    email = ndb.StringProperty()
    blurb = ndb.StringProperty()
    avatar = ndb.BlobProperty()
    groups_member = ndb.KeyProperty(kind = 'Group', repeated = True)
    groups_invited = ndb.KeyProperty(kind = 'Group', repeated = True)
    credential = ndb.LocalStructuredProperty(Credential, repeated = False)

    @classmethod
    def return_by_user_id(cls, user_id):
        return ndb.Key(User, user_id).get()

    @classmethod
    def return_by_username(cls, username):
        return User.query(User.username == username).get()

    @classmethod
    def authenticate_password(cls, username, password):
        user = User.return_by_username(username)
        if not user.credential.verify_password(password):
            raise StandardError("Incorrect password.")
        return user

    @classmethod
    def authenticate_token(cls, user_id, token):
        user = User.return_by_user_id(user_id)
        if not user.credential.verify_token(token):
            raise StandardError("Not logged in")
        return user

    @classmethod
    def valid_password(cls, password):
        if len(password) < 6:
            raise StandardError("Invalid password")
        return password

    @classmethod
    def create_new_user(cls, username, password):
        if User.query(User.username == username).count() > 0:
            raise StandardError("Username already taken.")
        user_id = str(uuid.uuid4())
        password = User.valid_password(password)
        credential = Credential()
        credential.hash_password(password)
        user = User(user_id=user_id,
            username=username,
            id=user_id, 
            credential=credential)
        user.put()
        return user

    def update_profile(self, data):
        for field in ['username', 'email', 'blurb', 'avatar']:
            if field in data:
                setattr(self, field, data[field])
        self.put()
        return self

    def add_group(self, group_key):
        self.groups_member.append(group_key)
        self.put()
        return self

    def check_ismember(self, group_id):
        count = 0
        while count < len(self.groups_member):
            if group_id == self.groups_member[count].id():
                return self
            count+=1
        raise StandardError("User isn't a member of group.")

    def login_output(self):
        return {
            'user_id': self.user_id,
            'token': self.credential.token
        }

    def public_output(self):
        groups_member_names = []
        for x in range(0, len(self.groups_member)):
            groups_member_names.append(self.groups_member[x].get().groupname)
        invited_groups_names = []
        for y in range(0, len(self.groups_invited)):
            invited_groups_names.append(self.groups_invited[y].get().groupname)
        return {
            'username': self.username,
            'blurb': self.blurb,
            'avatar': self.avatar,
            'groups_member' : groups_member_names,
            'groups_invited' : invited_groups_names
        }

    def owner_output(self):
        groups_member_names = []
        for x in range(0, len(self.groups_member)):
            groups_member_names.append(self.groups_member[x].id())
        invited_groups_names = []
        for y in range(0, len(self.groups_invited)):
            invited_groups_names.append(self.groups_invited[y].id())
        return {
            'username': self.username,
            'blurb': self.blurb,
            'avatar': self.avatar,
            'email': self.email,
            'groups_member' : groups_member_names,
            'groups_invited' : invited_groups_names
        }

# Avoiding circular import

from models.group import Group
