import logging
logger = logging.getLogger('streamcorpus')
logger.addHandler(logging.NullHandler())
import unittest
import streamcorpus
import shutil
import json

from scrapy.http import Request, TextResponse
from scrapy.utils.test import get_crawler
from scrapy.spider import Spider

from streamitem.loaders import StreamItemLoader
from streamitem.items import StreamItem
from streamitem.exporters import StreamItemExporter
from streamitem.storages import StreamItemFileFeedStorage


EXPORT_TEMP_DIR = '.exports'
EXPORT_SC_FILENAME = EXPORT_TEMP_DIR + '/streamitem.sc'

EXAMPLE_01 = {
    'url': 'http://www.example.com',
    'http_status': 200,
    'content_type': 'text/html',
    'response_size': 0,
    'metadata': {},
}
EXAMPLE_02 = {
    'url': 'http://www.example.com',
    'body': 'Redirections',
    'source_url': 'http://www.source.com',
    'redirect_urls': [
        'http://www.source.com',
        'http://www.example.com',
    ],
    'http_status': 200,
    'content_type': 'text/html',
    'response_size': 12,
    'metadata': {},
}
EXAMPLE_03 = {
    'url': 'http://www.example.com',
    'body': '404 - Not found',
    'http_status': 404,
    'content_type': 'text/html',
    'response_size': 15,
    'metadata': {},
}
EXAMPLE_04 = {
    'url': 'http://www.example.com',
    'body': 'I have metadata',
    'http_status': 200,
    'content_type': 'text/html',
    'response_size': 15,
    'metadata': {
        'language_code': 'ES',
        'language_name': 'Spanish',
        'emails_count': 5,
    },
}

METADATA_FIELDS = [
    'language_code',
    'language_name',
    'emails_count',
]


def load_item_from_values(values):
    request = Request(values['url'])
    response = TextResponse(
        url=values['url'],
        status=values['http_status'],
        body=values.get('body', ''),
        request=request,
        headers={
            'Content-Type': values['content_type'],
        }
    )
    if 'redirect_urls' in values:
        response.meta['redirect_urls'] = values['redirect_urls']
    loader = StreamItemLoader(item=StreamItem(), response=response)
    loaded_item = loader.load_item()
    loaded_item['metadata'] = values['metadata']
    return loaded_item


def print_debug_item(title, item):
    print '-'*80
    print title
    print '-'*80
    print item


class ItemLoad(unittest.TestCase):

    def _test_example(self, values, debug=False):
        expected_item = StreamItem(values)
        loaded_item = load_item_from_values(values)
        if debug:
            print_debug_item('expected_item', expected_item)
            print_debug_item('loaded_item', loaded_item)
        self.assertEquals(expected_item, loaded_item)

    def test_example_01(self):
        self._test_example(EXAMPLE_01, debug=False)

    def test_example_02(self):
        self._test_example(EXAMPLE_02, debug=False)

    def test_example_03(self):
        self._test_example(EXAMPLE_03, debug=False)

    def test_example_04(self):
        self._test_example(EXAMPLE_04, debug=False)


class BaseItemExporterTest(unittest.TestCase):

    def setUp(self):
        self._remove_temp_dir()

    def tearDown(self):
        self._remove_temp_dir()

    def _remove_temp_dir(self):
        shutil.rmtree(EXPORT_TEMP_DIR, ignore_errors=True)

    def _get_streamitem(self):
        for si in streamcorpus.Chunk(EXPORT_SC_FILENAME):
            return si
        return None

    def _export_streamitem(self, values):
        item = load_item_from_values(values)
        crawler = get_crawler()
        spider = Spider('streamitem_test')
        spider.set_crawler(crawler)
        storage = StreamItemFileFeedStorage(EXPORT_SC_FILENAME)
        exporter = StreamItemExporter(file=storage.open(spider))
        exporter.start_exporting()
        exporter.export_item(item)
        exporter.finish_exporting()

    def _test_example(self, values):
        self._export_streamitem(values)
        si = self._get_streamitem()

        self.assertEquals(values['url'], si.abs_url)
        self.assertEquals(values.get('source_url', None), si.original_url)
        self.assertEquals(values.get('body', ''), si.body.raw)
        self.assertEquals(values['content_type'], si.body.media_type)
        self.assertEquals(values['metadata'].get('language_code', '?'), si.body.language.code)
        self.assertEquals(values['metadata'].get('language_name', '?'), si.body.language.name)
        self.assertEquals(json.dumps(values.get('redirect_urls', [])), si.source_metadata['redirect_urls'])
        self.assertEquals(str(values['response_size']), si.source_metadata['response_size'])
        for metadata_field in METADATA_FIELDS:
            if metadata_field in values['metadata']:
                self.assertEquals(str(values['metadata'][metadata_field]), si.source_metadata[metadata_field])

    def test_example_01(self):
        self._test_example(EXAMPLE_01)

    def test_example_02(self):
        self._test_example(EXAMPLE_02)

    def test_example_03(self):
        self._test_example(EXAMPLE_03)

    def test_example_04(self):
        self._test_example(EXAMPLE_04)

