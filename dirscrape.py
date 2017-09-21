import json
from urllib.request import urlopen as request
from bs4 import BeautifulSoup as soup

#Grabbing the directory page
url = 'http://mangafox.me/directory/'

client = request(url)
page = client.read()
client.close()

page_soup = soup(page, "html.parser")

#Initilising the containers
containers_img = page_soup.findAll("a", {"class" : "manga_img"})
containers_name_link = page_soup.findAll("div", {"class" : "manga_text"})
containers_rating = page_soup.findAll("span", {"class" : "rate"})
containers_latest = page_soup.findAll("p", {"class" : "nowrap latest"})

#Setting the parameters
img = []
name = []
link = []
rating = []
latest_chapter_no = []
latest_chapter_link = []

#Getting image link
for item in containers_img:
        img.append(item.div.img["src"])


#Getting name and link
for item in containers_name_link:
        name.append(item.a.text)
        link.append(item.a["href"])


#Getting rating
for item in containers_rating:
        rating.append(item.text)


#Getting latest chapter no. and its link
for item in containers_latest:
        latest_chapter_no.append(item.text)
        latest_chapter_link.append(item.a["href"])


#Making dictionary out of the data
manga = {}
for i in range(0,len(name)):
        dictionary = {}
        dictionary["img"] = img[i]
        dictionary["name"] = name[i]
        dictionary["link"] = link[i]
        dictionary["rank"] = i
        dictionary["rating"] = int(rating[i])
        dictionary["latest_chapter_no"] = latest_chapter_no[i]
        dictionary["latest_chapter_link"] = latest_chapter_link[i]
        manga[name[i]] = dictionary


#Storing the info into json style in .txt file
write_file = open("directory.json", "w", encoding = "utf-8")
json.dump(manga, write_file, ensure_ascii = False)
write_file.close()
