
import pathlib

from django.conf import settings


METAJSONS_PATH = pathlib.Path(settings.BASE_DIR) / settings.JSONFORMS_SCHEMA_DIR
META_VERSIONS = {
    metapath.name[-8:-5]: metapath
    for metapath in METAJSONS_PATH.iterdir() if metapath.suffix == ".json"
}
LATEST_META_VERSION = max(list(META_VERSIONS.keys()))
