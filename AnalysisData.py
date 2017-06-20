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

import DocAnalyser
import CourtList
import FileUtils


def get_zm(name, zm_list):
    zm_in_name = ''
    for zm in zm_list:
        if not zm_in_name:
            zm_in_name = re.search(zm, name)
        else:
            break
    if zm_in_name:
        return zm_in_name.group()
    else:
        #print(zm)
        #print(name)
        return None
        
        
def calculate_bh_rate_2(case_matrix, procedure=None):
    count = len(case_matrix['name'])
    print('Total case number is %s' % count)
    for i in range(count):
        if not case_matrix['bgr'][i]:
            for key in case_matrix:
                case_matrix[key][i] = ''
        
    bgr_n = 0
    bhr_n = 0
    gbhr_n = 0
    for i in range(count):
        if case_matrix['procedure'][i] == procedure:
            bgr_n += int(case_matrix['bgr_n'][i])
            gbhr_n += int(case_matrix['gbhr_n'][i])
            if int(case_matrix['wtbhr_n'][i]) == 0 and int(case_matrix['zdbhr_n'][i]) == 0 and int(case_matrix['sws_n'][i]) != 0:
                bhr_n += int(case_matrix['sws_n'][i])
            else:
                bhr_n += int(case_matrix['wtbhr_n'][i])
                bhr_n += int(case_matrix['zdbhr_n'][i])
            
            
    
    
    print('辩护人 %s  辩护人组%s 被告人 %s' % (bhr_n, gbhr_n, bgr_n))
    try:
        bh_rate = (bhr_n - gbhr_n) / bgr_n
    except ZeroDivisionError:
        bh_rate = 0
    print('%s 的辩护率是 %s' % (procedure, bh_rate))
    
    return bh_rate



    

def calculate_bh_rate(case_matrix, zm=None):
    if 'match' not in case_matrix.keys():
        #print('----------------------------------------------------------')
        case_matrix = FileUtils.add_cols_2_matrix(case_matrix, ['match'])
    
    count = len(case_matrix['name'])
    case_matrix['match'] = ['Y'] * len(case_matrix['name'])
    print('Total case number is %s' % count)
    for i in range(count):
        if not case_matrix['bgr'][i]:
            for key in case_matrix:
                case_matrix[key][i] = ''
        if zm:
            if case_matrix['gzm'][i] != zm:
                case_matrix['match'][i] = 'N'
                
             #print(case_matrix['zm'][i])
                #for key in case_matrix:
                    #case_matrix[key][i] = ''
    #count = len(case_matrix['name'])
    #print(count)
    #a 统计被告人数量，如果没有搜索出被告人，删除此条
    #    b 统计辩护律师数量
    #c 辩护律师分组数量

    #(b - c)/a
    bgr_n = 0
    bhr_n = 0
    gbhr_n = 0
    for i in range(count):
        #print(i)
    #    print('')
        if case_matrix['match'][i] == 'Y':
            
            bgr_n += int(case_matrix['bgr_n'][i])
            #print('bgr %s'%case_matrix['bgr_n'][i])
            #print('bgr_n %s'%bgr_n)
            if int(case_matrix['wtbhr_n'][i]) == 0 and int(case_matrix['zdbhr_n'][i]) == 0 and int(case_matrix['sws_n'][i]) != 0:
                bhr_n += int(case_matrix['sws_n'][i])
            else:
                bhr_n += int(case_matrix['wtbhr_n'][i])
                bhr_n += int(case_matrix['zdbhr_n'][i])
            
            
            
            gbhr_n += int(case_matrix['gbhr_n'][i])
    
    
    print('辩护人 %s  辩护人组%s 被告人 %s' % (bhr_n, gbhr_n, bgr_n))
    try:
        bh_rate = (bhr_n - gbhr_n) / bgr_n
    except ZeroDivisionError:
        print('No %s case' % zm)
        bh_rate = 0
    print('%s 的辩护率是 %s' % (zm, bh_rate))
    
    return bh_rate
        

def calculate_bhr_number(case_matrix, zm=None):
    if 'match' not in case_matrix.keys():
        #print('----------------------------------------------------------')
        case_matrix = FileUtils.add_cols_2_matrix(case_matrix, ['match'])
    
    count = len(case_matrix['name'])
    case_matrix['match'] = ['Y'] * len(case_matrix['name'])
    print('Total case number is %s' % count)
    for i in range(count):
        if not case_matrix['bgr'][i]:
            for key in case_matrix:
                case_matrix[key][i] = ''
        if zm:
            if case_matrix['gzm'][i] != zm:
                case_matrix['match'][i] = 'N'
                
        
    bhr_n = 0

    for i in range(count):
        if case_matrix['match'][i] == 'Y':
            bhr_n += int(case_matrix['wtbhr_n'][i])
            bhr_n += int(case_matrix['zdbhr_n'][i])
            if int(case_matrix['wtbhr_n'][i]) == 0 and int(case_matrix['zdbhr_n'][i]) == 0 and int(case_matrix['sws_n'][i]) != 0:
                bhr_n += int(case_matrix['sws_n'][i])        
    
    
    return bhr_n        
        
        
def calculate_bgr_number(case_matrix, zm=None):
    if 'match' not in case_matrix.keys():
        #print('----------------------------------------------------------')
        case_matrix = FileUtils.add_cols_2_matrix(case_matrix, ['match'])
    
    count = len(case_matrix['name'])
    case_matrix['match'] = ['Y'] * len(case_matrix['name'])
    print('Total case number is %s' % count)
    for i in range(count):
        if not case_matrix['bgr'][i]:
            for key in case_matrix:
                case_matrix[key][i] = ''
        if zm:
            if case_matrix['gzm'][i] != zm:
                case_matrix['match'][i] = 'N'
                
        
    bgr_n = 0

    for i in range(count):
        if case_matrix['match'][i] == 'Y':
            bgr_n += int(case_matrix['bgr_n'][i])
            
    
    
    return bgr_n        
        
        
def count_case_number_of_zm(case_matrix, zm=None):
    zm_count = case_matrix['zm'].count(zm)
    print('%s ----------------------> %s' % (zm_count, zm))
    return zm_count
        
        
        
def file_analyse(path, court, case_matrix):
    path_2_court = path + court
    count = len(case_matrix['name'])
    analyser = DocAnalyser.DocAnalyser()
    for i in range(count):
        #print('%s / %s' % (i, count))
    #for i in range(43, 44):
        #print('%s/%s' % (i, count))
        file_name = path_2_court + '\\' + case_matrix['name'][i] + case_matrix['date'][i] + '.docx'
        #print(file_name)
        analyser.read_doc(file_name)
        analyser.get_wtbhr()
        analyser.get_zdbhr()
        analyser.get_group_bhr()
        analyser.get_bgr()
        analyser.get_procedure()
        analyser.get_sws()
        analyser.get_hyt()
        analyser.bhr_test()
        analyser.bgr_test()
        
        case_matrix['bhrt'][i] = 'Y' if analyser.bhrt else 'N'
        case_matrix['bgrt'][i] = 'Y' if analyser.bgrt else 'N'
        
        
        wtbhr_n = len(analyser.wtbhr_list)
        zdbhr_n = len(analyser.zdbhr_list)
        bgr_n = len(analyser.bgr_list)
        sws_n = len(analyser.sws_list)
        gbhr_n = len(analyser.gbhr)
        #print(analyser.content)
        #print(analyser.gbhr)
        #sys.exit(0)
        for w in range(wtbhr_n):
            case_matrix['wtbhr'][i] += analyser.wtbhr_list[w]
            case_matrix['wtbhr'][i] += ', '
        case_matrix['wtbhr'][i] = case_matrix['wtbhr'][i][:-2]
        case_matrix['wtbhr_n'][i] = wtbhr_n
        
        for z in range(zdbhr_n):
            case_matrix['zdbhr'][i] += analyser.zdbhr_list[z]
            case_matrix['zdbhr'][i] += ', '
        case_matrix['zdbhr'][i] = case_matrix['zdbhr'][i][:-2]
        case_matrix['zdbhr_n'][i] = zdbhr_n
        
        
        for b in range(bgr_n):
            case_matrix['bgr'][i] += analyser.bgr_list[b]
            case_matrix['bgr'][i] += ', '
        case_matrix['bgr'][i] = case_matrix['bgr'][i][:-2]
        case_matrix['bgr_n'][i] = bgr_n
        
        #for p in range(len(analyser.procedure)):
        #    case_matrix['procedure'][i] += analyser.procedure[p]
        #    case_matrix['procedure'][i] += ', '
        case_matrix['procedure'][i] = analyser.procedure
        
        
        for h in range(len(analyser.hyt)):
            case_matrix['hyt'][i] += analyser.hyt[h]
            case_matrix['hyt'][i] += ', '
        case_matrix['hyt'][i] = case_matrix['hyt'][i][:-2]
        
        
        
        for s in range(sws_n):
            case_matrix['sws'][i] += analyser.sws_list[s]
            case_matrix['sws'][i] += ', '
        case_matrix['sws'][i] = case_matrix['sws'][i][:-2]
        case_matrix['sws_n'][i] = sws_n
        
        case_matrix['gbhr'][i] = analyser.gbhr
        case_matrix['gbhr_n'][i] = gbhr_n
        
        
        
        case_matrix['region'][i] = get_region(court)
        case_matrix['level'][i] = get_court_level(court)
        
        case_matrix['zm'][i] = analyser.get_1st_zm()
        for g in CourtList.zm_group_list:
            if case_matrix['zm'][i] in CourtList.zm_group[g]:
                case_matrix['gzm'][i] = CourtList.zm_group_name[g]
                break
        
        #if not case_matrix['gzm'][i]:
        #    print('%s not in any group' % case_matrix['zm'][i])
        #    for g in CourtList.zm_group_list:
        #        zm_t = get_zm(case_matrix['zm'][i], CourtList.zm_group[g])
        #    if not zm_t:
        #        print('%s --------> %s' % (zm_t, case_matrix['zm'][i]))
                #case_matrix['gzm'][i] = CourtList.zm_group_name[g]
                #break
        
        if not case_matrix['zm'][i]:
            pass
            #print('Case name is: %s ' % case_matrix['name'][i])
        if not case_matrix['gzm'][i]:
            if case_matrix['zm'][i]:
                for g in CourtList.zm_group_list:
                    zm_t = get_zm(case_matrix['zm'][i], CourtList.zm_group[g])
                    if zm_t:
                        #print('%s --------> %s' % (zm_t, case_matrix['zm'][i]))
                        case_matrix['gzm'][i] = CourtList.zm_group_name[g]
                        break
        
        if not case_matrix['gzm'][i]:
            print(case_matrix['zm'][i])
            
    return case_matrix



        
def combine(path, region):
    file_list = CourtList.court_list[region]
    case_matrix = read_csv((path + file_list[0]), '_result')
    for file in file_list[1:]:
        case_matrix_t = read_csv((path + file), '_result')
        #print(case_matrix_t)
        for key in case_matrix_t:
            case_matrix[key] += case_matrix_t[key]
    csv_file = path + region + '_total.csv'    
    FileUtils.dump2csv(case_matrix, csv_file)
        

    

def combine_matrix(matrixA, matrixB):
    for key in matrixA:
        matrixA[key] += matrixB[key]
    return matrixA
    
def bgr_analyse(path_2_court, case_matrix):
    count = len(case_matrix['name'])
    analyser = DocAnalyser.DocAnalyser()
    bgr_matrix = {'bgr':[], 'bhr':[], 'zm':[], 'xq':[], 'hx':[], 'level':[], 'cn':[]}
    #for i in range(count):
    for i in range(104, 105):
        #i = 16
        
        print('%s/%s' % (i, count))
        file_name = path_2_court + '\\' + case_matrix['name'][i] + case_matrix['date'][i] + '.docx'
        print(file_name)
        analyser.read_doc(file_name)
        bgr_matrix_t = analyser.get_bhr_of_bgr(i)
        bgr_matrix = combine_matrix(bgr_matrix, bgr_matrix_t)
    return bgr_matrix
    
def bgr_csv_gen(path, court):
    csv_file = path + court + '.csv'
    bgr_csv_file = path + court + '_bgr.csv'
    case_matrix = FileUtils.read_csv(csv_file)
    bgr_matrix = bgr_analyse(path + court, case_matrix)
    FileUtils.dump2csv(bgr_matrix, bgr_csv_file)    

def get_court_level(court):
    for key in CourtList.court_list:
        if court in CourtList.court_list[key]:
            if key == 'zhongji':
                return '中级'
            else:
                return '基层'
    
    
    
def get_region(court):
    for key in CourtList.court_list:
        if court in CourtList.court_list[key]:
            if key == 'zhongji':
                if court == '成都市中级人民法院':
                    return 'chengdu'
                if court == '自贡市中级人民法院':
                    return 'zigong'  
                if court == '攀枝花市中级人民法院':
                    return 'panzhihua'        
                if court == '泸州市中级人民法院':
                    return 'luzhou'        

                if court == '德阳市中级人民法院':
                    return 'deyang'        

                if court == '绵阳市中级人民法院':
                    return 'mianyang'        

                if court == '广元市中级人民法院':
                    return 'guangyuan'        

                if court == '遂宁市中级人民法院':
                    return 'shuining'        

                if court == '内江市中级人民法院':
                    return 'neijiang'        

                if court == '乐山市中级人民法院':
                    return 'leshan'        

                if court == '南充市中级人民法院':
                    return 'nanchong'        

                if court == '眉山市中级人民法院':
                    return 'meishan'        

                if court == '宜宾市中级人民法院':
                    return 'yibing'        

                if court == '广安市中级人民法院':
                    return 'guangan'        

                if court == '达州市中级人民法院':
                    return 'dazhou'        

                if court == '雅安市中级人民法院':
                    return 'yaan'        

                if court == '巴中市中级人民法院':
                    return 'bazhong'        

                if court == '资阳市中级人民法院':
                    return 'ziyang'        

                if court == '阿坝藏族羌族自治州中级人民法院':
                    return 'wenchuan'        

                if court == '甘孜藏族自治州中级人民法院':
                    return 'kangding'        

                if court == '凉山彝族自治州中级人民法院':
                    return 'xichang'        

                if court == '成都铁路运输中级法院':
                    return 'tielu'        

            else:
                return key

def get_middle_court_name(region):
    if region == 'chengdu':
        return '成都市中级人民法院'
        
    if region == 'zigong':
        return '自贡市中级人民法院'
        
    if region == 'panzhihua':
        return '攀枝花市中级人民法院'
                
    if region == 'luzhou':        
        return '泸州市中级人民法院'
       
    if region == 'deyang':
        return '德阳市中级人民法院'
      
    if region == 'mianyang':        
        return '绵阳市中级人民法院'
       
    if region == 'guangyuan':        
        return '广元市中级人民法院'
    
    if region == 'shuining':        
        return '遂宁市中级人民法院'
      
    if region == 'neijiang':
        return '内江市中级人民法院'

    if region == 'leshan':
        return '乐山市中级人民法院'

    if region == 'nanchong':
        return '南充市中级人民法院'

    if region == 'meishan':        
        return '眉山市中级人民法院'
        
    if  region == 'yibing':
        return '宜宾市中级人民法院'
       
    if  region == 'guangan':        
        return '广安市中级人民法院'
       
    if  region == 'dazhou':        
        return '达州市中级人民法院'
       
    if  region == 'yaan':       
        return '雅安市中级人民法院'
       
    if  region == 'bazhong':        
        return '巴中市中级人民法院'
       
    if  region == 'ziyang':        
        return '资阳市中级人民法院'
       
    if  region == 'wenchuan':        
        return '阿坝藏族羌族自治州中级人民法院'
       
    if  region == 'kangding':        
        return '甘孜藏族自治州中级人民法院'
       
    if  region == 'xichang':        
        return '凉山彝族自治州中级人民法院'
       
    if  region == 'tielu':
        return '成都铁路运输中级法院'       

                
def summary_csv_gen(path, court):
    col_list = ['bgrt', 'bhrt', 'bgr', 'bgr_n',
                'wtbhr', 'wtbhr_n', 'zdbhr',
                'zdbhr_n', 'sws', 'sws_n',
                'procedure', 'hyt', 'gbhr', 'gbhr_n',
                'zm', 'gzm', 'region', 'level']
    csv_file = path + court + '.csv'
    case_matrix = FileUtils.read_csv(csv_file)
    case_matrix = FileUtils.add_cols_2_matrix(case_matrix, col_list)
    case_matrix = file_analyse(path, court, case_matrix)
    csv_file_result = path + court + '_result.csv'     
    FileUtils.dump2csv(case_matrix, csv_file_result) 
    
    
def bh_rate_csv_gen(path, year):
    bh_rate_matrix = {'region':[],'total':[]}
    col_list = CourtList.zm_group_list
    
    bh_rate_matrix = FileUtils.add_cols_2_matrix(bh_rate_matrix, col_list)
    bh_rate_matrix = FileUtils.add_cols_2_matrix(bh_rate_matrix, ['jycx', 'ptcx'])
    
    
    bh_rate_matrix['region'].append('')
    bh_rate_matrix['region'].append('sichuan')
    bh_rate_matrix['total'].append('所有')
    
    for key in CourtList.court_list:
        bh_rate_matrix['region'].append(key)
    for key in CourtList.court_list:    
        for court in CourtList.court_list[key]:
            bh_rate_matrix['region'].append(court)
    
    # add zm group name to row 2 since it's not good to use Chinese to be dict key.
    for zm in CourtList.zm_group_list:
        bh_rate_matrix[zm].append(CourtList.zm_group_name[zm])
    
    # Add 普通程序 简易程序to the last two columns.
    bh_rate_matrix['jycx'].append('简易程序')
    bh_rate_matrix['ptcx'].append('普通程序')
    
    
    # Generate matrix for whole sichuan
    case_matrix = {}
    for key in CourtList.court_list:
        for court in CourtList.court_list[key]:
            csv_file = path + court + '_result.csv'
            if case_matrix:
                case_matrix = combine_matrix(case_matrix, FileUtils.read_csv(csv_file))
            else:
                case_matrix = FileUtils.read_csv(csv_file)
    
    bh_rate = calculate_bh_rate(case_matrix)
    bh_rate_matrix['total'].append(bh_rate)
    for zm in CourtList.zm_group_list:
        bh_rate = calculate_bh_rate(case_matrix, CourtList.zm_group_name[zm])
        bh_rate_matrix[zm].append(bh_rate)    
    
    bh_rate_matrix['jycx'].append(calculate_bh_rate_2(case_matrix, '简易程序'))
    bh_rate_matrix['ptcx'].append(calculate_bh_rate_2(case_matrix, '普通程序'))
    
    
    
    
    # Generate matrix for region
    for key in CourtList.court_list:
        case_matrix = {}
        #print('----------------->%s'%key)
        for court in CourtList.court_list[key]:
                csv_file = path + court + '_result.csv'
                #print(csv_file)
                #print(court)
                if case_matrix:
                    case_matrix = combine_matrix(case_matrix, FileUtils.read_csv(csv_file))
                else:
                    case_matrix = FileUtils.read_csv(csv_file)
        
        if key != 'zhongji':    
            court = get_middle_court_name(key)            
            csv_file = path + court + '_result.csv'            
            case_matrix = combine_matrix(case_matrix, FileUtils.read_csv(csv_file))        
                    
        bh_rate = calculate_bh_rate(case_matrix)
        bh_rate_matrix['total'].append(bh_rate)
        bh_rate_matrix['jycx'].append(calculate_bh_rate_2(case_matrix, '简易程序'))
        bh_rate_matrix['ptcx'].append(calculate_bh_rate_2(case_matrix, '普通程序'))
        for zm in CourtList.zm_group_list:
            #print(csv_file)
            bh_rate = calculate_bh_rate(case_matrix, CourtList.zm_group_name[zm])
            bh_rate_matrix[zm].append(bh_rate) 
        
    # Generate matrix for court
    for key in CourtList.court_list:
        #print('----------------->%s'%key)
        for court in CourtList.court_list[key]:
            case_matrix = {}
            csv_file = path + court + '_result.csv'
            case_matrix = FileUtils.read_csv(csv_file)
            bh_rate = calculate_bh_rate(case_matrix)
            bh_rate_matrix['total'].append(bh_rate)
            bh_rate_matrix['jycx'].append(calculate_bh_rate_2(case_matrix, '简易程序'))
            bh_rate_matrix['ptcx'].append(calculate_bh_rate_2(case_matrix, '普通程序'))
            for zm in CourtList.zm_group_list:
                bh_rate = calculate_bh_rate(case_matrix, CourtList.zm_group_name[zm])
                bh_rate_matrix[zm].append(bh_rate) 

                
    print(bh_rate_matrix)
    csv_file_bh_rate = path + year + '_bh_rate.csv'     
    FileUtils.dump2csv(bh_rate_matrix, csv_file_bh_rate) 


def bgr_csv_gen(path, year):
    bgr_number_matrix = {'region':[],'total':[]}
    col_list = CourtList.zm_group_list
    
    bgr_number_matrix = FileUtils.add_cols_2_matrix(bgr_number_matrix, col_list)
    
    bgr_number_matrix['region'].append('')
    bgr_number_matrix['region'].append('sichuan')
    bgr_number_matrix['total'].append('所有')
    
    for key in CourtList.court_list:
        bgr_number_matrix['region'].append(key)
    for key in CourtList.court_list:    
        for court in CourtList.court_list[key]:
            bgr_number_matrix['region'].append(court)
    
    # add zm group name to row 2 since it's not good to use Chinese to be dict key.
    for zm in CourtList.zm_group_list:
        bgr_number_matrix[zm].append(CourtList.zm_group_name[zm])
    
    
    # Generate matrix for whole sichuan
    case_matrix = {}
    for key in CourtList.court_list:
        for court in CourtList.court_list[key]:
            csv_file = path + court + '_result.csv'
            if case_matrix:
                case_matrix = combine_matrix(case_matrix, FileUtils.read_csv(csv_file))
            else:
                case_matrix = FileUtils.read_csv(csv_file)
    
    bgr_number = calculate_bgr_number(case_matrix)
    bgr_number_matrix['total'].append(bgr_number)
    for zm in CourtList.zm_group_list:
        bgr_number = calculate_bgr_number(case_matrix, CourtList.zm_group_name[zm])
        bgr_number_matrix[zm].append(bgr_number)    
    
    # Generate matrix for region
    for key in CourtList.court_list:
        case_matrix = {}
        #print('----------------->%s'%key)
        for court in CourtList.court_list[key]:
                csv_file = path + court + '_result.csv'
                #print(csv_file)
                #print(court)
                if case_matrix:
                    case_matrix = combine_matrix(case_matrix, FileUtils.read_csv(csv_file))
                else:
                    case_matrix = FileUtils.read_csv(csv_file)
        bgr_number = calculate_bgr_number(case_matrix)
        bgr_number_matrix['total'].append(bgr_number)
        for zm in CourtList.zm_group_list:
            bgr_number = calculate_bgr_number(case_matrix, CourtList.zm_group_name[zm])
            bgr_number_matrix[zm].append(bgr_number) 
        
    # Generate matrix for court
    for key in CourtList.court_list:
        for court in CourtList.court_list[key]:
            case_matrix = {}
            csv_file = path + court + '_result.csv'
            case_matrix = FileUtils.read_csv(csv_file)
            bgr_number = calculate_bgr_number(case_matrix)
            bgr_number_matrix['total'].append(bgr_number)
            for zm in CourtList.zm_group_list:
                bgr_number = calculate_bgr_number(case_matrix, CourtList.zm_group_name[zm])
                bgr_number_matrix[zm].append(bgr_number) 

                
    print(bgr_number_matrix)
    csv_file_bgr_number = path + year + '_bgr_number.csv'     
    FileUtils.dump2csv(bgr_number_matrix, csv_file_bgr_number)

    
def bhr_csv_gen(path, year):
    bhr_number_matrix = {'region':[],'total':[]}
    col_list = CourtList.zm_group_list
    
    bhr_number_matrix = FileUtils.add_cols_2_matrix(bhr_number_matrix, col_list)
    
    bhr_number_matrix['region'].append('')
    bhr_number_matrix['region'].append('sichuan')
    bhr_number_matrix['total'].append('所有')
    
    for key in CourtList.court_list:
        bhr_number_matrix['region'].append(key)
    for key in CourtList.court_list:    
        for court in CourtList.court_list[key]:
            bhr_number_matrix['region'].append(court)
    
    # add zm group name to row 2 since it's not good to use Chinese to be dict key.
    for zm in CourtList.zm_group_list:
        bhr_number_matrix[zm].append(CourtList.zm_group_name[zm])
    
    
    # Generate matrix for whole sichuan
    case_matrix = {}
    for key in CourtList.court_list:
        for court in CourtList.court_list[key]:
            csv_file = path + court + '_result.csv'
            if case_matrix:
                case_matrix = combine_matrix(case_matrix, FileUtils.read_csv(csv_file))
            else:
                case_matrix = FileUtils.read_csv(csv_file)
    
    bhr_number = calculate_bhr_number(case_matrix)
    bhr_number_matrix['total'].append(bhr_number)
    for zm in CourtList.zm_group_list:
        bhr_number = calculate_bhr_number(case_matrix, CourtList.zm_group_name[zm])
        bhr_number_matrix[zm].append(bhr_number)    
    
    # Generate matrix for region
    for key in CourtList.court_list:
        case_matrix = {}
        #print('----------------->%s'%key)
        for court in CourtList.court_list[key]:
                csv_file = path + court + '_result.csv'
                #print(csv_file)
                #print(court)
                if case_matrix:
                    case_matrix = combine_matrix(case_matrix, FileUtils.read_csv(csv_file))
                else:
                    case_matrix = FileUtils.read_csv(csv_file)
        bhr_number = calculate_bhr_number(case_matrix)
        bhr_number_matrix['total'].append(bhr_number)
        for zm in CourtList.zm_group_list:
            bhr_number = calculate_bhr_number(case_matrix, CourtList.zm_group_name[zm])
            bhr_number_matrix[zm].append(bhr_number) 
        
    # Generate matrix for court
    for key in CourtList.court_list:
        for court in CourtList.court_list[key]:
            case_matrix = {}
            csv_file = path + court + '_result.csv'
            case_matrix = FileUtils.read_csv(csv_file)
            bhr_number = calculate_bhr_number(case_matrix)
            bhr_number_matrix['total'].append(bhr_number)
            for zm in CourtList.zm_group_list:
                bhr_number = calculate_bhr_number(case_matrix, CourtList.zm_group_name[zm])
                bhr_number_matrix[zm].append(bhr_number) 

                
    print(bhr_number_matrix)
    csv_file_bhr_number = path + year + '_bhr_number.csv'     
    FileUtils.dump2csv(bhr_number_matrix, csv_file_bhr_number) 
    
  
    
def main():    
    desc = ""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-y', '--year', action='store')
    parser.add_argument('-c', '--court', action='store')
    parser.add_argument('-r', '--region', action='store')
    parser.add_argument('-s', '--summary', action='store_true')
    parser.add_argument('--bgr', action='store_true')
    parser.add_argument('-a', '--append', action='store_true')
    parser.add_argument('--calculate', action='store')
    parser.add_argument('--count', action='store')
    parser.add_argument('--zm', action='store')
    parser.add_argument('--combine', action='store_true')
    parser.add_argument('--test', action='store_true')
    
    
    args = parser.parse_args()
    year = args.year
    region = args.region
    court = args.court
    path = 'C:\\Users\\lij37\\Code\\Han' + year + '\\'
    if args.zm:
        zm = args.zm
    else:
        zm = None
    
    
    if args.bgr:
        if court:
            bgr_csv_gen(path, court)
        elif region:
            for court in CourtList.court_list[region]:
                bgr_csv_gen(path, court)
        else:
            print('invalid')
        sys.exit(0)
    
        
    if args.append:
        if region:
            combine(path, region)
            sys.exit(0)
#   

    if args.combine:
        case_matrix = {}
        csv_tt_file = path + year + '_total_result.csv'
        for key in CourtList.court_list:    
            for court in CourtList.court_list[key]:
                csv_file = path + court + '_result.csv'
                if case_matrix:
                    case_matrix = combine_matrix(case_matrix, FileUtils.read_csv(csv_file))
                else:
                    case_matrix = FileUtils.read_csv(csv_file)
        FileUtils.dump2csv(case_matrix, csv_tt_file) 
    
    
    if args.calculate ==  'bhr_number':
        if args.summary:
            bhr_csv_gen(path, year)
            sys.exit(0)
    elif args.calculate ==  'bgr_number':
        if args.summary:
            bgr_csv_gen(path, year)
            sys.exit(0)
    
    
    
    if args.calculate ==  'bh_rate':
        if args.summary:
            bh_rate_csv_gen(path, year)
            sys.exit(0)
        case_matrix = {}
        if region:
            for court in CourtList.court_list[region]:
                csv_file = path + court + '_result.csv'
                case_matrix_s = FileUtils.read_csv(csv_file)
                print(court)
                calculate_bh_rate(case_matrix_s, zm)
                print('')
            
                csv_file = path + court + '_result.csv'
                if case_matrix:
                    case_matrix = combine_matrix(case_matrix, FileUtils.read_csv(csv_file))
                else:
                    case_matrix = FileUtils.read_csv(csv_file)
            print(region)
            calculate_bh_rate(case_matrix, zm)
        elif court:
            csv_file = path + court + '_result.csv'
            case_matrix = FileUtils.read_csv(csv_file)
            calculate_bh_rate(case_matrix, zm)
        else:
            pass
    
    
    if args.calculate == 'bh_rate_procedure':
        #case_matrix = {}
        #for key in CourtList.court_list:    
        #    for court in CourtList.court_list[key]:
        #        csv_file = path + court + '_result.csv'
        #        if case_matrix:
        #            case_matrix = combine_matrix(case_matrix, FileUtils.read_csv(csv_file))
        #        else:
        #            case_matrix = FileUtils.read_csv(csv_file)
        #calculate_bh_rate_2(case_matrix, '简易程序')
        #calculate_bh_rate_2(case_matrix, '普通程序')
        if court:
            csv_file = path + court + '_result.csv'
            case_matrix_c = FileUtils.read_csv(csv_file)
            calculate_bh_rate_2(case_matrix_c, '简易程序')
            print('')
            calculate_bh_rate_2(case_matrix_c, '普通程序')
        if region:
            for court in CourtList.court_list[region]:
                print(court)
                csv_file = path + court + '_result.csv'
                case_matrix_c = FileUtils.read_csv(csv_file)
                calculate_bh_rate_2(case_matrix_c, '简易程序')
                print('')
                calculate_bh_rate_2(case_matrix_c, '普通程序')
                print('')
    
    if args.count ==  'zm':
        case_matrix = {}
        if region:
            for court in CourtList.court_list[region]:
                csv_file = path + court + '_result.csv'
                if case_matrix:
                    case_matrix = combine_matrix(case_matrix, FileUtils.read_csv(csv_file))
                else:
                    case_matrix = FileUtils.read_csv(csv_file)
            print(region)
            for zm in CourtList.zm_list:
                count_case_number_of_zm(case_matrix, zm)
        elif court:
            csv_file = path + court + '_result.csv'
            case_matrix = FileUtils.read_csv(csv_file)
            calculate_bh_rate(case_matrix, zm)
        else:
            pass    
        
        
    if args.summary:
        if region:
            for court in CourtList.court_list[region]:
                summary_csv_gen(path, court)
        elif court:
            summary_csv_gen(path, court)
        else:
            for key in CourtList.court_list:
                for court in CourtList.court_list[key]:
                    summary_csv_gen(path, court)
    
    if args.test:
        #file = 'C:\\Users\\lij37\\Code\\Han2015\\内江市中级人民法院\\钟涛故意杀人、盗窃罪一审刑事判决书2015-05-02.docx'
        folder = 'C:\\Users\\lij37\\Code\\Han2015\\成都市金牛区人民法院'
        file_list = os.listdir(folder)
        analyser = DocAnalyser.DocAnalyser()
        for file in file_list:
            #print(file)
            analyser.analyse_doc(folder + '\\' + file)
            #print('')
            
        #for key, value in case_info.item():
        #    print('%s %s' % (key, value))
        #analyser.get_wtbhr()
        #analyser.get_bgr()
        #print(analyser.bgr_list)
        #print(analyser.content)
        #analyser.get_group_bhr()
        
        #analyser.get_wtbhr()
        #analyser.get_zdbhr()
        sys.exit(0)
        #print(analyser.gbhr)
        #print(analyser.content)
    
        #print(get_region('南充市中级人民法院'))
        #path += '中级人民法院'
        #for court in CourtList.court_list['zhongji']:
        #    os.makedirs(path + court)
        #sys.exit(0)
        
        #analyser = DocAnalyser.DocAnalyser()
                
        #file_list = os.listdir(path + '中级人民法院')
        #for file in file_list:
        #    analyser.read_doc(path + '中级人民法院\\' + file)
        #    analyser.analyse_jufa()
        #    print(analyser.court)
        #    FileUtils.copy_csv(path + '中级人民法院\\' + file, path + analyser.court + '\\' + file)
            
            #FileUtils.move(path + '中级人民法院\\' + file, path + '中级人民法院\\' + file[:-19] + analyser.date + '.docx')
            
        
        analyser = DocAnalyser.DocAnalyser()
            
        for court in CourtList.court_list['zhongji']:
            file_list = os.listdir(path + court)
        #    case_matrix = {'name':[], 'doc_id':[], 'date':[],  'case_id':[],  'procedure':[],  'court':[]}
            case_matrix = {'name':[], 'doc_id':[], 'date':[]}
        
            for file in file_list:
                #print(file)
                analyser.read_doc(path + court + '\\' + file)
                analyser.analyse_jufa()
                case_matrix['name'].append(file[:-15])
                case_matrix['doc_id'].append('')
                case_matrix['date'].append(analyser.date)
        #        case_matrix['case_id'].append(analyser.case_id)
        #        case_matrix['procedure'].append('')
        #        case_matrix['court'].append(analyser.court)
            csv_file = path + court + '.csv'   
            FileUtils.dump2csv(case_matrix, csv_file)
        #csv_file = 'C:\\Users\\lij37\\Code\\Han2015\\南充市中级人民法院_result.csv'
        #case_matrix = FileUtils.read_csv(csv_file)
        #bh_rate = calculate_bh_rate(case_matrix)
        #analyser = DocAnalyser.DocAnalyser()
        
if __name__ == "__main__":
    main()
    
    
    
    
    