# -*- coding: utf-8 -*-
import sha, json, time, uuid, operator



# placeholders
deposits = []
users = []

class User(object):

    @classmethod
    def user_dennis(cls):
        return User(name="Dennis Blommesteijn",
            email="dennis.blommesteijn@surfsara.nl", password="dennis123")

    @classmethod
    def user_emanuel(cls):
        return User(name="Emanuel Dima",
            email="emanuel.dima@uni-tuebingen.de", password="eman$123")

    @classmethod
    def user_carl(cls):
        return User(name="Carl Johan Håkansson",
            email="cjhak@kth.se", password="carl$123")

    @classmethod
    def user_lassi(cls):
        return User(name="Lassi Lehtinen",
            email="lassi.lehtinen@csc.fi", password="lassi$123")

    @classmethod
    def user_sarah(cls):
        return User(name="Sarah Berenji",
            email="sarahba@pdc.kth.se", password="sarah$123")

    def __init__(self, name, email, password):
        self._name = name
        self._email = email
        self._password = sha.new(email + ":" + password).hexdigest()
        self.new_token()

    def gen_token(self):
        time_ms = str(int(round(time.time() *1000)))
        return str(sha.new(self._email + ":" + time_ms).hexdigest())

    def new_token(self):
        self._token = self.gen_token()
        return self._token

    def to_dict(self):
        return {'user': {
            'name': self._name,
            'email': self._email,
            'token': self._token},
        'info':{}}

    def get_email(self):
        return self_email

    def to_json(self):
        return json.dumps(self.to_dict())

    def get_email(self):
        return self._email

    def get_token(self):
        return self._token

    @classmethod
    def find_user(cls, email=None, password=None, token=None):
        for u in users:
            if email and password:
                if u.verify_email_password(email=email, password=password):
                    return u
            elif token:
                if u.verify_token(token=token):
                    return u
        return None

    def verify_email_password(self, email, password):
        ep = sha.new(email + ":" + password).hexdigest()
        return (email == self._email and ep == self._password)

    def verify_token(self, token):
        # verify token and generate new one
        if self._token == token:
            self.new_token()
            return True
        # invalid token
        else:
            return False

    @classmethod
    def to_users_json(cls, us, user=None):
        return json.dumps({'users': [u.to_json() for u in us]})

class Deposit(object):

    def __init__(self, title, description):
        self._uuid = str(uuid.uuid4())
        self._title = title
        self._description = description
        self._created_at = time.time()

    def to_dict(self):
        return {'deposit': {
            'uuid': self._uuid,
            'title': self._title,
            'description': self._description,
            'authors': [],
            'domain': "",
            'created_at': str(int(self._created_at*1000)),
            'modified_at': str(int(time.time()*1000)),
            'pid': '',
            'files': [],
            'license': ''},
        'info':{
        }}

    def to_json(self, user=None):
        return json.dumps(self.to_dict())

    def get_created_at(self):
        return self._created_at

    def get_uuid(self):
        return self._uuid

    @classmethod
    def count(cls):
        return len(deposits)

    @classmethod
    def to_deposits_json(cls, ds, user=None):
        return json.dumps({'deposits': [d.to_dict() for d in ds],
            'info': {'count': Deposit.count()}})

    @classmethod
    def get_deposits(cls, page, size, order_by, order, user=None):
        start = (page - 1) * size
        end = start + size
        # sort
        reverse = order == 'asc'
        ds = sorted(deposits, key=lambda d: d.get_created_at(), reverse=reverse)
        return ds[start:end]

    @classmethod
    def find_deposit(cls, uuid, user=None):
        for d in deposits:
            if d.get_uuid() == uuid:
                return d
        return None

# user, deposit test values
users = [ User.user_dennis(), User.user_emanuel(), User.user_sarah(),
    User.user_lassi(), User.user_carl() ]
for i in range(1000):
    d = Deposit(title="Deposit "+str(i),
        description="Description of deposit " + str(i))
    deposits.append(d)
    time.sleep(.001)