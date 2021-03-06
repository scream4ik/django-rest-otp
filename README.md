# Django OTP and recovery codes auth with django-rest-framework

### Basic Installation

```
pip install https://github.com/scream4ik/django-rest-otp/archive/master.zip
```

- Add `rest_otp` to INSTALLED_APPS
- Add the following line to URLS
```
path('rest-otp/', include('rest_otp.urls')),
```
- Add the following lines to AUTHENTICATION_BACKENDS
```
'rest_otp.auth_backends.OtpAuthenticationBackend',
'rest_otp.auth_backends.RecoveryCodeAuthenticationBackend',
```

### Requirements
- redis-server
- Django>=2.0
- djangorestframework>=3.7
- djangorestframework-jwt<1.12
- Pillow
- pyotp==2.3.0
- qrcode<7
- redis-collections<1

### Configuration

- `REST_OTP_ISSUER_NAME` - Issuer Name for Provisioning URI
- `REST_OTP_REDIS_URL` - redis url scheme. For example `'redis://h:{}@{}:{}/0'.format(os.environ.get('REDIS_PASSWORD'), os.environ.get('REDIS_HOST'), os.environ.get('REDIS_PORT'))`
- `REST_OTP_JWT_SERIALIZER` - response for successful authentication
- `REST_OTP_USER_DETAILS_SERIALIZER` - serializer that include in `REST_OTP_JWT_SERIALIZER`
- `REST_OPT_LOGIN_RECOVERY_CODE_SERIALIZER` - serializer for login with recovery code
- `REST_OTP_RECOVERY_CODES_RANGE` - how much to generate recovery codes for user (default: 16)
- `REST_OTP_QR_VERSION` - controls the size of the QR Code (default 1). More info https://pypi.python.org/pypi/qrcode
- `REST_OTP_QR_BOX_SIZE` - the box_size parameter controls how many pixels each “box” of the QR code is. (default 10). More info https://pypi.python.org/pypi/qrcode
- `REST_OTP_QR_BORDER` - the border parameter controls how many boxes thick the border should be (default 4). More info https://pypi.python.org/pypi/qrcode
- `REST_OTP_ALLOWED_CHARS` - allowed chars for revocery codes creation (default: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789)

### How to use
In your Login view after user credentials validate call function `tmp_user_id`. Function get param user_id and return dict with temperary codes for OTP and recovery auth.
```
>>> from rest_otp.helpers import tmp_user_id
>>> data = tmp_user_id(1)
>>> print(data)
{'otp': 'Pe00izDPDVUN', 'recovery': 'KwSdJl7qFF77'}
```
Now you can transfer otp/recovery user temp key to next step form

### Endpoints

**GET /rest-otp/totp/**

response
```
{
    "id": 1,
    "otp_uri": "otpauth://totp/Secure%20App:admin?secret=RQL7JGHWNMOBJ742&issuer=Secure%20App",
    "qr_code": "BASE64_IMAGE_FORMAT_PNG",
    "secret": "RQL7JGHWNMOBJ742",
    "name": "admin",
    "issuer_name": "Secure App",
    "created": "2018-03-01T12:37:10.393985Z",
    "user": 1
}
```

**GET /rest-otp/recovery-codes/**

response
```
[
    {
        "code":"495765",
        "is_enable":true
    }
]
```

**POST /rest-otp/login/otp/**

request
```
{
    "tmp_user_id":"Jncdcd3",
    "otp_code":"495765"
}
```

response
```
{
    "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1Ni",
    "user":{
        "pk":13,
        "username":"user",
        "email":"",
        "first_name":"",
        "last_name":""
    }
}
```

**POST /rest-otp/login/recovery-code/**

request
```
{
    "tmp_user_id":"Jncdcd3",
    "recovery_code":"495765"
}
```

response
```
{
    "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1Ni",
    "user":{
        "pk":13,
        "username":"user",
        "email":"",
        "first_name":"",
        "last_name":""
    }
}
```
