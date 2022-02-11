
import json
import pathlib

from meta_crawler.crawler.base import Crawler
from meta_crawler.models import Source, Meta, Owner, Tag


class FilesystemCrawler(Crawler):
    def __init__(self, run, path):
        self.source = Source(run=run, type="filesystem", path=path)
        self.source.save()
        self.path = pathlib.Path(path)

    def crawl(self):
        meta_counter = 0
        for path in self.path.rglob("*"):
            if path.suffix != ".json":
                continue
            with open(path, "r") as jsonfile:
                try:
                    metadata = json.load(jsonfile)
                except json.JSONDecodeError:
                    continue
            if "metaMetadata" not in metadata:
                continue

            # We found metadata!
            meta_counter += 1
            print("Metadata found: ", meta_counter)

            try:
                owner_data = metadata["contributors"][0]
            except (KeyError, IndexError):
                owner = None
            else:
                owner = Owner.objects.get_or_create(name=owner_data["title"], email=owner_data["email"])[0]
            meta = Meta(
                source=self.source,
                location=str(path),
                version=metadata["metaMetadata"]["metadataVersion"],
                title=metadata["title"],
                name=metadata["name"],
                metadata=metadata,
                owner=owner,
            )
            meta.save()

            for keyword in metadata["keywords"]:
                if keyword == "":
                    continue
                tag = Tag.objects.get_or_create(name=keyword)[0]
                meta.tags.add(tag)
