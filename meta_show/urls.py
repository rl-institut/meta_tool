
from django.urls import path

from meta_show import views


app_name = 'meta_show'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('show', views.ShowView.as_view(), name='show'),
    path('crawler', views.CrawlerView.as_view(), name='crawler'),
    path('ajax/get_meta', views.get_meta, name='meta'),
]
