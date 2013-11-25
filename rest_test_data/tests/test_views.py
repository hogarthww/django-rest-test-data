from nose.tools import assert_equal
from mock import Mock, patch

from rest_test_data.views import (
    BaseTestDataRestView,
    TestDataDetailRestView,
    TestDataModelRestView,
    TestDataSearchRestView,
)


@patch.object(BaseTestDataRestView, 'serializer')
def test_get_all(serializer):
    view = TestDataModelRestView()
    view.model = Mock()
    view.get(None)
    view.model.objects.all.assert_called_once_with()
    serializer.serialize.assert_called_once_with(view.model.objects.all())


def test_delete_all():
    view = TestDataModelRestView()
    view.model = Mock()
    view.model.objects.all().count.return_value = 4
    assert_equal(view.delete(None), 4)
    view.model.objects.all().delete.assert_called_once_with()


def test_delete_all_failure():
    view = TestDataModelRestView()
    view.model = Mock()
    view.model.objects.all().delete.side_effect = Exception
    assert_equal(view.delete(None), False)
    view.model.objects.all().delete.assert_called_once_with()


@patch.object(BaseTestDataRestView, 'serializer')
@patch.object(BaseTestDataRestView, 'get_data')
@patch('rest_test_data.views.mommy')
def test_create(mommy, get_data, serializer):
    get_data.side_effect = lambda data: data
    mommy.make.return_value = Mock(pk=1)
    view = TestDataModelRestView()
    view.data = {'test_data': 'test'}
    view.model = Mock()
    view.post(None)
    mommy.make.assert_called_once_with(view.model, test_data='test')
    view.model.objects.get.assert_called_once_with(pk=1)
    serializer.serialize.assert_called_once_with([view.model.objects.get()])


@patch.object(BaseTestDataRestView, 'serializer')
@patch('rest_test_data.views.mommy')
def test_create_without_data(mommy, serializer):
    mommy.make.return_value = Mock(pk=1)
    view = TestDataModelRestView()
    view.data = None
    view.model = Mock()
    view.post(None)
    mommy.make.assert_called_once_with(view.model)
    view.model.objects.get.assert_called_once_with(pk=1)
    serializer.serialize.assert_called_once_with([view.model.objects.get()])


@patch.object(BaseTestDataRestView, 'serializer')
def test_get_single(serializer):
    view = TestDataDetailRestView()
    view.object = Mock()
    result = view.get(None)
    serializer.serialize.assert_called_once_with([view.object])
    assert_equal(result, serializer.serialize())


def test_delete_single():
    view = TestDataDetailRestView()
    view.object = Mock()
    result = view.delete(None)
    view.object.delete.assert_called_once_with()
    assert_equal(result, True)


def test_delete_single_failure():
    view = TestDataDetailRestView()
    view.object = Mock()
    view.object.delete.side_effect = Exception
    result = view.delete(None)
    view.object.delete.assert_called_once_with()
    assert_equal(result, False)


@patch.object(BaseTestDataRestView, 'serializer')
def test_search(serializer):
    view = TestDataSearchRestView()
    view.model = Mock()
    view.data = {'data': {'pk': 1}}
    result = view.post(None)
    view.model.objects.filter.assert_called_once_with(**view.data['data'])
    serializer.serialize.assert_called_once_with(view.model.objects.filter())
    assert_equal(result, serializer.serialize())


@patch.object(BaseTestDataRestView, 'serializer')
def test_search_all(serializer):
    view = TestDataSearchRestView()
    view.model = Mock()
    view.data = None
    result = view.post(None)
    view.model.objects.filter.assert_called_once_with()
    serializer.serialize.assert_called_once_with(view.model.objects.filter())
    assert_equal(result, serializer.serialize())

