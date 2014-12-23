from scrapy.contrib.loader import ItemLoader
from scrapy.http import TextResponse


class StreamItemLoader(ItemLoader):
    """Scrapy Item loader for a streamitem"""

    def __init__(self, item=None, selector=None, response=None, **context):
        super(StreamItemLoader, self).__init__(item=item, selector=selector, response=response, context=context)

        redirect_urls = response.meta.get('redirect_urls', [])
        if redirect_urls:
            redirect_urls.append(response.url)  # Append the final URL to have the entire redirection trail.

        self.add_value('url', response.url)
        self.add_value('body', response.body_as_unicode() if isinstance(response, TextResponse) else '')
        self.add_value('source_url', redirect_urls[0] if redirect_urls else None)
        self.add_value('redirect_urls', redirect_urls)
        self.add_value('http_status', response.status)
        self.add_value('content_type', response.headers.get('Content-Type', None))
        self.add_value('response_size', len(response.body))
        self.add_value('metadata', {})
