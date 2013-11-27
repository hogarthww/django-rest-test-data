Getting Started
===============

django-rest-test-data is a reusable Django application.  To get started, you'll
need to install it::

    pip install django-rest-test-data

Once you've done that, you'll need to add it to your ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        ...,
        rest_test_data,
    ]

You'll also need to hook it up in your URLs; it's up to you where you put it
but in this example we'll put it at ``/testdata/``::

    urlpatterns = patterns('',
        ...,
        url('testdata/', include('rest_test_data.urls', namespace='rest_test_data')),
    )

Now let's test it!  Choose an app and model in your application and plug them
in to the following (``auth`` and ``User`` might make sense)::

    $ ./manage.py runserver

    # and in another shell:
    $ curl http://localhost:8000/testdata/<app>/<model>/

You should get back a JSON list containing all of the instances of that model.
To see what else you can do, move on to the next section.
