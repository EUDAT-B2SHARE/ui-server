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
        for u in users:
            if u.equals(email=email, password=password):
                return u
        return None

    def equals(self, email, password):
        ep = sha.new(email + ":" + password).hexdigest()
        return (email == self._email and ep == self._password)

    @classmethod
    def to_users_json(cls, us):
        return json.dumps({'users': [u.to_json() for u in us]})

class Deposit(object):

    def __init__(self, title, description):
        self._uuid = str(uuid.uuid4())
        self._title = title
        self._description = description
        self._created_at = str(time.time())

    def to_json(self):
        return json.dumps({'deposit': {
            'uuid': self._uuid,
            'title': self._title,
            'description': self._description,
            'authors': [],
            'domain': "",
            'created_at': self._created_at,
            'modified_at': str(time.time()),
            'pid': '',
            'files': [],
            'license': ''
        }})
    def get_created_at(self):
        return self._created_at

    @classmethod
    def to_deposits_json(cls, ds):
        return json.dumps({'deposits': [d.to_json() for d in ds]})

    @classmethod
    def get_deposits(cls, page, size, order_by, order):
        start = (page - 1) * size
        end = start + size
        # sort
        reverse = order == 'asc'
        ds = sorted(deposits, key=lambda d: d.get_created_at(), reverse=reverse)

        return ds[start:end]

# user, deposit test values
users = [ User.user_dennis(), User.user_walter() ]
for i in range(1000):
    d = Deposit(title="Deposit "+str(i),
        description="Description of deposit " + str(i))
    deposits.append(d)
    time.sleep(.001)