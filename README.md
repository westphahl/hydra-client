DEPRECATED
==========

**This library is no longer maintained. Please use the official [ORY Hydra package](https://github.com/ory/sdk/tree/master/clients/hydra/python).**

[![No Maintenance Intended](http://unmaintained.tech/badge.svg)](http://unmaintained.tech/)
[![Build Status](https://travis-ci.org/westphahl/hydra-client.svg?branch=master)](https://travis-ci.org/westphahl/hydra-client)

Python wrapper for the [ORY Hydra](https://www.ory.sh/docs/hydra/) OAuth2 and
OpenID Connect server REST API.

**Disclaimer: This library is still in alpha state!**

Installation
------------

```
pip install hydra-client
```

Basic usage
-----------

```python
from hydra_client import HydraAdmin

hydra = HydraAdmin("http://localhost:4445")
login_request = hydra.login_request("challenge")
redirect_to = login_request.accept(subject="username")
```

See also the example [login/consent provider](
https://github.com/westphahl/hydra-login-consent-python).

Development
-----------

All code is formatted using [black](https://github.com/ambv/black). Tests and
static checks can be run with tox:

    tox

### Recording test data

The hydra-client uses [Betamax](https://betamax.readthedocs.org/) for mocking
and recording HTTP interactions.

Run Hydra in a Docker container:

```
   docker run \
      -it \
      --rm \
      -e "DSN=memory" \
      -e "URLS_SELF_ISSUER=http://localhost:4444/" \
      --name hydra \
      -p 4445:4445 \
      -p 4444:4444 \
      oryd/hydra:v1.0 \
      serve all --dangerous-force-http
```


Create a new OAuth2 client:

```
   docker exec \
      -it hydra \
       hydra clients create \
       --endpoint http://localhost:4445 \
       --id test-client \
       --secret test-secret \
       --callbacks http://client.localhost
```

Re-Record Betamax cassettes:

```
   BETAMAX_RECORD_MODE=all tox
```
