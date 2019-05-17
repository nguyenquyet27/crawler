from bs4 import BeautifulSoup
import requests
import os.path
from os import path
import re

#hàm filter
def not_relative_url(href):
    return re.compile('^/c').search(href) is  not  None

#hàm lấy danh sách tất cả các chapter
def chapter_list():
    mainpageURL="https://blogtruyen.com/139/one-piece"
    chapterlist = {}
    response = requests.get(mainpageURL)
    parsed_html = BeautifulSoup(response.text,'html.parser')
    option_select = parsed_html.find("div", class_ = "list-wrap", id="list-chapters" ).find_all('a',href=not_relative_url)
    if option_select is not None:
        for chapter in option_select:
            link_chapter=chapter.get('href')
            title_chapter=chapter.get('title')

            #Lưu dữ liệu và định dạng lại nó
            chapterlist.update({title_chapter.upper():"https://blogtruyen.com"+link_chapter})
    else:
        print ("Cannot find manga list")
    return chapterlist

#hàm download 1 link ảnh
def download_Image(link,count,name_chapter):
        req = requests.get(link, stream=True)

        #mở thư mục name_chapter và tạo file count.jpg
        with open(name_chapter+'/'+str(count)+ '.jpg','wb') as fd:
            for chunk in req.iter_content():
                fd.write(chunk)
                #hàm download toàn bộ ảnh trong 1 chap
def download_chapter(name_chapter,list_chapter):
    response = requests.get(list_chapter[name_chapter])
    soup = BeautifulSoup(response.text)
    links = soup.find('section').find('article', id='content').find_all('img')
    count=0

    #tạo thư mục
    if not path.exists(name_chapter):
        os.mkdir(name_chapter)

    for link in links:
        link_download=link.get('src')
        count+= 1
        download_Image(link_download,count,name_chapter)
    print("Complete Download "+name_chapter)

#khởi tạo danh sách thông tin các chapter
DS_chapter=chapter_list()

print("SCRIPT DOWNLOAD TRUYEN TRANH ONEPIECE TU BLOGTRUYEN.COM")
print("TONG HOP CAC CHAP TRUYEN: "+str(len(DS_chapter)))
print("\nNHAN SO 1 DE DOWNLOAD CHAP TUY CHON")
print("NHAN SO 2 DE DOWNLOAD HET CAC CHAP")
print("\nNHAN SO 0 DE THOAT")

value=int(input())
if value==0:
    exit
elif value==1:
    print("\nNHAP CHAP BAN MUON DOWNLOAD")
    value_one=input()
    name_chapter="ONE PIECE CHAP "+value_one
    if name_chapter in DS_chapter:
         download_chapter(name_chapter,DS_chapter)
    else:
         print("CHAP CHUA RA HOAC BI LOI ROI BAN OI!!!")
elif  value==2:
    for name_chapter in DS_chapter:
        download_chapter(name_chapter,DS_chapter)
else:
    print("BAN NHAP CHUA HOP LE!!!")
