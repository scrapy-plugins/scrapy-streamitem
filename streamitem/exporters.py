import json
import streamcorpus
import time

from scrapy.contrib.exporter import BaseItemExporter

from streamitem.items import StreamItem


class StreamItemExporter(BaseItemExporter):
    """Scrapy Item exporter to streamcorpus .sc file"""

    encoding = 'utf-8'

    def __init__(self, file, **kwargs):
        self._configure(kwargs, dont_fail=True)
        self._chunk = streamcorpus.Chunk(file_obj=file, mode='wb')

    def export_item(self, item):
        assert isinstance(item, StreamItem), 'Exported item must subclass StreamItem'
        self._chunk.add(self._get_stream_item(item))

    def finish_exporting(self):
        # Call flush instead of close because the feed exporter acts on the file
        # through seek and closing conflicts with implementation.
        self._chunk.flush()

    def _get_stream_item(self, item):
        stream_item = streamcorpus.make_stream_item(time.time(), item['url'])
        stream_item.body.raw = self._encode(item.get('body', u''))
        stream_item.body.media_type = self._get_media_type(item)
        stream_item.body.encoding = self.encoding
        stream_item.original_url = item.get('source_url')
        meta = self._get_metadata(item)
        stream_item.body.language = streamcorpus.Language(
            code=meta.get('language_code', '?'),
            name=meta.get('language_name', '?'))
        stream_item.source_metadata = meta
        return stream_item

    def _get_media_type(self, item):
        # Content type might contain the encoding which we actually superseed
        # with utf-8.
        ctype = item.get('content_type') or u''
        return self._encode(ctype.partition(';')[0])

    def _get_metadata(self, item):
        meta = {
            'response_size': json.dumps(item.get('response_size', 0)),
            'redirect_urls': json.dumps(item.get('redirect_urls', [])),
        }
        meta.update([(k, unicode(v)) for k, v in item['metadata'].items()])
        return meta

    def _encode(self, s):
        if isinstance(s, unicode):
            return s.encode(self.encoding)
        return s
