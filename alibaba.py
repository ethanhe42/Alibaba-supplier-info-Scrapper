#encoding:utf-8
from __future__ import print_function

""" Note:
login alibaba is not necessary


"""
developerInfo="\n-------------------------------------\n"\
              "Developed by Yihui He\n" \
              "QQ:      535505132\n" \
              "Weixin:  he535505132\n" \
              "Email:   rex686568@outlook.com\n" \
              "find me: zhihu.com/people/rex686568\n" \
              "-------------------------------------\n"

debug=False
totxt=False

from selenium import webdriver
import selenium.common.exceptions
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.keys import Keys
import time
# from BeautifulSoup import *
# from urlparse import urljoin
# import sys
# import chardet
# import re
# from sqlite3 import dbapi2 as sqlite
# import urllib2
# import sys  
# from lxml import html
import random
import pandas as pd
# import numpy as np
import os


# from PyQt4.QtGui import *
# from PyQt4.QtCore import *
# from PyQt4.QtWebKit import *
#import PyQt4






# def fetch(line=searchPage,
#     D=False):
#     #chardet 需要下载安装
#
#     import chardet
#     #抓取网页html
#     html_1 = urllib2.urlopen(line,timeout=120).read()
#     infoencode = chardet.detect(html_1).get('encoding','utf-8')
#     ##通过第3方模块来自动提取网页的编码
#
#     #print html_1
#
#     encoding_dict = chardet.detect(html_1)
#     #print encoding
#     web_encoding = encoding_dict['encoding']
#     if web_encoding == 'utf-8' or web_encoding == 'UTF-8':
#         html = html_1
#     else :
#         html = html_1.decode('gbk','ignore').encode('utf-8')
#     if D:
#         print html
#     return html

def getAttr(browser):
    props=[]
    
    
    shortlists=browser.\
    find_elements_by_class_name('cd')
    # print shortlists[0].get_attribute('href')

    for item in shortlists:
        props.append(item.get_attribute('href'))
    
    # zz=browser.find_element_by_class_name('zz-site-tbl')
    # for i in zz.find_elements_by_tag_name('span'):
    #     props.append(i.text)
        
        
    # lists=browser.find_elements_by_class_name('report_list')
    
    # for i in range(len(lists)-5,len(lists)):
    #     props.append(lists[i].find_element_by_tag_name('div').text.strip(' '))

    
    return props

def inp2keyword(inp):
    words=inp.split()
    key=""
    for i in range(len(words)):
        key+=words[i]
        if i == len(words)-1:
            break
        key+="_"
    return key

def composeURL(page,keyword):
    if page == 1:
        return 'http://www.alibaba.com/corporations/'+keyword+'/--------------------50.html'
    return 'http://www.alibaba.com/corporations/'+keyword+'/--------------------50/'+str(page)+'.html'


def companyList(browser,keyword,startpage=1,maxpage=10000):

    result=[]
    while True:
        url=composeURL(startpage,keyword)
        browser.get(url)
        # waiting until go through anti system
        while True:
            if browser.current_url==url:
                break
            else:
                browser.get(url)
                time.sleep(random.randint(2,4))

        list=getAttr(browser)
        result+=list
        if len(list)==0 or startpage>=maxpage:
            print("found "+str(len(result))+" companys")
         
            dir = os.getcwd()
            dir = os.path.join(dir,keyword)
            if not os.path.exists(dir):
                os.makedirs(dir)
            filename = os.path.join(dir, "company for "+keyword+".txt")
            
            f=open(filename,"w")
            for i in result:
                f.write(i+"\n")

            return result

        startpage+=1



def getContact(browser,
               url):
    #browser=webdriver.Chrome()#to be commented

    title=[]
    data=[]
    props=[]

    #init browser
    try:
        browser.get(url)
    except selenium.common.exceptions.TimeoutException:
        return title,data

    # waiting until go through anti system
    while True:
        if browser.current_url==url:
            break
        else:
            browser.get(url)
            time.sleep(random.randint(2,4))

    #get person name
    try:
        name=browser.find_element_by_class_name("contact-info").find_element_by_class_name("name").text

    except selenium.common.exceptions.NoSuchElementException:
        pass
    else:
        title.append("name")
        data.append(name)

    shortlists=browser.find_elements_by_class_name('dl-horizontal')

    #get person infos
    if len(shortlists)>=1:
        for i in shortlists[0].find_elements_by_tag_name('dt'):
            title.append(i.text)
        for i in shortlists[0].find_elements_by_tag_name('dd'):
            data.append(i.text)

    #get telephones
    if len(shortlists)>=2:
        for i in shortlists[1].find_elements_by_tag_name('dt'):
            title.append(i.text)
        for i in shortlists[1].find_elements_by_tag_name('dd'):
            data.append(i.text)

    #get contact infomation
    if len(shortlists)>=3:
        for i in shortlists[2].find_elements_by_tag_name('dt'):
            title.append(i.text)
        for i in shortlists[2].find_elements_by_tag_name('dd'):
            data.append(i.text)

    #get company info
    try:
        table=browser.find_element_by_class_name("company-contact-information").find_element_by_tag_name("tbody")
    except selenium.common.exceptions.NoSuchElementException:
        pass
    else:
        for i in table.find_elements_by_tag_name("th"):
            title.append(i.text)
        iconflag=True
        for i in table.find_elements_by_tag_name("td"):
            if iconflag:
                iconflag=False
            else:
                data.append(i.text)
                iconflag=True

    #print infos


    if debug:
        print(title)
        print(data)

#    return np.array([title,data]).T
    return title,data


def main():

    inp="SHENZHEN LED DISPLAY"
    page=1
    print(developerInfo)
    print("contacts crawler for alibaba.com")
    inp=raw_input("type keywords below to search contacts(leave blank space between keywords)\n")

    keyword=inp2keyword(inp)
    # print(keyword)
    dir = os.getcwd()
    dir = os.path.join(dir,keyword)

    contNum=0
    if totxt:
        filename = os.path.join(dir, "contacts for "+keyword+".txt")
    else:
        filename= os.path.join(dir,"contacts for "+ keyword+".xlsx")

    if not os.path.exists(os.path.join(dir, "company for "+keyword+".txt")):

        browser = webdriver.Chrome()
        companylist=companyList(browser,
                                keyword,
                                page
                                )#maxpage to be del

        #prepare a file to get each company infos
        if not os.path.exists(dir):
            os.makedirs(dir)

        if totxt:
            f=open(filename,"w")
            f.write(developerInfo)
        else:
            pass

    else:
        f=open(os.path.join(dir, "company for "+keyword+".txt"))
        companylist=[]
        for i in f.readlines():
            companylist.append(i.strip())
        #start from previous work
        contNum=input("enter the number to start from previous work,from 0 to "+str(len(companylist))+"\n")
        contNum=int(contNum)
        print("grabbing contacts websites")
        browser = webdriver.Chrome()


    print("grabbing contacts infos, please leave computer working")
    if totxt:
        f=open(filename,"a+")
    else:
        pass

    df=pd.DataFrame([])
    for cnt in range(contNum,len(companylist)):

        print(str(cnt)+"/"+str(len(companylist)),end='\r')

        if not totxt:
            #write to csv
            idx,data=getContact(browser,companylist[cnt])
            if len(idx)==0:
                continue

            ad=pd.DataFrame(data,idx,columns=[cnt])
            if df.empty:
                df=ad
            else:
                df=df.join(ad,how='outer')
            if (cnt%30 == 0) or (cnt == len(companylist)-1) :
                (df.T).to_excel(filename)

        else:
            #write to txt

            singleContact=getContact(browser,companylist[cnt])
            f.write(str(cnt)+"\n")
            for info in singleContact:
                s=info[0]+" "+info[1]
                f.write(s)
                f.write("\n")

    if totxt:
        f.close()
    browser.close()
    print("done")
#    data.to_csv('urlD.csv',encoding='utf-8',mode='a',header=False)

if __name__ == "__main__":
#    getContact('http://elnor.en.alibaba.com/contactinfo.html')
    
    main()











