# pylint: disable=no-value-for-parameter
from django.conf.urls import patterns, url

from rest_test_data.views import (
    TestDataModelRestView, TestDataDetailRestView, TestDataSearchRestView
)

urlpatterns = patterns('',
    url(r'^(?P<app>[^/]+)/(?P<model>[^/]+)/$',
        TestDataModelRestView.as_view(), name='objects'),
    url(r'^(?P<app>[^/]+)/(?P<model>[^/]+)/search/$',
        TestDataSearchRestView.as_view(), name='search'),
    url(r'^(?P<app>[^/]+)/(?P<model>[^/]+)/(?P<pk>\d+)/$',
        TestDataDetailRestView.as_view(), name='object'),
)
