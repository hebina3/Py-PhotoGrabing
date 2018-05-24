
# coding: utf-8

# In[3]:


import requests
from bs4 import BeautifulSoup
import os

home_page_url = 'http://taylorpictures.net/'
initial_url = 'http://taylorpictures.net/index.php?cat=3'
initial_request = requests.get(initial_url)
initial_page_source = initial_request.text
initial_page_soup = BeautifulSoup(initial_page_source,'lxml')
cats = initial_page_soup.find('div',{'class':'spec'}).find_all('span',{'class':'catlink'})
i = 0
# 进入 catalog 找 album
for each_cat in cats:
    page_url = home_page_url + each_cat.find('a')['href']
    year_title = str(each_cat.find('a').text)
    os.mkdir(year_title)
    page_source = requests.get(page_url).text
    page_soup = BeautifulSoup(page_source,'lxml')
    albums = page_soup.find('div',{'class':'spec'}).find_all('a',{'class':'albums'})
    # 找到 album
    # 进入 album 找 thumbnails
    for each_album in albums:
        album_url = home_page_url + each_album['href']
        album_source = requests.get(album_url).text
        album_soup = BeautifulSoup(album_source,'lxml')
        title = album_soup.find('h2').text
        os.mkdir(year_title+'/'+title)
        album_link = album_soup.find('div',{'class':'spec'}).find_all('img',{'class':'image thumbnail'})
        for album_img_link in album_link:
            img_url_thumbnail = home_page_url + album_img_link['src']
            file_name = img_url_thumbnail.split('/')[-1].split('_')[-1]
            img_url_real = '/'.join(img_url_thumbnail.split('/')[:-1] + [img_url_thumbnail.split('/')[-1].split('_')[-1]])
            img_source = requests.get(img_url_real).content
            f = open(year_title+'/'+title+'/'+ file_name,'wb')
            f.write(img_source)
            f.close()
            i = i + 1
            print('爬取第%d张图' %i)

