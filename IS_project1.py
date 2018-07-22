# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 21:04:54 2018

@author: qyjbo
"""

# -*- coding: UTF-8 -*-

  
import io  
import sys  
import requests
#reload(sys)  
import chardet 
import jieba
#爬虫之网页信息抓取  
#需要的函数方法：urllib,re,urllib2  
  
import urllib.request

import re  
  
#测试函数->读取  
#def test():  
#     f=urllib.urlopen('http://www.baidu.com')  
#     while True:  
#          firstLine=f.readline()  
#          print firstLine  
  
  
  
#针对于百度贴吧获取前十页楼主小说文本内容  
from    bs4 import  BeautifulSoup as sp
import datetime
import random
random.seed(datetime.datetime.now())
import os
stopwords_path = './stop_word.txt'
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def nltkclearText(text):
    stemmer = PorterStemmer() 
    tokens = [t for t in text.split()] 
    cleantext=[]
    sr = stopwords.words('english') 
    for token in tokens: 
        if token not in sr:
            #print(token)
            token=stemmer.stem(token)
            cleantext+= token+" "
            
    return(''.join(cleantext))

def jiebaclearText(text):
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr="/ ".join(seg_list)
    f_stop = open(stopwords_path)
    try:
        f_stop_text = f_stop.read( )
        #f_stop_text=f_stop_text.decode('utf-8')
    finally:
        f_stop.close( )
    f_stop_seg_list=f_stop_text.split('\n')
    for myword in liststr.split('/'):
        if not(myword.strip() in f_stop_seg_list) and len(myword.strip())>1:
            mywordlist.append(myword)
    return ''.join(mywordlist)
class BDTB:  
     def __init__(self,baseUrl,seeLZ):  
          #成员变量  
          self.baseURL=baseUrl  
          self.seeLZ='?see_lz='+str(seeLZ)  
  
     #获取该页帖子的代码  
     def getPage(self,pageNum):  
          try:  
                   url=self.baseURL+'?pn='+str(pageNum)  
                   #创建request对象  
                   page = urllib.request.urlopen(url)
               html = page.read()
               #html = html.decode("utf-8")
               #print 'URL:'+url  
               return html
          except Exception as e:
               print(e)  
                 
     #匹配标题  
     def Title(self):  
          html=self.getPage(1)  
          #compile提高正则匹配效率  
          reg=re.compile(r'<title>(.*?)。')  
          #返回list列表  
          items=re.findall(reg,html.decode('utf-8'))  
          f=open('output.txt','w+')  
          item=('').join(items)  
          f.write('\t\t\t\t\t'+item)  
          f.close()  
  
     #匹配正文  
     def Text(self,pageNum):
          html=self.getPage(pageNum)  
          #compile提高正则匹配效率  
          reg=re.compile(r'"d_post_content j_d_post_content ">(.*?)</div>')  
          #返回list列表  
          items=re.findall(reg,html.decode('utf-8'))
          filepath='C:/Users/qyjbo/Desktop/Web_Chinese/'
          f=open(filepath+str(pageNum)+'.txt','w',encoding='gb18030')  
          #[1:]切片，第一个元素不需要，去掉。  
          for i in items[1:]:  
               #超链接去除  
               removeAddr=re.compile('<a.*?>|</a>')  
               #用""替换  
               i=re.sub(removeAddr,"",i)  
               #<br>去除  
               i=i.replace('<br>','')                
               f.write('\n\n'+i)  
          f.close()  
  
     def getLinks(articleUrl,pageNum):
          page=requests.get("http://en.wikipedia.org"+articleUrl,timeout=5)
          html=page.content
          html=html.decode('utf-8')
          bsObj=sp(html,"html.parser")
          info=bsObj.find("div",{"class":"mw-parser-output"})
          Filter ={'script','nonscipt','style'}
          for items in Filter:
              for va in info.find_all(items):
                  va.decompose;
          filepath='C:/Users/qyjbo/Desktop/Web_English/'
          f=open(filepath+str(pageNum)+'.txt','w',encoding='gb18030')  
          f.write(info.get_text())
          return bsObj.find("div",{"id":"bodyContent"}).findAll("a",href=re.compile("^(/wiki/)((?!:).)*$"))

         
         
#调用入口  
if __name__ == '__main__':
    baseURL='https://tieba.baidu.com/p/5663710766'  
    bdtb=BDTB(baseURL,1)  
    print ('爬虫正在启动....')  
#多页  
    #bdtb.Title() 
    #print('抓取标题完毕！')  
    #for i in range(501,501):  
     #print('正在抓取第%02d页'%i)  
     #bdtb.Text(i)  
     #print('抓取正文完毕!') 
    '''
    links=BDTB.getLinks("/wiki/LOL",0)
    pageNum=1
    while  len(links)>0:
         newArticle=links[random.randint(0,len(links)-1)].attrs["href"]
         links=BDTB.getLinks(newArticle,pageNum)
         pageNum=pageNum+1
     
    chinesebase="C:/Users/qyjbo/Desktop/Web_Chinese/"
    englishbase="C:/Users/qyjbo/Desktop/Web_English/"
    files= os.listdir(chinesebase) #得到文件夹下的所有文件名称  
    Num=0
    newcpath="C:/Users/qyjbo/Desktop/Web_Chinese/changed/"
    for file in files: #遍历文件夹
       f=open('C:/Users/qyjbo/Desktop/Web_Chinese/'+file,'r',encoding='gb18030')
       for rs in f.readlines():
           temp = re.sub("[A-Za-z0-9\<\"\_\/\.\>\?\=\:\!\%\[\]\,\。]", "", rs)
           print(temp)
           j=open(newcpath+str(Num)+'.txt','a+',encoding='gb18030')
           j.writelines('\n'+temp)
           
       Num=Num+1
       j.close()
       
    changebase="C:/Users/qyjbo/Desktop/Web_Chinese/changed/"
    jiebabase="C:/Users/qyjbo/Desktop/Web_Chinese/jieba/"
    files= os.listdir(changebase)
    Num=0
    for file in files:
        f=open(changebase+file,'r',encoding='gb18030')
        for rs in f.readlines():
            new_line=jiebaclearText(rs)
            j=open(jiebabase+str(Num)+'.txt','a+',encoding='gb18030')
            j.writelines('\n'+new_line)
        Num=Num+1
        j.close()
        '''
    englishbase="C:/Users/qyjbo/Desktop/Web_English/"
    englishfinalbase="C:/Users/qyjbo/Desktop/Web_English/final/"
    files= os.listdir(englishbase)
    files= os.listdir(englishbase)
    Num=0
    for file in files:
        f=open(englishbase+file,'r',encoding='gb18030')
        for rs in f.readlines():
            #print(rs)
            new_line=nltkclearText(rs)
            j=open(englishfinalbase+str(Num)+'.txt','a+',encoding='gb18030')
            j.writelines('\n'+new_line)
        Num=Num+1
        j.close()
            
    
                
       
        