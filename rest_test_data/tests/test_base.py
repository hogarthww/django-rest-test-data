from django.core.serializers import json
from django.http import HttpResponseNotFound, HttpResponse
from django.views.generic import View

from rest_test_data.models import Simple
from rest_test_data.views import BaseTestDataRestView

from nose.tools import assert_equal, assert_is_instance
from mock import Mock, patch


def create_request(body=None):
    request = Mock()
    request.body = body
    return request


def test_dispatch_model_not_found():
    view = BaseTestDataRestView()
    result = view.dispatch(None, app='something', model='notfoundmodel')
    assert_is_instance(result, HttpResponseNotFound)


@patch.object(View, 'dispatch')
def test_dispatch_model_found(dispatch):
    dispatch.return_value = ''
    view = BaseTestDataRestView()
    view.dispatch(create_request(), app='rest_test_data', model='simple')
    assert_equal(view.model, Simple)
    assert_equal(dispatch.call_count, 1)


@patch.object(BaseTestDataRestView, 'get_object')
@patch.object(View, 'dispatch')
def test_dispatch_get_object(dispatch, get_object):
    dispatch.return_value = ''
    view = BaseTestDataRestView()
    result = view.dispatch(
        create_request(),
        app='rest_test_data',
        model='simple',
        pk='1'
    )
    get_object.assert_called_once_with(1, model=Simple)
    assert_is_instance(result, HttpResponse)
    assert_equal(dispatch.call_count, 1)


@patch.object(BaseTestDataRestView, 'get_object')
def test_dispatch_get_object_failure(get_object):
    get_object.side_effect = Exception
    view = BaseTestDataRestView()
    result = view.dispatch(None, app='rest_test_data', model='simple', pk='1')
    get_object.assert_called_once_with(1, model=Simple)
    assert_is_instance(result, HttpResponseNotFound)


def test_get_serializer():
    view = BaseTestDataRestView()
    assert_is_instance(view.serializer, json.Serializer)


@patch.object(View, 'dispatch')
def test_dispatch_wraps_string_result(dispatch):
    dispatch.return_value = 'result!'
    view = BaseTestDataRestView()
    result = view.dispatch(
        create_request(),
        app='rest_test_data',
        model='simple'
    )
    assert_is_instance(result, HttpResponse)
    assert_equal(result['Content-Type'], 'application/json')
    assert_equal(result.content, 'result!')


@patch.object(View, 'dispatch')
def test_dispatch_passes_http_response(dispatch):
    dispatch.return_value = HttpResponse()
    view = BaseTestDataRestView()
    result = view.dispatch(
        create_request(),
        app='rest_test_data',
        model='simple'
    )
    assert_equal(result, dispatch.return_value)


@patch.object(View, 'dispatch')
def test_dispatch_jsons_other(dispatch):
    dispatch.return_value = {'test': 'data'}
    view = BaseTestDataRestView()
    result = view.dispatch(
        create_request(),
        app='rest_test_data',
        model='simple'
    )
    assert_is_instance(result, HttpResponse)
    assert_equal(result['Content-Type'], 'application/json')
    assert_equal(result.content, '{"test": "data"}')


def test_get_object_model():
    model = Mock(**{'objects.get.return_value': 'object'})
    assert_equal(BaseTestDataRestView.get_object(1, model), 'object')
    model.objects.get.assert_called_once_with(pk=1)


@patch('rest_test_data.views.get_model')
def test_get_object_from_string(get_model):
    BaseTestDataRestView.get_object('app.model:1')
    get_model.assert_called_once_with('app', 'model')
    get_model().objects.get.assert_called_once_with(pk=1)


@patch.object(BaseTestDataRestView, 'get_object')
def test_get_data(get_object):
    result = BaseTestDataRestView.get_data({'data': {'test': 1},
                                            'objects': {
                                                'test_2': 'app.model:1',
                                                'test_3': ['app.model:1'],
                                            }})
    get_object.assert_called_with('app.model:1')
    assert_equal(result, {
        'test': 1,
        'test_2': get_object(),
        'test_3': [get_object()]
    })
