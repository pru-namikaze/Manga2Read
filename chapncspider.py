# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import json

chapter_base_page = 'http://mangafox.me/manga/one_piece/vTBD/c877/'
#curr_page = 2
Manga_Name = 'One Piece'
curr_chapter = 877



class ChapncspiderSpider(CrawlSpider):
    name = 'chapncspider'

    def __init__(self, curr_page, *args, **kwargs):
        super(ChapncspiderSpider,self).__init__(*args, **kwargs)
        self.start_urls=[chapter_base_page+str(curr_page)+'.html/']

    def parse(self, response):
        vol = response.xpath("//div[@id='series']/strong/text()").extract()
        page_detail = {}
        page_detail[int(vol[1].strip().split()[1])] = response.xpath("//div[@class='read_img']/a/img/@src").extract_first()

        #Saving the data which remain unchanged within the chapter
        write_file = open(Manga_Name+str(curr_chapter)+".json", "w", encoding = "utf-8")
        json.dump(page_detail, write_file, ensure_ascii = False)
        write_file.close()

        return page_detail
