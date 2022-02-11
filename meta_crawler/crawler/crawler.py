
from .filesystem import FilesystemCrawler
from meta_crawler.settings import config
from meta_crawler.models import Run


def crawl():
    run = Run()
    run.save()
    for source in config["sources"]:
        if source["type"] == "filesystem":
            crawler = FilesystemCrawler(run, source["path"])
        else:
            raise ValueError(f"Unknown source type '{source['type']}'.")
        crawler.crawl()


