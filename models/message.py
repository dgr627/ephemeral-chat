from google.appengine.ext import ndb
from models.user import User
from models.group import Group
from responses.standard_error import StandardError
import datetime

class Message(ndb.Model):
    user_id = ndb.KeyProperty(kind='User', required = True)
    username = ndb.ComputedProperty(lambda self: self.user_id.get().username)
    groupname = ndb.KeyProperty(kind='Group', required = True)
    message_text = ndb.StringProperty()
    message_media = ndb.BlobProperty()
    message_time = ndb.DateTimeProperty()
    message_expiry = ndb.DateTimeProperty()

    @classmethod
    def create_message(cls, groupname, data):
    	message = Message()
    	for field in ['message_text', 'message_media', 'message_expiry']:
    		if field in data:
    			setattr(message, field, data[field])
    	message.user_id = ndb.Key(User, data['user_id'])
    	message.groupname = ndb.Key(Group, groupname)
    	group = message.groupname.get()
    	message.message_time = datetime.datetime.now()
    	message.put()
    	group.message_list.append(message.key)
    	group.put()
    	return message

    @classmethod
    def return_by_msg_id(cls, msg_id):
    	message = ndb.Key(Message, msg_id).get()
    	return message

    def message_output(self):
    	return{'user_id' : self.user_id.id(),
    	'username' : self.username,
    	'groupname' : self.groupname.id(),
    	'message_text' : self.message_text,
    	'message_media' : self.message_media,
    	'message_time' : self.message_time,
    	'message_expiry' : self.message_expiry,
    	'msg_id' : self.key.id()}