# -*- coding: utf-8 -*-

import pymongo

from scrapy import log
from scrapy.conf import settings
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing {0}".format(data))
        self.collection.update_one(
            {'url': item['url']},
            {
                "$set": {
                    'title': item['title'],
                    'portal_name': item['portal_name'],
                    'posted_at': item['posted_at'],
                    'summary': item['summary'],
                    'image': item['image'],
                    'url': item['url'],
                    'search_origin': item['search_origin']
                }
            },
            upsert=True
        )
        log.msg("News added to MongoDB database!",
                level=log.DEBUG, spider=spider)

        return item
