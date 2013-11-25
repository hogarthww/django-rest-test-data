# pylint: disable=unused-argument,attribute-defined-outside-init
import json
import logging

from django.core import serializers
from django.db.models import get_model
from django.http import HttpResponse, HttpResponseNotFound
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from model_mommy import mommy

logger = logging.getLogger(__name__)


class BaseTestDataRestView(View):

    @property
    def serializer(self):  # pylint: disable=no-self-use
        return serializers.get_serializer("json")()

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.model = get_model(kwargs['app'], kwargs['model'])
        if self.model is None:
            return HttpResponseNotFound()

        if 'pk' in kwargs:
            try:
                self.object = self.get_object(int(kwargs['pk']),
                                              model=self.model)
            except:  # pylint: disable=bare-except
                logger.exception('Error fetching object')
                return HttpResponseNotFound()

        self.data = None if not request.body else json.loads(request.body)

        result = super(BaseTestDataRestView, self).dispatch(request, *args,
                                                            **kwargs)
        if isinstance(result, HttpResponse):
            return result
        elif isinstance(result, basestring):
            return HttpResponse(result,
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps(result),
                                content_type='application/json')

    @staticmethod
    def get_object(value, model=None):
        if model is None:
            model, value = value.split(':')
            model = get_model(*model.split('.'))
            value = int(value)
        return model.objects.get(pk=value)

    @classmethod
    def get_data(cls, data):
        kwargs = data.get('data', {}).copy()
        for key, value in data.get('objects', {}).iteritems():
            if isinstance(value, list):
                kwargs[key] = [cls.get_object(i) for i in value]
            else:
                kwargs[key] = cls.get_object(value)
        return kwargs


class TestDataModelRestView(BaseTestDataRestView):

    def get(self, request, *args, **kwargs):
        return self.serializer.serialize(self.model.objects.all())

    def delete(self, request, *args, **kwargs):
        try:
            qs = self.model.objects.all()
            count = qs.count()
            qs.delete()
        except:  # pylint: disable=bare-except
            logger.exception('Error deleting objects')
            return False
        else:
            return count

    def post(self, request, *args, **kwargs):
        if self.data is None:
            data = {}
        else:
            data = self.get_data(self.data)

        obj = mommy.make(self.model, **data)
        # Fetch from database because otherwise dates can't be serialized
        return self.serializer.serialize(
            [self.model.objects.get(pk=obj.pk)]
        )


class TestDataDetailRestView(BaseTestDataRestView):

    def get(self, request, *args, **kwargs):
        return self.serializer.serialize([self.object])

    def delete(self, request, *args, **kwargs):
        try:
            self.object.delete()
        except:  # pylint: disable=bare-except
            logger.exception('Error deleting object')
            return False
        else:
            return True


class TestDataSearchRestView(BaseTestDataRestView):

    def post(self, request, *args, **kwargs):
        if self.data is None:
            data = {}
        else:
            data = self.get_data(self.data)

        return self.serializer.serialize(self.model.objects.filter(**data))
