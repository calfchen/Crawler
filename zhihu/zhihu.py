# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 16:23:33 2017

@author: chenx
"""

import requests
from bs4 import BeautifulSoup
import re
from requests.exceptions import RequestException
import os
from hashlib import md5

kv = {'user-agent' : 'Mozilla/5.0'}

count = 0

#获取相关话题的内容
def getHTMLText(url, kv):
    try:
        r = requests.get(url, headers = kv,timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print(r.status_code)
        return "爬取话题失败"
    
#获得相关话题的问题链接
def getTopicLink(text):
    soup = BeautifulSoup(text,"lxml")
    questionLink = []
    for link in soup.find_all('a'):
        if re.match(r'/question/\d{8}',str(link.get('href'))):
            questionLink.append("https://www.zhihu.com" + link.get('href')[0:18])
    
    questionLink = list(set(questionLink))
    return questionLink
        

#得到相关问题的内容
def getQuestionText(url):
    try:
        r = requests.get(url, headers = kv,timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print(r.status_code)
        return "爬取回答失败"

def save_image(content):
    global count
    count += 1
    file_path = '{0}/{1}.{2}'.format(os.getcwd(),count,'jpg')
    if file_path[-6:] != "hd.jpg" :
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()
            print('下载成功')

def download_image(url):
    print('正在下载',url)
    try:
        response = requests.get(url)  
        if response.status_code == 200:
            save_image(response.content)
            #return response.text
        return None
    except RequestException:
        print('请求图片出错',url)
        return None
    
    

#得到相关问题的图片链接
def getQuestionLink(text):
    soup = BeautifulSoup(text,"lxml")
    images_pattern = re.compile(r'https://pic\d.zhimg.com/[a-fA-F0-9]{5,32}_\w+.(?:png|jpg|jpeg)')
    pictureUrlList = images_pattern.findall(text)
        
    for pictureUrl in pictureUrlList:
        download_image(pictureUrl)


if __name__ == '__main__':
    keyword = "街拍"
    url = "https://www.zhihu.com/search?type=content&q=" + keyword
    
    text = getHTMLText(url, kv)
    questionLink = getTopicLink(text)
    
    for perURL in questionLink:
        perText = getQuestionText(perURL)       
        getQuestionLink(perText)
    
    
    
    
    
    
    