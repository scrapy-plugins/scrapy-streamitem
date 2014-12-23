import os

from scrapy.contrib.feedexport import FileFeedStorage


class StreamItemFileFeedStorage(FileFeedStorage):
    """
    This class exists only because the streamcorpus chunk writer expects
    a file in mode 'wb' instead of 'ab'. (When using file output)
    """
    def open(self, spider):
        dirname = os.path.dirname(self.path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        return open(self.path, 'wb')
