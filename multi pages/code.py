
# coding: utf-8

# In[ ]:


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
    
    
    # 进入 album 找 display
    for each_album in albums:
        album_url = home_page_url + each_album['href']
        album_source = requests.get(album_url).text
        album_soup = BeautifulSoup(album_source,'lxml')
        title = str(album_soup.find('h2').text)
        album_link = album_soup.find('div',{'class':'spec'}).find_all('td',{'class':'thumbnails'})
        os.mkdir(year_title+'/'+title)
        
        # 进入 display 找 img
        for displays in album_link:
            if displays.find('a') != None:
                display_links = home_page_url + displays.find('a')['href']
                img_source = requests.get(display_links).text
                img_soup = BeautifulSoup(img_source,'lxml')
                img_link = img_soup.find('div',{'class':'spec'}).find_all('td',{'style':'{SLIDESHOW_STYLE}'})
                for img_link_url in img_link:
                    if img_link_url.find('a') != None:
                        img_url_normal = home_page_url + img_link_url.find('a').find('img')['src']
                        file_name = img_url_normal.split('/')[-1].split('_')[-1]
                        img_url_real = '/'.join(img_url_normal.split('/')[:-1] + [img_url_normal.split('/')[-1].split('_')[-1]])
                        img_source = requests.get(img_url_real).content
                        f = open(year_title+'/'+title+'/'+ file_name,'wb')
                        f.write(img_source)
                        f.close()
                        i = i + 1
                        print('爬取第%d张图' %i)

