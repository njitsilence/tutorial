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
from tutorial.items import PeopleItem,MyImageItem

class PeoplePipeline(object):

    def open_spider(self,spider):
        self.file = open("items.json","w",encoding="UTF-8")

    def process_item(self, item, spider):
        logging.info("===========================come to process_item")
        logging.info(isinstance(item,PeopleItem))
        if isinstance(item,PeopleItem):
            line = json.dumps(dict(item),ensure_ascii=False) + "\n"
            self.file.write(line)
        return item

        # line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # self.file.write(line)
        # return item

    def close_spider(self,spider):
        self.file.close()

class MyImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        logging.info("===================come to get_media_request")
        logging.info(isinstance(item, MyImageItem))
        logging.info(item)
        if isinstance(item, MyImageItem):

            for image_url in item['image_urls']:
                yield Request(image_url,meta={"item":item})

        # for image_url in item['image_urls']:
        #     yield Request(image_url, meta={"item": item})
        # yield Request(item["image_urls"])

    def item_completed(self, results, item, info):

        if isinstance(item, MyImageItem):
            image_paths = [x["path"] for ok,x in results if ok]
            if not image_paths:
                 raise DropItem("Item contains no images")
            item["image_paths"] = image_paths

            return item

        # image_paths = [x["path"] for ok, x in results if ok]
        # if not image_paths:
        #     raise DropItem("Item contains no images")
        # item["image_paths"] = image_paths
        #
        # return item

    def file_path(self, request, response=None, info=None):
        # logging.info("=========file_path===================")
        # logging.info(request)
        # logging.info(response)
        # logging.info(info)
        # logging.info(request.meta)
        # logging.info(request.meta["item"])

        return 'full/%s.jpg' % request.meta["item"]["image_name"]

