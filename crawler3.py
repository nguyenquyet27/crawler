#play with crawler
from bs4 import BeautifulSoup
import urllib.request
import re

#tao listlinks
def not_relative_uri(href):
    return re.compile('^https://').search(href) is  not  None

url =  'https://vnexpress.net'
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

new_feeds = soup.find('section', class_='featured container clearfix').find_all(
        'a', class_='', href=not_relative_uri)
new_feeds2 = soup.find('section', class_='sidebar_home_1').find_all(
        'a', class_='', href=not_relative_uri)
links = set()
for feed in new_feeds:
    link = feed.get('href')
    links.add(link)

for feed in new_feeds2:
    link = feed.get('href')
    links.add(link)
#crawl cac link trong listlinks
list0 = list(set(links))
#xoa link
def xoalink(list1):
    n = len(list1)
    i = 0
    while (i<n):
        k = "video.vnexpress.net" in list1[i]
        k1 = "e.vnexpress.net" in list1[i]
        k2 = "longform" in list1[i]
        k3 = "bang-gia" in list1[i]
        if (k == 1 or k1 == 1 or k2 == 1 or k3 == 1):
            del list1[i]
            n = n-1
        i = i+1
    return list1
list2 = xoalink(list0)
list3 = xoalink(list2)
listlinks = xoalink(list3)
n2 = len(listlinks)
for i in range(0,n2):
    url = listlinks[i]
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    crawl = soup.find('section', class_='container')
    print ("Link: ",i)
    #Lay tieu de cua link
    title = crawl.find('h1')
    if (title != None):
        title = crawl.find('h1').text
        print ("Tieu de: ")
        print (title)
    #Lay phan tom tat cua link
    description = crawl.find('p', class_ = 'description')
    if (description != None):
        description = crawl.find('p', class_ = 'description').text
        print ("Tom tat: ")
        print (description)
    #Lay noi dung cua link
    print ("Noi dung: ")
    k = crawl.find('article')
    if (k != None):
        content = crawl.find('article').find_all('p', class_ = 'Normal')
        for p in content:
            d = p.string
            if (d != None):
                print(p.string)
    #Lay ngay dang cua link
    posting_time = crawl.find(class_ = 'time left')
    if (posting_time != None):
        posting_time = crawl.find(class_ = 'time left').text
        print ("Ngay dang: ")
        print (posting_time)

    
