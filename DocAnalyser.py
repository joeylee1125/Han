# -*- coding: UTF-8 -*-
import re
import sys
import os
import time
import csv
import argparse
import codecs

from shutil import copyfile
from docx import Document

class DocAnalyser:
    def __init__(self):
        self.content = ''
        self.wtbhr_list = []
        self.zdbhr_list = []
        self.bgr_list = []
        self.sws_list = []
        self.procedure = []
        self.hyt = []
        self.bhrt = ''
        self.bgrt = ''
        
        
    def read_doc(self, doc_name):
        try:
            document = Document(doc_name) if doc_name else sys.exit(0)
        except:
            print("Document %s is invalid" % doc_name)
            
        #   读取每段资料
        l = [paragraph.text for paragraph in document.paragraphs]
        self.content = ''.join(str(e) for e in l)
    

        
    #取得委托辩护人姓名
    def get_wtbhr(self):
        bhr_list = re.findall('(?<!指定)辩护人\：?\w{2,4}，.*?律师', self.content)
        for i in range(len(bhr_list)):
            bhr = re.search('辩护人\：?\w{2,4}(?=，)', bhr_list[i])
            bhr_list[i] = bhr.group()
        self.bhr_list = bhr_list    


    #取得指定辩护人姓名
    def get_zdbhr(self):
        zdbhr_list = re.findall('指定辩护人\w{2,4}，.*?律师', self.content)
        for i in range(len(zdbhr_list)):
            zdbhr = re.search('指定辩护人\w{2,4}(?=，)', zdbhr_list[i])
            zdbhr_list[i] = zdbhr.group()
        self.zdbhr_list = zdbhr_list
        
        
    #取得被告人姓名    
    def get_bgr(self):
        bgr_list = re.findall('被告人）?\w{2,4}，.?[曾|男|女|别]', self.content)
        for i in range(len(bgr_list)):
            bgr = re.search('被告人）?\w{2,4}(?=，)', bgr_list[i])
            bgr_list[i] = bgr.group().replace('）', '')
        self.bgr_list = bgr_list


    #取得事务所名字
    def get_sws(self):    
        sws_list = re.findall('(?<=辩护人).*?事务所律师', self.content)
    
        for i in range(len(sws_list)):
            sws = re.search('(?<=，).*事务所', sws_list[i])
            sws_list[i] = sws.group()
        self.sws_list = sws_list

    
    
    #取得一组辩护人姓名
    def get_group_bhr(self):    
        self.gbhr = re.findall('(辩护人\w{2,4}，.*?律师.*?辩护人\w{2,4}，.*?律师)', self.content)
        
    
    def get_procedure(self):    
        self.procedure = re.findall('\w\w程序', self.content)
        
        
    def get_hyt(self):    
        self.hyt = re.findall('合议庭', self.content)
    
    
    def bhr_test(self):    
        self.bhrt = re.search('辩护人', self.content)
        
        
        
    def bgr_test(self):    
        self.bgrt = re.search('被告人', self.content)
        