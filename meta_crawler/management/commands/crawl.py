
from django.core.management.base import BaseCommand

from meta_crawler.crawler import crawler


class Command(BaseCommand):
    help = 'Crawls all sources given in crawler config'

    def handle(self, *args, **options):
        crawler.crawl()
        self.stdout.write(self.style.SUCCESS('Successfully crawled all sources'))
