from google.appengine.ext import ndb
from responses.standard_error import StandardError
import datetime
import uuid

class Message(ndb.Model):
    user_id = ndb.KeyProperty(kind='User', required = True)
    username = ndb.ComputedProperty(lambda self: self.user_id.get().username)
    groupname = ndb.KeyProperty(kind='Group', required = True)
    message_text = ndb.StringProperty()
    message_media = ndb.BlobProperty()
    message_time = ndb.DateTimeProperty()
    message_expiry = ndb.DateTimeProperty()

    @classmethod
    def create_message(cls, group_id, data):
    	message = Message(id =  str(uuid.uuid4()))
    	for field in ['message_text', 'message_media', 'message_expiry']:
    		if field in data:
    			setattr(message, field, data[field])
    	message.user_id = ndb.Key(User, data['user_id'])
    	group_key = ndb.Key('Group', group_id)
        message.groupname = group_key
        group = group_key.get()
    	message.message_time = datetime.datetime.now()
    	message.put()
    	group.message_list.append(message.key)
    	group.put()
    	return message

    @classmethod
    def return_by_msg_id(cls, msg_id):
    	message = ndb.Key(Message, msg_id).get()
    	return message

    def delete_message(self):
        group = self.groupname.get()
        group.remove_message(self.key.id())
        group.put()
        self.key.delete()
        return True

    def message_output(self):
    	return{'user_id' : self.user_id.id(),
    	'username' : self.username,
    	'group_id' : self.groupname.id(),
    	'message_text' : self.message_text,
    	'message_media' : self.message_media,
    	'message_time' : self.message_time,
    	'message_expiry' : self.message_expiry,
    	'msg_id' : self.key.id()}


# Avoid circular import

from models.user import User
from models.group import Group