# Pushwoosh
[![Build Status](https://travis-ci.org/Afonasev/PushWoosh.svg?branch=master)](https://travis-ci.org/Afonasev/pushwoosh)
[![Code Climate](https://codeclimate.com/github/Afonasev/PushWoosh/badges/gpa.svg)](https://codeclimate.com/github/Afonasev/PushWoosh)
[![Test Coverage](https://codeclimate.com/github/Afonasev/PushWoosh/badges/coverage.svg)](https://codeclimate.com/github/Afonasev/PushWoosh/coverage)

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
