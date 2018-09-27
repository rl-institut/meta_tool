
from django.urls import path

from meta_show import views


app_name = 'stemp'

urlpatterns = [
    path('', views.ShowView.as_view(), name='show'),
]