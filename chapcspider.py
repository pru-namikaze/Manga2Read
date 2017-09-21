# -*- coding: utf-8 -*-
import scrapy
import json
import subprocess

mangainfo = 'http://mangafox.me/manga/one_piece/'
chapter_start_page = 'http://mangafox.me/manga/one_piece/vTBD/c877/1.html'
Manga_Name = "One Piece"
curr_chapter = 877

class ChapspiderSpider(scrapy.Spider):
    name = 'chapspider'
    allowed_domains = [mangainfo]
    start_urls = [chapter_start_page]

    def parse(self, response):

        #If no file is present then make a new dictionary
        chapter_detail = {}
        #The data which remain common within pages
        name_and_num = response.xpath("//h1/a/text()").extract_first().strip().split()
        chapter_detail['curr_chapter'] = int(name_and_num.pop())
        chapter_detail['Manga_Name'] =  ' '.join(name_and_num).strip()
        chapter_detail['curr_volume'] = response.xpath("//div[@id='series']/strong/text()").extract()[0].strip().split('v')[len(response.xpath("//div[@id='series']/strong/text()").extract())-1]
        chapter_detail['curr_chapter_total_page'] = int(response.xpath("//div[@class='l']/text()").extract()[1].strip().split()[1])



        #All the page and their respective image link in a chapter
        page_details = {}
        for  i in range(1,chapter_detail['curr_chapter_total_page']+1):
            #Running the spiders
            subprocess.run(["scrapy","runspider","chapncspider.py","-a","curr_page="+str(i)])

            #Extracting the information extracted from each page
            data_file = open(Manga_Name+str(curr_chapter)+".json","r")
            page_details.update(json.load(data_file))
            data_file.close()

        chapter_detail['page_no_and_img_link'] = page_details

        #Saving the data which remain unchanged within the chapter
        write_file = open(Manga_Name+str(curr_chapter)+".json", "w", encoding = "utf-8")
        json.dump(chapter_detail, write_file, ensure_ascii = False)
        write_file.close()
