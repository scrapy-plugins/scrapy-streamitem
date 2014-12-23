from scrapy import Item, Field
from scrapy.contrib.loader.processor import TakeFirst


class StreamItem(Item):
    """Scrapy Item definition for a streamitem"""

    url = Field(output_processor=TakeFirst())
    body = Field(output_processor=TakeFirst())
    source_url = Field(output_processor=TakeFirst())
    redirect_urls = Field()
    http_status = Field(output_processor=TakeFirst())
    content_type = Field(output_processor=TakeFirst())
    response_size = Field(output_processor=TakeFirst())
    metadata = Field(output_processor=TakeFirst())
