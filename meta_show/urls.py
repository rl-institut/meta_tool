
from django.urls import path

from meta_show import views


app_name = 'meta_show'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('show', views.ShowView.as_view(), name='show'),
    path('ajax/get_meta', views.JsonView.as_view(), name='meta'),
]
