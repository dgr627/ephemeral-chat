from google.appengine.ext import ndb


class ChatMessage(ndb.Model):
    user_id = ndb.KeyProperty(kind='User', required=True)
    username = ndb.StringProperty()
    groupname = ndb.KeyProperty(kind='Group', repeated=True)
    message_text = ndb.StringProperty()
    message_media = ndb.BlobProperty()
    message_time = ndb.DateTimeProperty()
    message_expiry = ndb.DateTimeProperty()
