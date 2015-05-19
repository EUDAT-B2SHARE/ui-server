
## B2SHARE server

B2share dummy server in Python with Flask.

### Development

Eighter run through Apache (ProxyPass) or as standalone.

NOTE: `Access-Control-Allow-Origin` must be set if alternate ports/ hosts are used!

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

**Apache ProxyPass**

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

