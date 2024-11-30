import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import hashlib

class UnsplashPipeline:
    def process_item(self, item, spider):
        # Generate _id only if it's not already present
        if '_id' not in item or not item['_id']:
            key_fields = [item['name'], item['country'], item['date'], item['url'], str(item['photos'])] # Список ключевых полей
            key_string = u"".join(key_fields).encode('utf-8') # Объединяем поля в строку и кодируем в UTF-8
            item['_id'] = hashlib.sha256(key_string).hexdigest() # Генерация SHA256 хеша

        return item


class UnsplashPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for img_url in item['photos']:
            if img_url:
                yield scrapy.Request(img_url)

    def item_completed(self, results, item, info):
        item['photos'] = [x['path'] for ok, x in results if ok]
        return item

