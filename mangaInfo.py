import json
from urllib.request import urlopen as request
from bs4 import BeautifulSoup as soup


#Manga Name here
print("Enter a manga name: ")
manga_name = input()
#manga_name = 'TALES OF DEMONS AND GODS'

#Making the URL for the manga
manga_url_id = manga_name.lower().replace(" ","_")
manga_url = 'http://mangafox.me/manga/'+manga_url_id+'/'


"""
    Try - Catch, to check if the Url can be obtained from the manga name
"""



#Grabbing the directory page
client = request(manga_url)
page = client.read()
client.close()

page_soup = soup(page, "html.parser")

#Initilising the containers
containers_name = page_soup.find("h1")
container_facts = page_soup.findAll("td", {"valign" : "top"})
container_img_link = page_soup.find("img", {"width" : "200"})
container_summary = page_soup.find("div", {"id" : "title"})
container_stats = page_soup.findAll("div", {"class" : "data"})
container_vol_stat = page_soup.findAll("div",{"class":"slide"})
container_chap_list = page_soup.findAll("h4")


#Storage variables
details = {}
details["Name"] = containers_name.text
details["Classification"] = containers_name.text.split()[len(containers_name.text.split())-1]
details["Released"] = container_facts[0].a.text
details["Authors"] = container_facts[1].a.text
details["Artist(s)"] = container_facts[2].a.text
details["Genre(s)"] = container_facts[3].text.replace("\n","").replace(" ","").split(',')
details["Img_link"] = container_img_link["src"]
details["Summary"] = container_summary.p.text
details["Status"] = container_stats[0].span.text.replace("\n","").replace("\r","").replace(" ","").split(',')[0]
details["Upcomming_Chapter"] = container_stats[0].span.i.h2.a.text
details["Rank"] = container_stats[1].span.text.replace("\n","").replace("\r","").replace(" ","").split(',')[0]
details["Monthly_views"] = container_stats[1].span.text.split()[3]
details["Volume_stat"] = []

#To store the list of chapters of a manga
chap_list = []
for i in range(0,len(container_chap_list)):
    chap_list.append(container_chap_list[i].a.text.split()[len(container_chap_list[i].a.text.split())-1])
#To store the list of chapters of a manga
chap_link_list = []
for i in range(0,len(container_chap_list)):
    chap_link_list.append(container_chap_list[i].a["href"])
#To Store the Title of the chapter
title_list = []
for i in range(0,len(container_chap_list)):
    if container_chap_list[i].span is not None:
        title_list.append(container_chap_list[i].span.text)
    else:
        title_list.append("  ")


#To store the Starting, Ending and the List of chapters with there Title of a Volume
for i in range(0,len(container_vol_stat)):
    start = container_vol_stat[i].h3.text.split()[len(container_vol_stat[i].h3.text.split())-3]
    end = container_vol_stat[i].h3.text.split()[len(container_vol_stat[i].h3.text.split())-1]
    chap = []
    det = {}
    for j in range(0,len(chap_list)):
        if float(chap_list[j]) >= float(start) and float(chap_list[j]) <= float(end):
            chap.append({chap_list[j]:title_list[j],'link':chap_link_list[j]})
    volume_no = container_vol_stat[i].h3.text.split()[1]
    #if volume number is not abailable then set it to TBA
    if not volume_no.isdigit():
        volume_no = 'TBA'
    det[volume_no] = {'start':start,'end':end,'chap_list':chap}
    details["Volume_stat"].append(det)



#Storing the info into json style in .txt file
write_file = open(manga_url_id+".json", "w", encoding = "utf-8")
json.dump(details, write_file, ensure_ascii = False)
write_file.close()
