from google.appengine.ext import ndb
from pybcrypt import bcrypt


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
