import sha, json, time

class User(object):

    @classmethod
    def user_dennis(cls):
        return User(name="Dennis Blommesteijn",
            email="dennis.blommesteijn@surfsara.nl", password="dennis123")

    @classmethod
    def user_walter(cls):
        return User(name="Walter de Jong",
            email="walter.dejong@surfsara.nl", password="walter123")

    def __init__(self, name, email, password):
        self._name = name
        self._email = email
        self._password = sha.new(email + ":" + password).hexdigest()

    def to_json(self):
        time_ms = str(int(round(time.time() *1000)))
        return json.dumps({'user': {
            'name': self._name,
            'email': self._email,
            'token': str(sha.new(self._email + ":" + time_ms).hexdigest())
        }})

    def get_email(self):
        return self._email

    @classmethod
    def find_user(cls, email, password):
        us = Users.users().get_users()
        for u in us:
            if u.equals(email=email, password=password):
                return u
        return None

    def equals(self, email, password):
        ep = sha.new(email + ":" + password).hexdigest()
        return (email == self._email and ep == self._password)

class Users(object):

    @classmethod
    def users(cls):
        return Users([ User.user_dennis(), User.user_walter() ])

    def __init__(self, users):
        self._users = users

    def get_users(self):
        return self._users

    def to_json(self):
        users = [ x.to_json() for x in self.get_users()]
        return json.dumps({'users': users})

