from django.urls import path

from meta_creator import views


app_name = 'meta_creator'

urlpatterns = [
    path('', views.CreatorView.as_view(), name='creator')
]