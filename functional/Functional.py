
# coding: utf-8

# In[]:


import requests
from bs4 import BeautifulSoup
import os
def get_soup(url):
    r = requests.get(url).text
    soup = BeautifulSoup(r,'lxml')
    return soup
def saving_img(url,year_title,title):
    file_name = img_url_thumbnail.split('/')[-1].split('_')[-1]
    img_url_real = '/'.join(img_url_thumbnail.split('/')[:-1] + [img_url_thumbnail.split('/')[-1].split('_')[-1]])
    img_source = requests.get(img_url_real).content
    f = open(year_title+'/'+title+'/'+ file_name,'wb')
    f.write(img_source)
    f.close()

home_page_url = 'http://taylorpictures.net/'
initial_url = 'http://taylorpictures.net/index.php?cat=3'
initial_page_soup = get_soup(initial_url)
cats = initial_page_soup.find('div',{'class':'spec'}).find_all('span',{'class':'catlink'})
i = 0
# 进入 catalog 找 album
for each_cat in cats:
    page_url = home_page_url + each_cat.find('a')['href']
    year_title = str(each_cat.find('a').text)
    os.mkdir(year_title)
    page_soup = get_soup(page_url)
    albums = page_soup.find('div',{'class':'spec'}).find_all('a',{'class':'albums'})
    # 进入 album 找 thumbnail
    for each_album in albums:
        album_url = home_page_url + each_album['href']
        album_soup = get_soup(album_url)
        title = str(album_soup.find('h2').text)
        os.mkdir(year_title+'/'+title)
        album_link = album_soup.find('div',{'class':'spec'}).find_all('img',{'class':'image thumbnail'})
        for album_img_link in album_link:
            #if album_img_link['src'] != None:      # 不必再进行判断 已经存在
            img_url_thumbnail = home_page_url + album_img_link['src']
            file_name = img_url_thumbnail.split('/')[-1].split('_')[-1]
            img_url_real = '/'.join(img_url_thumbnail.split('/')[:-1] + [img_url_thumbnail.split('/')[-1].split('_')[-1]])
            saving_img(img_url_real,year_title,title)
            i = i + 1
            print('爬取第%d张图' %i)

