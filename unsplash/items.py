import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose
from scrapy.utils.project import get_project_settings
import hashlib
import re
def process_text(value):
    if value:
        value = value[0].strip()
    else:
        value = 'no information available'
    return value

def process_photo(value: str):
    if value and value.startswith('https'):
        return re.search(r"(https:.+?(?=\s|$))", value).group(1)
    elif value and value.startswith('data'):
        return None
    else:
        return None


class UnsplashItem(scrapy.Item):
    name = scrapy.Field(input_processor=Compose(process_text), output_processor=TakeFirst())
    country = scrapy.Field(input_processor=Compose(process_text), output_processor=TakeFirst())
    date = scrapy.Field(input_processor=Compose(process_text), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(process_photo))
    tag_title = scrapy.Field(input_processor=Compose(process_text), output_processor=TakeFirst())
    tag_href = scrapy.Field(input_processor=Compose(process_text), output_processor=TakeFirst())
    _id = scrapy.Field()
