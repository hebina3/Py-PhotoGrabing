
# coding: utf-8

# In[4]:


# 先导入 requests 库来获取请求
import requests

# 导入 beautifulsoup 库  作用相当于理清页面结构
from bs4 import BeautifulSoup

# 导入 os （operating system）库来获取对文件和文件夹的操作
import os

# 获取 url 指向
initial_url = 'http://www.gakky.me/6155.html'

# 当网页有反爬时和防盗链时 需要在 headers 中添加相关属性 使用字典传值
# headers = {'Referer':'http://www.gakky.me/6155.html','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'}

# 获取该 url 的源码  备注 ：  .text = 源码（网页）  .content = 二进制（图片、文件）
initial_request = requests.get(initial_url)
initial_pagesource = initial_request.text

# 利用 beautifulsoup 来网页源码进行解析
page_soup = BeautifulSoup(initial_pagesource,'lxml')

# 找到目标标签 img
imgs = page_soup.find('div',{'class':'entry-content'}).find_all('img')

# 找到目标标签 title 并取 title 的文本信息用于创建目录使用
title = page_soup.find('title').text

# 创建目录
os.mkdir(title)

# 循环抓取
for img in imgs:
    # 这个url 目前就是一个字符串 ''
    url = img['src']   
    # 将 url 进行拆分 拆分依据 '/' 遇到 '/' 拆
    file_name = url.split('/')[-1]
    # 获取图片的二进制编码
    img_source = requests.get(url).content
    # 向路径中写入图片
    f = open(title+'\\'+file_name,'wb')
    f.write(img_source)
    f.close()

