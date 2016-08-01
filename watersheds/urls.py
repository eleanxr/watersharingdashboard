from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'$', views.ListWatershedsAPIView.as_view(), name='list-watersheds'),
]
