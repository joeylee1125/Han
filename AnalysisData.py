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
#import Court


def read_doc(doc_name):
    try:
        document = Document(doc_name) if doc_name else sys.exit(0)
    except:
        print("Document %s is invalid" % doc_name)
            
    #   读取每段资料
    l = [paragraph.text for paragraph in document.paragraphs]
    s = ''.join(str(e) for e in l)
    return s

        
#取得委托辩护人姓名
def get_wtbhr(doc_content):
    bhr_list = re.findall('(?<!指定)辩护人\：?\w{2,4}，.*?律师', doc_content)
    for i in range(len(bhr_list)):
        bhr = re.search('辩护人\：?\w{2,4}(?=，)', bhr_list[i])
        bhr_list[i] = bhr.group()
    return bhr_list    


def get_zdbhr(doc_content):
    zdbhr_list = re.findall('指定辩护人\w{2,4}，.*?律师', doc_content)
    for i in range(len(zdbhr_list)):
        zdbhr = re.search('指定辩护人\w{2,4}(?=，)', zdbhr_list[i])
        zdbhr_list[i] = zdbhr.group()
    return zdbhr_list
        
def get_bgr(doc_content):
    bgr_list = re.findall('被告人）?\w{2,4}，.?[曾|男|女|别]', doc_content)
    for i in range(len(bgr_list)):
        bgr = re.search('被告人）?\w{2,4}(?=，)', bgr_list[i])
        bgr_list[i] = bgr.group().replace('）', '')
    return bgr_list


def get_sws(doc_content):    
    sws_list = re.findall('(?<=辩护人).*?事务所律师', doc_content)
    #print(sws_list)
    
    for i in range(len(sws_list)):
        sws = re.search('(?<=，).*事务所', sws_list[i])
        sws_list[i] = sws.group()
    #print(sws_list)
    return sws_list

    
def get_group_bhr(doc_content):    
    #gbhr = re.findall('(辩护人\w{2,4}，\w+律师.{1,3}辩护人\w{2,4}，\w+律师)', doc_content)
    gbhr = re.findall('(辩护人\w{2,4}，.*?律师.*?辩护人\w{2,4}，.*?律师)', doc_content)
    return gbhr

    
def get_procedure(doc_content):    
    pr = re.findall('\w\w程序', doc_content)
    return pr
    
def get_hyt(doc_content):    
    return re.findall('合议庭', doc_content)
    
    
def bhr_test(doc_content):    
    return re.search('辩护人', doc_content)
    

def bgr_test(doc_content):    
    return re.search('被告人', doc_content)
    
    
    
def load_files(year, court, path=''):
    case_matrix = {}
    count = 0
    print('%s %s %s' % (year, district, path))
    if path:
        for court in district:
            file_list = os.listdir('Download_' + court)
            for file in file_list:
                file_path = path + '/' + year + '/' + d + '/' + file
                
    case_matrix['path']  
    return case_matrix

    
def dump2csv(court, case_matrix, surfix=''):
    file = court + surfix + '.csv'
    print('dump 2 file %s' % file)
    with open(file, 'w', newline='', encoding='utf-8_sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(case_matrix.keys())
        writer.writerows(zip(*case_matrix.values()))



def read_csv(court, surfix=''):
    file = court + surfix + '.csv'
    print('open file %s' % file)
    with open(file, encoding='utf-8_sig') as csvfile:
        reader = csv.DictReader(csvfile)
        case_matrix = dict.fromkeys(reader.fieldnames)
        for key in case_matrix:
            case_matrix[key] = []
        for row in reader:
            for key in case_matrix:
                case_matrix[key].append(row[key])

        if not 'sws' in case_matrix.keys():
            col_list = ['bgrt', 'bhrt',
                        'bgr', 'bgr_n',
                        'wtbhr', 'wtbhr_n', 
                        'zdbhr', 'zdbhr_n',
                        'sws', 'sws_n',
                        'procedure', 'hyt',
                        'gbhr']
            for key in col_list:
                case_matrix[key] = [''] * len(case_matrix['name'])

        

        
    return case_matrix

        
def file_analyse(court, case_matrix):
    count = len(case_matrix['name'])
    analyser = DocAnalyser.DocAnalyser()
    for i in range(count):
        print('%s/%s' % (i, count))
        file_name = court + '\\' + case_matrix['name'][i] + case_matrix['date'][i] + '.docx'
        print(file_name)
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
        
        for p in range(len(analyser.procedure)):
            case_matrix['procedure'][i] += analyser.procedure[p]
            case_matrix['procedure'][i] += ', '
        case_matrix['procedure'][i] = case_matrix['procedure'][i][:-2]
        
        
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
    return case_matrix
        
def combine(path, file_list):
    case_matrix = read_csv((path + file_list[0]), '_result')
    for file in file_list[1:]:
        case_matrix_t = read_csv((path + file), '_result')
        #print(case_matrix_t)
        for key in case_matrix_t:
            case_matrix[key] += case_matrix_t[key]
        
    dump2csv('C:\\Users\\lij37\\Code\\Summer\\Total_', case_matrix,  '_result')
        
def main():    
    desc = ""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-y', '--year', action='store')
    parser.add_argument('-d', '--district', action='store')
    parser.add_argument('-p', '--path', action='store')
    parser.add_argument('-c', '--court', action='store')
    parser.add_argument('-a', '--append', action='store_true')
    
    args = parser.parse_args()
    if args.append:
        path = 'C:\\Users\\lij37\\Code\\Summer\\'
        court_list = ['青川县人民法院', '成都市金牛区人民法院']
        combine(path, court_list)
        sys.exit(0)
#    if args.copy:
#        file_list = os.listdir(args.copy)
#        for file in file_list:
#            copyfile(args.copy + '/' + file, args.copy + '/' + file[:-4] + '.doc')
#            os.remove(args.copy + '/' + file)
#        sys.exit(0)    
    #court = 'C:\\Users\\lij37\\Code\\Summer\\2016\\' + args.court
    
    court = 'C:\\Users\\lij37\\Code\\Summer\\' + args.court
    #file_list = os.listdir('成都市金牛区人民法院')
    #for file in file_list:
    #    copyfile('成都市金牛区人民法院/' + file, '成都市金牛区人民法院/' + file[:-4] + '.doc')
    
    #file_list = load_files(args.year, args.district, args.path)
    #file_analyse(file_list)
    #t = read_csv('test')
    #dump2csv('test', t)
    case_matrix = read_csv(court)
    #print(case_matrix)
    case_matrix_n = file_analyse(court, case_matrix)
    #print(case_matrix)
    dump2csv(court, case_matrix_n,  '_result')
    
if __name__ == "__main__":
    main()