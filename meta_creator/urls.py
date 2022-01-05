from django.urls import path

from meta_creator import views
from meta_creator.settings import META_VERSIONS, LATEST_META_VERSION


app_name = "meta_creator"

urlpatterns = [path("", views.IndexView.as_view(), name="index")] + [
    path(version, views.CreatorView.as_view(metapath=metapath))
    for version, metapath in META_VERSIONS.items()
]
