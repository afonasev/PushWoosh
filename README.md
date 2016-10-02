# Pushwoosh
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Afonasev/PushWoosh/blob/master/LICENSE)
[![Build Status](https://travis-ci.org/Afonasev/PushWoosh.svg?branch=master)](https://travis-ci.org/Afonasev/pushwoosh)
[![Coverage Status](https://coveralls.io/repos/github/Afonasev/PushWoosh/badge.svg?branch=master)](https://coveralls.io/github/Afonasev/PushWoosh?branch=master)

## Installing
```
$ pip install git+https://github.com/Afonasev/pushwoosh
```

## Create message
```python
import pushwoosh.client

pushwoosh.client.create_message(
    application='APPLICATION_CODE',
    auth_token='AUTH_TOKEN',
    content={'ru': 'ru text', 'en': 'eng text'},
    params={'android_ibc': 'red'},
    filters={'geoid': [1, 2, 3]},
)
```

## Running the testsuite

The minimal requirement for running the testsuite is ``pytest``.  You can
install it with::

    pip install pytest

Then you can run the testsuite with::

    py.test
