Using django-rest-test-data
===========================

Data Types
----------

.. _instance_objects:

Instance Objects
~~~~~~~~~~~~~~~~

django-rest-test-data will return all instance objects as JSON objects.  The
JSON output is the result of passing the Django instance to the Django JSON
serializer.  See `the Django serialization documentation`_ for further details.

Instance Specifications
~~~~~~~~~~~~~~~~~~~~~~~

When creating or searching for an object, you will need to use an instance
specification.  An instance specification is a JSON object with two (optional)
keys:

``data``
    A JSON object mapping Django field names to values.

``objects``
    A JSON object mapping Django field names to object specifications (see
    below).  ``objects`` is used to handle relations between objects.

    An object specification is a string of the form
    ``<app name>.<model name>:<primary key>``.

    .. warning::
        Currently, django-rest-test-data assumes that all primary keys in
        object specifications are integers.

Performing Actions
------------------

.. note::
    All URLs in this document will be given relative to the
    django-rest-test-data root; this will be different depending on where you
    hook up the URL in your URL config.

Listing All Objects
~~~~~~~~~~~~~~~~~~~

To list all objects, perform a GET request to the base of the model resource::

    GET /<app_name>/<model_name>/

This will return a JSON list containing :ref:`instance_objects` for all
``<model_name>`` instances in the database.

Searching for Objects
~~~~~~~~~~~~~~~~~~~~~

To search all objects, perform a POST request to the /search/ sub-resource of
the model resource::

    POST /<app_name>/<model_name>/search/

The body of the POST request should contain a JSON object with a single key,
"data".  This key should map to a JSON object which contains the search
criteria::

    {
        "data": {
            "key": "value",
            "other_key": "another value"
    }

The key/value pairs within the search criteria are passed to the model's
manager's filter method, so see `the Django filter documentation`_ for further
details.

The search call will return a JSON list containing :ref:`instance_objects` for
all ``<model_name>`` instances in the database that match the given search
terms.

Searching Based on Relations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Getting a Single Object
~~~~~~~~~~~~~~~~~~~~~~~

Creating an Object
~~~~~~~~~~~~~~~~~~

Foreign Keys
~~~~~~~~~~~~

Many-to-Many Fields
~~~~~~~~~~~~~~~~~~~

Deleting All Objects
~~~~~~~~~~~~~~~~~~~~

Deleting an Object
~~~~~~~~~~~~~~~~~~


.. _the Django serialization documentation:
    https://docs.djangoproject.com/en/dev/topics/serialization/#id2

.. _the Django filter documentation:
    https://docs.djangoproject.com/en/dev/topics/db/queries/#retrieving-specific-objects-with-filters
