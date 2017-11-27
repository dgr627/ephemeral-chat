from google.appengine.ext import ndb
from models.user import User
from responses.standard_error import StandardError

class Group(ndb.Model):
    groupname = ndb.StringProperty(required=True)
    members = ndb.KeyProperty(kind='User', repeated=True)
    invited_members = ndb.KeyProperty(kind='User', repeated=True)
    message_list = ndb.KeyProperty(kind='Message', repeated=True)
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
            invited_members = invited_member_keys, id = data['groupname'])
        for field in ('avatar', 'blurb'):
            if field in data:
                setattr(group, field, data[field])
    	group.put()
    	return group

    @classmethod
    def return_by_groupname(cls, groupname):
        return ndb.Key(Group, groupname).get()

    @classmethod
    def check_ismember(cls, groupname, user_id):
        group = Group.return_by_groupname(groupname)
        

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
        'avatar': self.avatar}

    def message_list_output(self):
        message_ids = []
        for x in range(0, len(self.message_list)):
            msg_id = self.message_list[x].id()
            message_ids.append(msg_id)
        return {'message_ids' : message_ids}
