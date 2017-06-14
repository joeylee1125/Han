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

import CourtList

class DocAnalyser:
    def __init__(self):
        self.content = ''
        self.doc_name = ''
        self.wtbhr_list = []
        self.zdbhr_list = []
        self.bgr_list = []
        self.sws_list = []
        self.procedure = []
        self.hyt = []
        self.bhr_of_bgr = {}
        self.bhrt = ''
        self.bgrt = ''
        self.gbhr = ''
        self.idt = ''
        #self.bgr_pattern1 = re.compile('被告人）?[^(的|相约)]\w{2,4}[，,（(].{0,10}[曾男女别1-9]')
        #self.bgr_pattern1 = re.compile('被告人）?[^(的|相约)]\w{2,4}[，,（(].{0,10}[曾男女别1-9]')
        #self.bgr_pattern1 = re.compile('被告人）?\w{2,4}[，,（(].{0,10}[曾男女别1-9]')
        #self.bgr_pattern12 = re.compile('被告人\w{2,4}。')
        #self.bgr_pattern13 = re.compile('被告人[）﹒\w]{2,10}[，,（(].{0,10}[曾男女别1-9]')
        #self.bgr_pattern13 = re.compile('被告人[\w]{2,10}[（：），\w]+[曾男女别]')
        #self.bgr_pattern1 = re.compile('被告人\w{2,4}.[曾男女别]')
        #self.bgr_pattern1 = re.compile('被告人\w{2,4}')
        
        self.bgr_pattern2 = re.compile('(?<=被告人)[）﹒\w]{2,15}(?=[。，,（(])')
        self.pj_pattern = re.compile('(判决|判处|决定|判)(结果|如下).*')
        
    def read_doc(self, doc_name):
        try:
            document = Document(doc_name) if doc_name else sys.exit(0)
        except:
            print("Document %s is invalid" % doc_name)
            
        #   读取每段资料
        l = [paragraph.text for paragraph in document.paragraphs]
        self.content = ''.join(str(e) for e in l)
        self.doc_name = doc_name
        
        
    def _get_pj_section(self):
        pj_section = re.search(self.pj_pattern, self.content)
        if pj_section:
            return pj_section.group()
        else:
            #print('判决---------------> NOT FOUND')
            #print(self.content)
            return None
    
    def get_1st_zm(self):
        pj = self._get_pj_section()
        if not pj:
            print('pj is empty')
            return None
        
        zm = re.search('(?<=犯).*?(?=罪)', pj)
        if not zm:
            for g in CourtList.zm_group_list:
                for zp in CourtList.zm_group[g]:
                    if not zm:
                        #print(zp)
                        zm = re.search(zp, pj)
        if zm:
            return zm.group()
        else:
            print('罪名 %s -------------> Not FOUND' % pj)
            return None
        
    #取得委托辩护人姓名
    def get_wtbhr(self):
        bhr_list = re.findall('(?<!指定)辩护人\：?\w{2,4}，.*?律师', self.content)
        for i in range(len(bhr_list)):
            bhr = re.search('辩护人\：?\w{2,4}(?=，)', bhr_list[i])
            bhr_list[i] = bhr.group()
        self.wtbhr_list = bhr_list    
    
    
    def _search_bgr(self, text):
        self.bgr_pattern0 = re.compile('(?<=被告人).+?[，,（(。]')
        bgr_list0 = re.findall(self.bgr_pattern0, text)
        #self.bgr_pattern1 = re.compile('(?<=被告)人?.*?(?=犯)')
        self.bgr_pattern1 = re.compile('(?<=被告人)' + CourtList.last_name + '\w{0,5}(?=[。，,，（(]|201|犯)')
        self.bgr_pattern12 = re.compile('(?<=被告人)' + CourtList.ss_name)
        self.bgr_pattern13 = re.compile('(?<=被告人..情况姓名)' + CourtList.last_name + '\w{0,4}[，（|出生日期|性别]')
        self.bgr_pattern14 = re.compile('(?<=被告人)' + CourtList.last_name + '\w{0,4}成都市')
        self.bgr_pattern15 = re.compile('(?<=被告人姓名)' + CourtList.last_name + '\w{0,4}出生日期')
        self.bgr_pattern16 = re.compile('(?<=被告)人?[：:?]' + CourtList.last_name + '\w{0,4}(?=[。，,，（(]|201)')        
        #self.bgr_pattern17 = re.compile('(?<=被告)' + CourtList.last_name + '\w{0,4}(?=[。，,，（(]|201)')        
        self.bgr_pattern17 = re.compile(CourtList.invalide_name)
        
        bgr_list = re.findall(self.bgr_pattern1, text)
        if not bgr_list:
            bgr_list = re.findall(self.bgr_pattern12, text)
        if not bgr_list:
            bgr_list = re.findall(self.bgr_pattern13, text)
        if not bgr_list:
            bgr_list = re.findall(self.bgr_pattern14, text)
        if not bgr_list:
            bgr_list = re.findall(self.bgr_pattern15, text)
        if not bgr_list:
            bgr_list = re.findall(self.bgr_pattern16, text)
        if not bgr_list:
            bgr_list = re.findall(self.bgr_pattern17, text)
            
            
        if not bgr_list:
            try:
                print(bgr_list0[0])
            except:
                return ''
                
           
            
            print(self.doc_name)
            print(self.content)
            
            sys.exit(0)
        #print(bgr_list[1])
        
        #if not bgr_list:
        #    bgr_list = re.findall(self.bgr_pattern12, text)
        
        #if not bgr_list:
        #    bgr_list = re.findall(self.bgr_pattern13, text)
        
        #print(text)
        #print(bgr_list)
        #for i in range(len(bgr_list)):
        #    print(bgr_list[i])
        
        
        
        
#        for i in range(len(bgr_list)):
            #bgr = re.search(self.bgr_pattern2, bgr_list[i])
            #bgr_list[i] = bgr.group().replace('）', '')
            #if len(bgr.group()) > 3:
            #    print(bgr.group())
            #    print(self.doc_name)
        #print(bgr_list)
        raw_list_c = len(bgr_list)
        if raw_list_c > 1:
            i = 0
            j = 1
            #print(bgr_list)
            #print('')
            while i < j:
                j = i + 1
                while j < raw_list_c:
                    #print('i -> %s, j -> %s,  %s %s raw_list_c -> %s' % (i, j, bgr_list[i], bgr_list[j], raw_list_c))
                    if bgr_list[i] in bgr_list[j]:
                        bgr_list.pop(j)
                        #print(bgr_list)
                        raw_list_c -= 1
                    else:
                        j += 1
                i += 1
        #print(bgr_list[0])
        #print(bgr_list[1])
        #print(bgr_list[2])
        #print('')
        return bgr_list
    
    
    def get_bhr_of_bgr(self, number):
        #print(self.content)
        #print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        #print('')
        first_half = re.search('(?<=公诉).*?(?=公诉)', self.content)
        if not first_half:
            first_half = re.search('(?<=人民检察院).*?(?=经审理查明)', self.content)
        #print(first_half.group())
        bgr_section = re.findall('被告人.*?(?=被告人)', first_half.group() + '被告人')
        #print(bgr_section)
        pj_section = re.search('判决(结果|如下).*', self.content)
        #print(pj_section.group())
        #bhr_list = re.findall(bgr + '.*?辩护人\：?\w{2,4}，.*?事务所律师', self.content)
        #print(first_half.group())
        #print(bgr_section)
        bgr_matrix = {}
        
        bgr_matrix['bgr'] = [''] * len(bgr_section)
        bgr_matrix['bhr'] = [''] * len(bgr_section)
        bgr_matrix['zm'] = [''] * len(bgr_section)
        bgr_matrix['xq'] = [''] * len(bgr_section)
        bgr_matrix['hx'] = [''] * len(bgr_section)
        bgr_matrix['level'] = [''] * len(bgr_section)
        bgr_matrix['cn'] = [number] * len(bgr_section)
        for i, text in enumerate(bgr_section):
            #print(text)
            ###############           bgr               #####################
            #bgr = re.search(self.bgr_pattern1, text)
            #bgr = re.search('被告人）?\w{2,4}()', bgr)
            #if not bgr:
            #    break
            #bgr.group().replace('）', '')
            #bgr = re.search(self.bgr_pattern2, bgr.group()) 
            #print('bgr -----------> %s' % bgr.group())
            
            #bgr_matrix['bgr'][i] = bgr.group()
            bgr_list = self._search_bgr(text)
            if bgr_list:
                bgr_matrix['bgr'][i] = bgr_list[0]
            else:
                break
            #print(bgr_list)
            
            
            ##############           bhr               #########################
            bhr_list = re.findall('辩护人.*事务所律师', text)
            bgr_matrix['bhr'][i] = ''.join(bhr_list)
            ##################      zm         #######################
            #print('pj -----------------> %s'%pj_section.group())
            pj = re.search('被告人' + bgr_list[0] + '.*?。', pj_section.group())
            #print(bgr.group())
            #print('pj -----------------> %s'%pj.group())
            #if not pj:
            #    break
            try:
                zm = re.findall('犯.*?罪', pj.group())
            except AttributeError:
                print('Exception Catch!')
                break
            bgr_matrix['zm'][i] = ''.join(zm)
            #print(pj.group())
            ###############   xq   ######################
            mul_zm = re.search('数罪并罚', pj.group())
            if mul_zm:
                tmp = re.search('(?<=数罪并罚).*', pj.group())
                xq = re.search('(判处|执行).*?(?=[；|，|。])', tmp.group())
            else:
                xq = re.search('判处.*?(?=[；|，|。])', pj.group())
            #print(xq)    
            if not xq:
                xq = re.search('免予刑事处罚', pj.group())
            
            if not xq:
                xq = re.search('(?<=罪，).*?(?=[；|，|。])', pj.group())
                
            if xq:
                bgr_matrix['xq'][i] = xq.group()
            else:
                bgr_matrix['xq'][i] =  ''
            #############      hx           #################
            hx = re.search('缓刑.*?(?=[；|，|。])', pj.group())
            if hx:
                bgr_matrix['hx'][i] = hx.group()
                
                
            #############     level        ###################
            # L0 免于处罚
            # L1 xq <= 3 year
            # L2 3 year < xq < 10  year
            # L3 10 <= xq < 15 year
            # L4 无期
            # L5 死刑
            if xq.group() == '免予刑事处罚':
                bgr_matrix['level'][i] = 0
            else:
                l1 = re.search('[一二]年(.*?月)?', xq.group())
                l2 = re.search('[三四五六七八九]年(.*?月)?', pj.group())
                l3 = re.search('十.?年(.*?月)?', pj.group())
                
                if not l1:
                    l1 = re.search('[一二三四五六七八九十][一]?.*?月', pj.group())
                if l1:
                    bgr_matrix['level'][i] = 1
                if l2:
                    bgr_matrix['level'][i] = 2
                    
                if l3:
                    bgr_matrix['level'][i] = 3
            print(bgr_matrix)   
        
        return bgr_matrix
         
        
    #取得指定辩护人姓名
    def get_zdbhr(self):
        zdbhr_list = re.findall('指定辩护人\w{2,4}，.*?律师', self.content)
        for i in range(len(zdbhr_list)):
            zdbhr = re.search('指定辩护人\w{2,4}(?=，)', zdbhr_list[i])
            zdbhr_list[i] = zdbhr.group()
        self.zdbhr_list = zdbhr_list
        
        
    #取得被告人姓名    
    def get_bgr(self):
        self.bgr_list = self._search_bgr(self.content)


    #取得事务所名字
    def get_sws(self):    
        sws_list = re.findall('(?<=辩护人).*?事务所律师', self.content)
        for i in range(len(sws_list)):
            
            #sws = re.search('(?<=[，,、]).*?事务所', sws_list[i])
            sws = re.search(CourtList.sws_pattern, sws_list[i])
            
            if sws:
                sws_list[i] = sws.group()
            else:
                print('------------------------------------')
                print(sws_list[i])
                #sws_list[i] = sws_list[i]
        #print(sws_list)        
        self.sws_list = sws_list

    
    
    #取得一组辩护人姓名
    def get_group_bhr(self):    
        self.gbhr = re.findall('(辩护人\w{2,4}，.{2,20}事务所律师。?辩护人\w{2,4}，.*?事务所律师)', self.content)
        #self.gbhr = re.findall('(辩护人\w{2,4}，.{2,20}事务所律师。辩护人)', self.content)
        
    
    def get_procedure(self):
        p = re.search('普通程序', self.content)
        if not p:
            p = re.search('简易程序', self.content)
        if not p:
            self.procedure = '普通程序'
        else:
            self.procedure = p.group()
        
        
    def get_hyt(self):    
        self.hyt = re.findall('合议庭', self.content)
    
    
    def bhr_test(self):    
        self.bhrt = re.search('辩护人', self.content)
        
        
        
    def bgr_test(self):    
        self.bgrt = re.search('被告人', self.content)
    
    
    def id_test(self):
        self.idt = re.search('[0-9]{1,5}号', self.content)
        
