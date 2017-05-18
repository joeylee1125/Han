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

import Spider
import Court


def get_case_info(wenshu, start_items, total_items):
    wenshu.getCaseList(start_items, total_items)

def get_doc_info(doc_name):
    name_list = ['刘正贵、刘正友犯故意伤害罪二审刑事判决书',
                 '吉马吉波犯运输毒品罪二审刑事判决书',
                 '周建刚犯故意杀人罪复核刑事判决书',
                 '孙西华犯故意伤害罪二审刑事判决书',
                 '张洪华犯故意伤害罪二审刑事附带民事判决书',
                 '朱秀英等私分国有资产二审刑事判决书',
                 '李东科等人故意伤害案二审刑事判决书',
                 '李兴云、谢瑞有、赖永辉犯故意杀人罪二审刑事判决书',
                 '李廷才、崔毕美犯故意杀人罪二审刑事附带民事判决书',
                 '汪思春故意杀人案二审刑事判决书',
                 '洞底故意杀人二审刑事裁定书',
                 '潘凤英犯故意杀人罪二审刑事判决书',
                 '王维杰犯故意伤害罪二审刑事判决书',
                 '罗鹏犯故意伤害罪二审刑事判决书',
                 '辛磊磊等贩卖毒品案二审刑事判决书',
                 '郭洪、朱家、王青龙、刘坤、谢红梅、曾清、蒲建国犯故意杀人罪刑...',
                 '钟新海等制造毒品二审刑事裁定书',
                 '陈太兵故意杀人案刑附民判决书',
                 '雷平华、任东东犯贩卖、运输毒品罪二审刑事裁定书']
    
    for i in range(len(name_list)):
        print(name_list[i])
        doc = Spider.DocAnalyser()
        doc.analyseDoc(name_list[i])
        print('')
        print('')
        #wt = doc.getWeituoBianhuren()
        #zd = doc.getZhidingBianhuren()
        #bg = doc.getBeigaoren()
        #print('%s         %s' % (name_list[i], wt))
        #print('%s         %s' % (name_list[i], zd))
    #print(doc.content)
    #doc = Spider.DocAnalyser()
    #doc.analyseDoc('', '吉马吉波犯运输毒品罪二审刑事判决书')
    #wt = doc.getWeituoBianhuren()
    #zd = doc.getZhidingBianhuren()
    #bg = doc.getBeigaoren()
    
    #print(wt)

    
def analyse_case(case_matrix, round):    
    path = 'Download' + str(round) + '/'
    col_name = 'name' + str(round)
    col_date = 'date' + str(round)
    doc = Spider.DocAnalyser()
    for i in range(len(case_matrix[col_name])):
        file_name = path + case_matrix[col_name][i] + case_matrix[col_date][i] + '.docx'
        print(file_name)
        doc.analyseDoc(file_name)
        print('')
        print('')
        print('')
        print('')
        
    
def download_case(wenshu, case_matrix, court):
    path = 'Download_' + court + '/'
    col_name = 'name'
    col_id = 'doc_id'
    col_date = 'date'
    row_count = len(case_matrix[col_name])
    download_list = ['Y'] * row_count

    if not os.path.exists(path):
        os.makedirs(path)
    for i in range(row_count):
        
        print("%s/%s"%(i, row_count))
        file_name = path + case_matrix[col_name][i] + case_matrix[col_date][i] + '.txt'
        if not os.path.exists(file_name):
            wenshu.downloadDocument(path,
                                    case_matrix[col_name][i],
                                    case_matrix[col_id][i],
                                    case_matrix[col_date][i])
            time.sleep(1)
        elif os.path.getsize(file_name) < 20000:
            with codecs.open(file_name, "r", "utf-8") as f:
                if not 'DOC' in f.readline():
                    wenshu.downloadDocument(path,
                                            case_matrix[col_name][i],
                                            case_matrix[col_id][i],
                                            case_matrix[col_date][i])
                    time.sleep(1)                        
        else:
            pass
             
        #if not os.path.exists(file_name):
               
            #doc_size = 0
            #attempts = 0
            #while doc_size < 80000 and attempts < 3:
            #    wenshu.downloadDocument(path,
            #                            case_matrix[col_name][i],
            #                            case_matrix[col_id][i],
            #                            case_matrix[col_date][i])
            #    time.sleep(1)                        
            #    doc_size = os.path.getsize(file_name)
                #print('doc %s size is %s' % (case_matrix[col_name][i], doc_size))
            #    attempts += 1
        #doc_size = os.path.getsize(file_name)
        #if  doc_size < 80000:
        #    print('docsize is %s, doc %s may corrupt' % (doc_size, case_matrix[col_name][i]))
        #    download_list[i] = 'N'
    return download_list
    
    
def dump2csv(case_matrix, surfix):
    with open('case' + surfix + '.csv', 'w', newline='', encoding='utf-8_sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(case_matrix.keys())
        writer.writerows(zip(*case_matrix.values()))


def read_csv(surfix):
    with open('case' + surfix + '.csv', encoding='utf-8_sig') as csvfile:
        reader = csv.DictReader(csvfile)
        case = dict.fromkeys(reader.fieldnames)
        for key in case:
            case[key] = []
        #print(case)
        for row in reader:
            for key in case:
                case[key].append(row[key])
    return case    


def copy_files():
    pass
    
# Phase 1: Search and get 2nd case list,
#          dump case name list into a csv file.
def phase1(search_criteria, court):
    case_matrix = {}
    # Get 2nd case list with search criteria.
    wenshu = Spider.WenShu()
    wenshu.setSearchCriteria(search_criteria)
    wenshu.getTotalItemNumber()
    print("Total case number is %s" % wenshu.total_items)
    get_case_info(wenshu, 1, wenshu.total_items)
    case_matrix['name'] = wenshu.case['name']
    case_matrix['doc_id'] = wenshu.case['doc_id']
    case_matrix['date'] = wenshu.case['date']
    #row_count = len(case_matrix['name'])
    #pop_count = 0
    #print('row count %s' % row_count)
    #for i in range(row_count):
        #print(i)
    #    if '附带民事' in case_matrix['name2'][i - pop_count]:
            #print('hahaha')
    #        for key in case_matrix:
    #            case_matrix[key].pop(i - pop_count)
    #        pop_count += 1
    dump2csv(case_matrix, 'phase1_' + court)


def phase2(search_criteria, court):
    # Read csv file and get case list.
    case_matrix = read_csv('phase1_' + court)
    wenshu = Spider.WenShu()
    wenshu.setSearchCriteria(search_criteria)
    #print(case_matrix['name2'])
    case_matrix['download2'] = download_case(wenshu, case_matrix, court)
    dump2csv(case_matrix, 'phase2_' + court)

    
def phase3(doc_num):
    case_matrix = read_csv('phase2' + str(doc_num))
    analyse_case(case_matrix, 2)
    

def phase5(court_list):
    for court in court_list:
        file_list = os.listdir('Download_' + court)
        for file in file_list:
            copyfile('Download_' + court + '/' + file, 'CasePool/' + file[:-4] + '.doc')
            #if os.path.getsize('Download_' + court + '/' + file) < 100000:
            #    copyfile('Download_' + court + '/' + file, 'CasePool/' + file[:-4] + '.doc')
            #else:
            #    copyfile('Download_' + court + '/' + file, 'CasePool/' + file[:-4] + '.docx')

    
def main():
    desc = "Select a phase to run"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-p', '--phase', action='store')
    parser.add_argument('-d', '--doc', action='store')
    parser.add_argument('-c', '--court', action='store')
    args = parser.parse_args()
    search_criteria = "案件类型:刑事案件,审判程序:一审,法院地域:四川省,裁判年份:2016,文书类型:判决书," + "基层法院:" + args.court
    if args.phase == 'all':
        pass
    elif args.phase == '1':
        print('phase 1')
        phase1(search_criteria, args.court)
    elif args.phase == '2':
        print('phase 2')
        phase2(search_criteria, args.court)
    elif args.phase == '3':
        print('phase 3')
        phase3(args.doc)
    elif args.phase == '4':
        print('phase 4')
        wenshu1 = Spider.WenShu()
        phase4(wenshu, wenshu1)
    elif args.phase == '5':
        for r in Court.region:
            phase5(eval('Court.%s' % r))
    else:
        print('invalid')
    
    
    
if __name__ == "__main__":
    main()
