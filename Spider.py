# -*- coding: UTF-8 -*-
import re
import os
import requests
import urllib
import time
import sys
from docx import Document
from bs4 import BeautifulSoup
     
        
class WenShu:
    def __init__(self):
        self.index = 1
        #self.user_agent = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
        #self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self.headers = {'User-Agent':self.user_agent, 'Connection':'close'}
        self.search_criteria = ''
        self.download_conditions = ''
        self.item_in_page = '20'
        self.total_items = ''
        self.doc_content = ''
        self.case = {}
        self.search_url = 'http://wenshu.court.gov.cn/List/ListContent'
        self.download_url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateListDocZip.aspx?action=1'
        self.data = {'Param':self.search_criteria,\
                     'Index': self.index,\
                     'Page':self.item_in_page,\
                     'Order':'法院层级',\
                     'Direction':'asc'}


    def _handleValidateCode(self):
        input("Refresh the Page and Enter:")
               
                     
    def setSearchCriteria(self, search_criteria):
        self.search_criteria = search_criteria
        self.data = {'Param':self.search_criteria,\
                     'Index': self.index,\
                     'Page':self.item_in_page,\
                     'Order':'法院层级',\
                     'Direction':'asc'}


    def setDownloadConditions(self):
        self.download_conditions = self.search_criteria.replace(':', '为').replace(',', '且')


    def downloadDocument(self, path, name, id, date):
        docIds = id + '|' + name + '|' + date
        condition = urllib.parse.quote(self.download_conditions)
        data = {'conditions':condition,'docIds':docIds,'keyCode':''}
        #proxies = {"http":"http://218.64.92.190:808"}
        print("Downloading case %s"%(name))
        #r = requests.post(self.download_url, headers = self.headers, data = data, proxies=proxies)
        r = requests.post(self.download_url, headers = self.headers, data = data)
        if r.status_code != 200: 
            print(r.status_code)
        else:
            self.doc_content = r.content
            
            
    def getTotalItemNumber(self):
        attempts = 0
        pattern = re.compile('"Count":"([0-9]+)"', re.S)
        while attempts < 10:
            if attempts > 6:
                self._handleValidateCode()
 
            r = requests.post(self.search_url, headers=self.headers, data=self.data)
            try:
                raw = r.json()
                total_number = re.findall(pattern, raw)
                if total_number:
                    if int(total_number[0]) == 0:
                        print("total number is 0")
                        print("attempts %s" % attempts)
                    else:
                        self.total_items = int(total_number[0]) if total_number else 0
                        break
            except:
                print('Exception catch, re-send request.')    
                    
            attempts += 1
            
            
    def getCaseList(self, start_items, total_items):
        name_list = []
        date_list = []
        id_list = []
        case_id_list = []
        brief_list = []
        procedure_list = []
        court_list = []
        max_page = (total_items // int(self.item_in_page)) + 1
        pattern_name = re.compile('"案件名称":"(.*?)"', re.S)
        pattern_id = re.compile('"文书ID":"(.*?)"', re.S)
        pattern_date = re.compile('"裁判日期":"(.*?)"', re.S)
        pattern_case_id = re.compile('"案号":"(.*?)"', re.S)
        pattern_brief = re.compile('"裁判要旨段原文":"(.*?)"', re.S)
        pattern_procedure = re.compile('"审判程序":"(.*?)"', re.S)
        pattern_court = re.compile('"法院名称":"(.*?)"', re.S)
            
        for index in range(1, max_page + 1):
        #for index in range(1, 3):
            attempts = 0
            while attempts < 10:
                if attempts > 6:
                    self._handleValidateCode()
                 
                print("Get Case list on page %s" % index)
                print("retry %s" % attempts)
                self.data['Index'] = index
                r = requests.post(self.search_url, headers=self.headers, data=self.data)
                try:
                    raw = r.json()
                    if not re.findall(pattern_name, raw):
                        print(raw)
                    else:
                        break
                except:
                    print('Exception catch, re-send request.')
                attempts += 1
            
            name_list += re.findall(pattern_name, raw)
            id_list += re.findall(pattern_id, raw)
            date_list += re.findall(pattern_date,raw)
            case_id_list += re.findall(pattern_case_id, raw)
            brief_list += re.findall(pattern_brief, raw)
            procedure_list += re.findall(pattern_procedure, raw)
            court_list +=  re.findall(pattern_court, raw)
            time.sleep(1)
            #print(case_id_list)
        self.case['name'] = name_list
        self.case['doc_id'] = id_list
        self.case['date'] = date_list
        self.case['case_id'] = case_id_list
        self.case['brief'] = brief_list
        self.case['procedure'] = procedure_list
        self.case['court'] = court_list
