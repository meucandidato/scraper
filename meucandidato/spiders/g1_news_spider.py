# -*- coding: utf-8 -*-

import re

from urllib.parse import quote, unquote
from datetime import timedelta, datetime

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from meucandidato.items import NewsItem


class G1NewsSpider(CrawlSpider):
    name = "g1_news"
    allowed_domains = ["g1.globo.com"]
    rules = [
        Rule(LinkExtractor(allow=r'\?q=\w.*\&page=\d{1,2}'),
             callback='parse_item', follow=True)
    ]

    def __init__(self, keywords="", *args, **kwargs):
        super(G1NewsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            "http://g1.globo.com/busca/?q={0}".format(
                quote(keywords)
            ),
        ]

    def parse_start_url(self, response):
        return self._parse_news(response)

    def parse_item(self, response):
        return self._parse_news(response)

    def _parse_news(self, response):
        news_results = response.xpath(
            '//div[@class="busca-materia-padrao"]'
        )

        for news in news_results:
            item = NewsItem()
            item['title'] = news.xpath('a/@title').extract_first()

            item['portal_name'] = news.xpath(
                'p/span[@class="busca-portal"]/text()'
            ).extract_first()

            item['posted_at'] = news.xpath(
                'p/span[@class="busca-tempo-decorrido"]/text()'
            ).extract_first()

            item['posted_at'] = self._parse_post_date(
                re.sub(r'\n|\s{2,}', '', item['posted_at'])
            )

            item['summary'] = " ".join(news.xpath(
                'div/p[@class="busca-highlight"]/span/text()'
            ).extract())

            image_news = news.xpath('div/a/img/@src').extract()

            item['image'] = None
            if image_news:
                item['image'] = "http:{0}".format(image_news[0])

            item['url'] = news.xpath('a/@href').re(r'(?:;u=|&u=)(.*?)(?:&.*)')
            item['url'] = unquote(item['url'][0])

            item['search_origin'] = "G1"

            yield item

    def _parse_post_date(self, post_date):
        match = re.search(
            r'\d{1,2}\/\d{2}\/\d{4}\s\d{2}h\d{2}',
            post_date
        )

        if not match:
            return self._dehumanize_date(post_date)

        return datetime.strptime(post_date, "%d/%m/%Y %Hh%M")

    def _dehumanize_date(self, date):
        translations = {
            "dias": "days",
            "dia": "days",
            "horas": "hours",
            "hora": "hours",
            "minutos": "minutes",
            "minuto": "minutes"
        }
        dehumanized_date = datetime.now()

        _, number, time_type = date.split(" ")

        if re.search(r'\d.', date):
            kwargs = {translations.get(time_type): int(number)}
            dehumanized_date = datetime.now() - timedelta(**kwargs)

        return dehumanized_date
