# -*- coding: UTF-8 -*-
import re
import os
import requests
import urllib
import time
import sys
from docx import Document
from bs4 import BeautifulSoup

class DocAnalyser:
    def __init__(self):
        self.content = ''
        self.bhr_list = []
        self.zdbhr_list = []
        self.bgr_list = []
    
    def analyseDoc(self, name):
        self.readDoc(name)
        self.getWeituoBianhuren()
        self.getZhidingBianhuren()
        self.getBeigaoren()
        self.getGroupBianhuren()
        
    def readDoc(self, doc_name):
        try:
            document = Document(doc_name) if doc_name else sys.exit(0)
        except:
            print("Document %s is invalid" % doc_name)
            
    #   读取每段资料
        l = [paragraph.text for paragraph in document.paragraphs]
        s = ''.join(str(e) for e in l)
        self.content = s

    #取得委托辩护人姓名
    def getWeituoBianhuren(self):
        #print(self.content)
        bhr_list = re.findall('(?<!指定)辩护人\w{2,4}，\w+律师', self.content)
        for i in range(len(bhr_list)):
            bhr = re.search('辩护人\w{2,4}(?=，)', bhr_list[i])
            bhr_list[i] = bhr.group()
        print('委托辩护人  %s'%bhr_list)


    def getZhidingBianhuren(self):
        zdbhr_list = re.findall('指定辩护人\w{2,4}，\w+律师', self.content)
        for i in range(len(zdbhr_list)):
            zdbhr = re.search('指定辩护人\w{2,4}(?=，)', zdbhr_list[i])
            zdbhr_list[i] = zdbhr.group()
        print('指定辩护人  %s'%zdbhr_list)

        
    def getBeigaoren(self):
        bgr_list = re.findall('被告人）?\w{2,4}，[男|女|别]', self.content)
        for i in range(len(bgr_list)):
            bgr = re.search('被告人）?\w{2,4}(?=，)', bgr_list[i])
            bgr_list[i] = bgr.group().replace('）', '')
        print('被告人  %s'%bgr_list)
        
    def getGroupBianhuren(self):    
        gbhr = re.findall('(辩护人\w{2,4}，\w+律师.{1,3}辩护人\w{2,4}，\w+律师)', self.content)
        print(gbhr)
        
        
class WenShu:
    def __init__(self):
        self.index = 1
        #self.user_agent = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36'
        #self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self.headers = {'User-Agent':self.user_agent }
        self.search_criteria = ''
        self.download_conditions = ''
        self.item_in_page = '20'
        self.total_items = ''
        self.case = {}
        self.search_url = 'http://wenshu.court.gov.cn/List/ListContent'
        self.download_url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateListDocZip.aspx?action=1'
        self.data = {'Param':self.search_criteria,\
                     'Index': self.index,\
                     'Page':self.item_in_page,\
                     'Order':'法院层级',\
                     'Direction':'asc'}


    def setSearchCriteria(self, search_criteria):
        self.search_criteria = search_criteria
        self.data = {'Param':self.search_criteria,\
                     'Index': self.index,\
                     'Page':self.item_in_page,\
                     'Order':'法院层级',\
                     'Direction':'asc'}


    def setDownloadConditions(self):
        self.download_conditions = self.search_criteria.replace(':', '为').replace(',', '且')


    def getContent(self, maxPage):
        for index in range(1, maxPage+1):
            print("Page %s" % index)
            self.LoadPageContent(index)
            self.downloadDocument()
            p = [self.date, self.case_id, self.title, self.doc_id, self.brief, self.procedure, self.court]
            with open('results.csv', 'a') as f:
                f.write(codecs.BOM_UTF8)
                writer = csv.writer(f)
                for item in zip(*p):
                    writer.writerow(item)

                    
    def downloadDocument(self, path, name, id, date):
        docIds = id + '|' + name + '|' + date
        condition = urllib.parse.quote(self.download_conditions)
        data = {'conditions':condition,'docIds':docIds,'keyCode':''}
        ####################################
        proxies = {"http":"http://119.5.1.6:808"}
        #proxy_support = requests.ProxyHandler(proxy)
        #opener = requests.build_opener(proxy_support)
        #opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
        #requests.install_opener(opener)
        ####################################
        #with requests.Session() as s:
        #    r = s.post(self.download_url, headers = self.headers, data = data)
        print("Downloading case %s"%(name))
        #r = requests.post(self.download_url, headers = self.headers, data = data, proxies=proxies)
        r = requests.post(self.download_url, headers = self.headers, data = data)
        if r.status_code != 200: 
            print(r.status_code)
        else:
            with open(path + name + date + ".txt", "wb") as word_doc:
                word_doc.write(r.content)
            
    def getTotalItemNumber(self):
        #print(self.data)
        r = requests.post(self.search_url, headers=self.headers, data=self.data)
        raw = r.json()
        if raw == 'remind':
            self.handleValidateCode()
            # re-send requests
            r = requests.post(self.search_url, headers=self.headers, data=self.data)
            raw = r.json()
        pattern = re.compile('"Count":"([0-9]+)"', re.S)
        total_number = re.findall(pattern, raw)
        self.total_items = int(total_number[0]) if total_number else 0
    
    def getCaseList(self, start_items, total_items):
        name_list = []
        date_list = []
        id_list = []
        case_id_list = []
        case_brief_list = []
        max_page = (total_items // int(self.item_in_page)) + 1
        #start_page = (start_items // int(self.item_in_page)) + 1
        #print('Get case info from %s to %s'%(start_page, max_page))
        #sys.exit(0)
        for index in range(1, max_page + 1):
        #for index in range(1, 3):
            print("Get Case list on page %s" % index)
            self.data['Index'] = index
            #print(self.data)
            r = requests.post(self.search_url, headers=self.headers, data=self.data)
            try:
                raw = r.json()
                #print(raw)
            except:
                print('exception catch, re-send request.')
                self.handleValidateCode()
                r = requests.post(self.search_url, headers=self.headers, data=self.data)
                raw = r.json()
            if raw == 'remind':
                self.handleValidateCode()
                # If blocked by website, hold and refresh manually, and then re-send requests
                r = requests.post(self.search_url, headers=self.headers, data=self.data)
                raw = r.json()
            pattern_name = re.compile('"案件名称":"(.*?)"', re.S)
            pattern_id = re.compile('"文书ID":"(.*?)"', re.S)
            pattern_date = re.compile('"裁判日期":"(.*?)"', re.S)
            pattern_case_id = re.compile('"案号":"(.*?)"', re.S)
            pattern_brief = re.compile('"裁判要旨段原文":"(.*?)"', re.S)
            name_list += re.findall(pattern_name, raw)
            id_list += re.findall(pattern_id, raw)
            date_list += re.findall(pattern_date,raw)
            case_id_list += re.findall(pattern_case_id, raw)
            case_brief_list += re.findall(pattern_brief, raw)
            time.sleep(1)
            #print(case_id_list)
        self.case['name'] = name_list
        self.case['doc_id'] = id_list
        self.case['date'] = date_list
        self.case['case_id'] = case_id_list
        self.case['brief'] = case_brief_list

        
    def getHomePage(self, url):
        res = requests.get(url)
        res.encoding = 'utf-8'
        print(res.text)
    
    def handleValidateCode(self):
        input("Refresh the Page and Enter:")
    
    
    def LoadPageContent(self, index):
        #记录开始时间
        begin_time = datetime.datetime.now()
        url = 'http://wenshu.court.gov.cn/List/ListContent'
        self.data['Index'] = index
        r = requests.post(url, headers = self.headers, data = self.data)
        raw=r.json()

        pattern1 = re.compile('"裁判日期":"(.*?)"', re.S)
        self.date = re.findall(pattern1,raw.encode("utf-8"))
        
        pattern2 = re.compile('"案号":"(.*?)"', re.S)
        self.case_id = re.findall(pattern2,raw.encode("utf-8"))
        
        pattern3 = re.compile('"案件名称":"(.*?)"', re.S)
        self.title = re.findall(pattern3,raw.encode("utf-8"))
        
        pattern4 = re.compile('"文书ID":"(.*?)"', re.S)
        self.doc_id = re.findall(pattern4,raw.encode("utf-8"))
        
        pattern5 = re.compile('"裁判要旨段原文":"(.*?)"', re.S)
        self.brief = re.findall(pattern5,raw.encode("utf-8"))
        
        pattern6 = re.compile('"审判程序":"(.*?)"', re.S)
        self.procedure = re.findall(pattern6,raw.encode("utf-8"))
        
        pattern7 = re.compile('"法院名称":"(.*?)"', re.S)
        self.court = re.findall(pattern7,raw.encode("utf-8"))

