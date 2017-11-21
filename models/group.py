from google.appengine.ext import ndb
from models.user import User
from responses.standard_error import StandardError

class Group(ndb.Model):
    groupname = ndb.StringProperty(required=True)
    members = ndb.KeyProperty(kind='User', repeated=True)
    invited_members = ndb.KeyProperty(kind='User', repeated=True)
    message_list = ndb.KeyProperty(kind='ChatMessage', repeated=True)
    avatar = ndb.BlobProperty()
    blurb = ndb.StringProperty()

    @classmethod
    def create_new_group(cls, data):
        if Group.query(Group.groupname == data['groupname']).count() > 0:
            raise StandardError("Group name already taken.")
    	invited_member_keys = []
        if 'invited_members' in data:
            for x in range(0, len(data['invited_members'])):
                key = ndb.Key(User, data['invited_members'][x])
                invited_member_keys.append(key)
    	members = []
    	members.append(ndb.Key(User, data['user_id']))
        group = Group(groupname = data['groupname'],
            members = members,
            invited_members = invited_member_keys)
        for field in ('avatar', 'blurb'):
            if field in data:
                setattr(group, field, data[field])
    	group.put()
    	return group
 
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
        'avatar': self.avatar}