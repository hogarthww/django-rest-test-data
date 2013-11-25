from django.conf.urls import include, url


urlpatterns = (
    url('', include('rest_test_data.urls', namespace='rest_test_data')),
)
