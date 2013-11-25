Motivation
==========

Why django-rest-test-data?
--------------------------

In the spirit of `Continuous Delivery`_, we believe the following:

* Running automated tests driven by Selenium against our websites is a Good
  Thing™, and
* Running those tests against environments that closely resemble our production
  environments is also a Good Thing™.

Whilst striving to achieve these two Good Things™, we found that fixtures were
causing us problems.  Our initial solution was to set up all of the data that
we needed in the `"Given"`_ parts of our acceptance tests.  This caused a
couple of problems: it opened us up to more "weird" Selenium failures [#weird]_
but, more importantly, it made our tests deadly slow.

We then took stock of the situation. We considered using a Django-based test
runner, and using Django fixtures. We concluded, however, that this would limit
our ability to run the tests against the gamut of environments that we would
like to be able to run them against [#runserver]_.

We concluded that our best bet was to build a simple API that would allow us to
programatically set up the data in our environments however we needed it to be
set up for our testing.  ``django-rest-test-data`` (initally known just as
``testdata`` internally), was the result of that effort.

What it isn't
-------------

django-rest-test-data isn't a solution for any problem you have in production.
Not even one.  It is horribly insecure, it doesn't give you any control over
how your data is represented, nor does it support any sort of versioning.

If you want any of those things (and, for production code, you do), then you
should check out `Django Rest Framework`_.

.. _Continuous Delivery: http://www.amazon.co.uk/Continuous-Delivery-Deployment-Automation-Addison-Wesley/dp/0321601912

.. _"Given": http://guide.agilealliance.org/guide/gwt.html

.. _Django Rest Framework: http://django-rest-framework.org/

.. rubric:: Footnotes

.. [#weird]
    This isn't a great reason, really. We should obviously have been stamping
    these failures out, rather than ignoring them. This, however, is much
    easier said than done.

.. [#runserver]
    A lot of [#weasel]_ the implementations of Django-based Selenium test
    runners seem to have a strong dependency on ``runserver``.  We didn't want
    to have to try and break this dependency.

.. [#weasel]
    Yes, I know, weasel words.
