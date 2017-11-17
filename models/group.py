from google.appengine.ext import ndb


class Group(ndb.Model):
    groupname = ndb.StringProperty(required=True)
    members = ndb.KeyProperty(kind='User', repeated=True)
    invited_members = ndb.KeyProperty(kind='User', repeated=True)
    message_list = ndb.KeyProperty(kind='ChatMessage', repeated=True)
    avatar = ndb.BlobProperty()
    blurb = ndb.StringProperty()
