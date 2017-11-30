from google.appengine.ext import ndb
from models.user import User
from responses.standard_error import StandardError
import uuid

class Group(ndb.Model):
    groupname = ndb.StringProperty(required=True)
    members = ndb.KeyProperty(kind='User', repeated=True)
    invited_members = ndb.KeyProperty(kind='User', repeated=True)
    message_list = ndb.KeyProperty(kind='Message', repeated=True)
    avatar = ndb.BlobProperty()
    blurb = ndb.StringProperty()

    @classmethod
    def create_new_group(cls, data):
    	invited_member_keys = []
        if 'invited_members' in data:
            for x in range(0, len(data['invited_members'])):
                key = ndb.Key(User, data['invited_members'][x])
                invited_member_keys.append(key)
    	members = []
    	members.append(ndb.Key(User, data['user_id']))
        group = Group(groupname = data['groupname'],
            members = members,
            invited_members = invited_member_keys, id = str(uuid.uuid4()))
        for field in ('avatar', 'blurb'):
            if field in data:
                setattr(group, field, data[field])
    	group.put()
        creator = User.return_by_user_id(data['user_id'])
        creator.add_group(group.key)
    	return group

    @classmethod
    def return_by_group_id(cls, group_id):
        return ndb.Key(Group, group_id).get()

    def check_ismember(self, user_id):
        count = 0
        while count < len(self.members):
            if user_id == self.members[count].id():
                return self
            count+=1
        raise StandardError("User isn't a member of group.")

    def remove_message(self, msg_id):
        count = 0
        while count < len(self.message_list):
            if msg_id == self.message_list[count].id():
                self.message_list.pop(count)
                return self
            count+=1
        raise StandardError("Message not found")

    def update_group_info(self, data):
        for field in ('avatar', 'blurb'):
            if field in data:
                setattr(self, field, data[field])
        self.put()
        print self
        return self
 
    def info_output(self):
        member_usernames = []
        invited_member_usernames = []
        for x in range(0, len(self.members)):
            member_usernames.append(self.members[x].get().username)
        for y in range(0, len(self.invited_members)):
            invited_member_usernames.append(self.invited_members[y].get().username)
        output_data = {}
        return {'groupname': self.groupname,
        'members': member_usernames,
        'invited_members': invited_member_usernames,
        'blurb': self.blurb,
        'avatar': self.avatar,
        'id' : self.key.id()}

    def message_list_output(self):
        message_ids = []
        for x in range(0, len(self.message_list)):
            msg_id = self.message_list[x].id()
            message_ids.append(msg_id)
        return {'message_ids' : message_ids}
