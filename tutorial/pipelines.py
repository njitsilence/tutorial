# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import logging
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request
class PeoplePipeline(object):

    def open_spider(self,spider):
        self.file = open("items.json","w",encoding="UTF-8")

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self,spider):
        self.file.close()

class MyImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        logging.info(item)
        for image_url in item['image_urls']:
            yield Request(image_url)
        # yield Request(item["image_urls"])

    def item_completed(self, results, item, info):
        image_paths = [x["path"] for ok,x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item["image_paths"] = image_paths

        return item

