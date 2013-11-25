from setuptools import setup


setup(
    name='django-rest-test-data',
    description='Django app that exposes an API that lets you put the'
                ' database in any (legal) desired state.',
    version='0.1.0',
    author='Hogarth Worldwide Ltd.',
    author_email='zonza-devs@hogarthww.com',
    install_requires=['Django', 'model_mommy'],
    packages=['rest_test_data'],
)
