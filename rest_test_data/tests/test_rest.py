# coding=utf-8
from datetime import datetime
import json

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse
from django.test import Client
from django.utils.timezone import utc

from nose.plugins.attrib import attr
from nose.tools import assert_equal

from rest_test_data.models import Key, Simple


class TestdataClient(Client):

    # pylint: disable=dangerous-default-value
    def post(self, path, data={}, content_type='application/json',
             follow=False, **extra):
        data = json.dumps(data, cls=DjangoJSONEncoder)
        return super(TestdataClient, self).post(path, data, content_type,
                                                follow, **extra)


def _pk_sort(l):
    l.sort(key=lambda x: x['pk'])

def _load_json_from_response(response):
    return json.loads(response.content.decode('utf-8'))


@attr('slow')
class TestBase(object):

    def setUp(self):
        self.client = TestdataClient()
        self.serializer = serializers.get_serializer("json")()
        self.clear()

    def tearDown(self):
        self.clear()

    @staticmethod
    def clear():
        Key.objects.all().delete()
        Simple.objects.all().delete()

    @staticmethod
    def url(model_object, pk=None, search=False):
        # pylint: disable=protected-access
        kwargs = {
            'model': model_object._meta.object_name.lower(),
            'app': model_object._meta.app_label.lower(),
        }
        if search:
            view = 'search'
        elif pk is None:
            view = 'objects'
        else:
            view = 'object'
            kwargs['pk'] = pk
        return reverse('rest_test_data:{}'.format(view), kwargs=kwargs)


class TestSimple(TestBase):

    def test_create(self):
        response = self.client.post(self.url(Simple))

        assert_equal(response.status_code, 200)
        assert_equal(response['Content-Type'], 'application/json')
        assert_equal(
            response.content,
            self.serializer.serialize([Simple.objects.get()]).encode('utf-8')
        )

    def test_str(self):
        self.client.post(
            self.url(Simple),
            {'data': {'str_attr': u'testdata ☃'}}
        )

        obj = Simple.objects.get()
        assert_equal(obj.str_attr, u'testdata ☃')

    def test_int(self):
        self.client.post(self.url(Simple), {'data': {'int_attr': 1}})

        obj = Simple.objects.get()
        assert_equal(obj.int_attr, 1)

    def test_date(self):
        # Supply timezone(django auto sets it otherwhise)
        # Supply microsecond as the database has less precision
        value = datetime.now().replace(tzinfo=utc, microsecond=0)
        self.client.post(self.url(Simple), {'data': {'date_attr': value}})

        obj = Simple.objects.get()
        assert_equal(obj.date_attr, value)

    def test_list(self):
        self.client.post(self.url(Simple))
        self.client.post(self.url(Simple))

        response = self.client.get(self.url(Simple))

        assert_equal(
            response.content,
            self.serializer.serialize(Simple.objects.all()).encode('utf-8')
        )

    def test_delete_all(self):
        self.client.post(self.url(Simple))
        self.client.post(self.url(Simple))

        assert_equal(Simple.objects.all().count(), 2, 'Objects not created')
        self.client.delete(self.url(Simple))
        assert_equal(Simple.objects.all().count(), 0)

    def test_get_one(self):
        self.client.post(self.url(Simple))
        obj = _load_json_from_response(
            self.client.post(self.url(Simple))
        )
        self.client.post(self.url(Simple))

        result = _load_json_from_response(
            self.client.get(self.url(Simple, pk=obj[0]['pk']))
        )
        assert_equal(obj, result)

    def test_delete_one(self):
        self.client.post(self.url(Simple))
        obj = _load_json_from_response(
            self.client.post(self.url(Simple))
        )
        self.client.post(self.url(Simple))
        assert_equal(Simple.objects.all().count(), 3, 'Objects not created')

        result = self.client.delete(self.url(Simple, pk=obj[0]['pk']))
        assert_equal(result.content, b'true')
        assert_equal(Simple.objects.all().count(), 2)
        assert_equal(Simple.objects.filter(pk=obj[0]['pk']).count(), 0)

    def test_search(self):

        response = self.client.post(
            self.url(Simple),
            {'data': {'int_attr': 1}}
        )
        q01 = _load_json_from_response(response)

        response = self.client.post(
            self.url(Simple),
            {'data': {'int_attr': 1}}
        )
        q01.extend(_load_json_from_response(response))

        response = self.client.post(
            self.url(Simple),
            {'data': {'int_attr': 1}}
        )
        q02 = _load_json_from_response(response)
        assert_equal(Simple.objects.all().count(), 3, 'Objects not created')

        response = self.client.post(
            self.url(Simple, search=True),
            {'data': {'int_attr': 1}}
        )
        result = _load_json_from_response(response)
        assert_equal(_pk_sort(result), _pk_sort(q01))

        response = self.client.post(
            self.url(Simple, search=True),
            {'data': {'int_attr': 2}}
        )
        result = _load_json_from_response(response)
        assert_equal(_pk_sort(result), _pk_sort(q02))

        response = self.client.post(self.url(Simple, search=True))
        result = _load_json_from_response(response)
        assert_equal(_pk_sort(result), _pk_sort(q01 + q02))


class TestKey(TestBase):

    def test_create(self):
        response = self.client.post(self.url(Key))

        assert_equal(response.status_code, 200)
        assert_equal(response['Content-Type'], 'application/json')
        assert_equal(
            response.content,
            self.serializer.serialize([Key.objects.get()]).encode('utf-8')
        )

    def test_f_key(self):
        self.client.post(self.url(Simple))
        simple = Simple.objects.get()
        self.client.post(self.url(Key), {
            'objects': {
                'f_key': 'rest_test_data.simple:{}'.format(simple.pk)
            }
        })

        obj = Key.objects.get()
        assert_equal(obj.f_key, simple)

    def test_m2m_key(self):
        self.client.post(self.url(Simple))
        self.client.post(self.url(Simple))
        simples = list(Simple.objects.all())
        self.client.post(self.url(Key), {
            'objects': {
                'm2m': [
                    'rest_test_data.simple:{}'.format(i.pk) for i in simples
                ]
            }
        })

        obj = Key.objects.get()
        assert_equal(list(obj.m2m.all()), simples)
