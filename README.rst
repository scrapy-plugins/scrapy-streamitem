=================
scrapy-streamitem
=================

.. image:: https://badge.fury.io/py/scrapy-streamitem.png
   :target: http://badge.fury.io/py/scrapy-streamitem

.. image:: https://api.travis-ci.org/scrapinghub/scrapy-streamitem.png?branch=master
   :target: http://travis-ci.org/scrapinghub/scrapy-streamitem

Overview
========

Scrapy support for working with streamcorpus_ StreamItems_.

Includes the following:

- **StreamItem**: Scrapy Stream Item definition. ``streamitem.items.StreamItem``
- **StreamItemLoader**: Scrapy Itemloader for ``StreamItem``. ``streamitem.loaders.StreamItemLoader``
- **StreamItemExporter**: Scrapy ItemExporter to .sc file. ``streamitem.exporters.StreamItemExporter``
- **StreamItemFileFeedStorage**: Scrapy FileFeedStorage to handle .sc files. ``streamitem.storages.StreamItemFileFeedStorage``

Stream Items
============

Scrapy Stream Item will be populated from response with the following fields:

- **url**: A string containing the URL of the response.
- **body**: A string containing the body of this Response. 
- **source_url**: If response has been redirected, a string containing the URL of the original page. Defaults to None.
- **redirect_urls**: If response has been redirected, a list containing the URLs of all the redirected pages, including the current one. Defaults to None.
- **http_status**: An integer representing the HTTP status of the response. Example: 200, 404.
- **content_type**: A string containing the Content-Type HTTP header of the response.
- **response_size**: An integer representing the response body size in bytes.
- **metadata**: A dict containing arbitrary metadata for this page.

If items are exported they will generate streamcorpus StreamItem_ items filling the following fields:

- **abs_url**: item.url
- **source_url**: item.source_url
- **body.raw**: item.body
- **body.media_type**: item.content_type
- **body.language.code**: item.metadata.language_code
- **body.language.name**: item.metadata.language_name
- **source_metadata['redirect_urls']**: item.redirect_urls
- **source_metadata['response_size']**: item.response_size
- **source_metadata**: will be filled with all fields in item.metadata

How to use it
=============

An example of use from a spider::

    def parse_page(self, response):
        loader = StreamItemLoader(item=StreamItem(), response=response)
        return loader.load_item()

Settings for exporting::

    FEED_URI = ".exports/streamitems.sc"
    FEED_FORMAT = "streamcorpus"
    FEED_EXPORTERS = {
        'streamcorpus': 'scrapylib.streamitem.exporters.StreamItemExporter',
    }
    FEED_STORAGES = {
        '': 'scrapylib.streamitem.storages.StreamItemFileFeedStorage',
    }
    
You can also add additional info to your item using the ``metadata`` field.
For example from a Item pipeline::

    def process_item(self, item, spider):
         item['metadata']['my_custom_field'] = 'whatever'
         return item


Requirements
============

* Scrapy_ >= 0.22.0
* streamcorpus_

Install
=======

using pypi::

   pip install scrapy-streamitem


.. _streamcorpus: https://github.com/trec-kba/streamcorpus
.. _StreamItem: http://streamcorpus.org/sphinx-docs/streamcorpus.html#stream-items
.. _StreamItems: http://streamcorpus.org/sphinx-docs/streamcorpus.html#stream-items
.. _Scrapy: https://github.com/scrapinghub/scrapy
