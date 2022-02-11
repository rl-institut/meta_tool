from abc import ABC, abstractmethod


class Crawler(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        super(Crawler, self).__init__()

    @abstractmethod
    def crawl(self):
        pass