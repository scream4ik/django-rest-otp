from setuptools import setup, find_packages

setup(
    name='django-rest-otp',
    version='0.1.10',
    packages=find_packages(),
    install_requires=[
        'Django>=2.0,<2.1',
        'djangorestframework>=3.7,<3.9',
        'djangorestframework-jwt<1.12',
        'Pillow',
        'pyotp<2.3',
        'qrcode<7.0',
        'redis-collections>=0.4,<0.5'
    ]
)
