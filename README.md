
## B2SHARE server

B2share dummy server in Python with Flask.

### Development

**Prerequisites**

* Python 2.7
* Pip
* Virtualenv

**Install**

```bash
virtualenv .dev
. .dev/bin/activate
python setup.py develop
```

**Run**

```bash
python scripts/b2share-serve
```

**Apache ProxyBypass**

```
<VirtualHost *:80>
  ProxyRequests off
  <Proxy *>
    Order deny,allow
    Allow from all
  </Proxy>
  <Location /backend/>
    ProxyPass http://x.x.x.x:5000/
    ProxyPassReverse http://x.x.x.x:5000/
  </Location>
</VirtualHost>
```

