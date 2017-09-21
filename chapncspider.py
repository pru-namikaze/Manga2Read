# -*- coding: utf-8 -*-
import scrapy
import json


class ChapncspiderSpider(scrapy.Spider):
    name = 'chapncspider'


    def __init__(self, curr_page,Chapter_Base_Page, *args, **kwargs):
        super(ChapncspiderSpider,self).__init__(*args, **kwargs)
        self.start_urls = [Chapter_Base_Page+str(curr_page)+'.html']

    def parse(self, response):
        #Scraping the Manga Name and Current Chapter Number
        name_and_num = response.xpath("//h1/a/text()").extract_first().strip().split()
        curr_chapter = float(name_and_num.pop())
        manga_name =  ' '.join(name_and_num).strip()
        #Scraping the Page Number and its Link
        vol = response.xpath("//div[@id='series']/strong/text()").extract()
        page_detail = {}
        page_detail[int(vol[1].strip().split()[1])] = response.xpath("//div[@class='read_img']/a/img/@src").extract_first()

        #Saving the data which remain unchanged within the chapter
        write_file = open(manga_name+str(curr_chapter)+".json", "w", encoding = "utf-8")
        json.dump(page_detail, write_file, ensure_ascii = False)
        write_file.close()
