
from django.urls import path

from . import views


app_name = 'meta_crawler'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('ajax/get_meta', views.get_meta, name='meta'),
]
