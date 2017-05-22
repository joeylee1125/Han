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
import CourtList


def get_case_info(wenshu, start_items, total_items):
    wenshu.getCaseList(start_items, total_items)


    
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
            with open(file_name, "wb") as word_doc:
                word_doc.write(wenshu.content)
            time.sleep(1)
        elif os.path.getsize(file_name) < 20000:
            with codecs.open(file_name, "r", "utf-8") as f:
                if not 'DOC' in f.readline():
                    wenshu.downloadDocument(path,
                                            case_matrix[col_name][i],
                                            case_matrix[col_id][i],
                                            case_matrix[col_date][i])
                    with open(file_name, "wb") as word_doc:
                        word_doc.write(wenshu.content)
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
    with open(surfix + '.csv', 'w', newline='', encoding='utf-8_sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(case_matrix.keys())
        writer.writerows(zip(*case_matrix.values()))


def read_csv(surfix):
    with open(surfix + '.csv', encoding='utf-8_sig') as csvfile:
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
    print('phase1 %s' % court)
    case_matrix = {}
    #dump2csv(case_matrix, court)
    # Get 2nd case list with search criteria.
    wenshu = Spider.WenShu()
    wenshu.setSearchCriteria(search_criteria)
    wenshu.getTotalItemNumber()
    print("Total case number is %s" % wenshu.total_items)
    get_case_info(wenshu, 1, wenshu.total_items)
    case_matrix['name'] = wenshu.case['name']
    case_matrix['doc_id'] = wenshu.case['doc_id']
    case_matrix['date'] = wenshu.case['date']
    case_matrix['case_id'] = wenshu.case['case_id']
    case_matrix['procedure'] = wenshu.case['procedure']
    case_matrix['court'] = wenshu.case['court']
    
    print('%s %s' % (wenshu.total_items, len(case_matrix['name'])))
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
    dump2csv(case_matrix, court)


def phase2(search_criteria, court):
    print('phase2 %s' % court)
    # Read csv file and get case list.
    case_matrix = read_csv(court)
    wenshu = Spider.WenShu()
    wenshu.setSearchCriteria(search_criteria)
    #print(case_matrix['name2'])
    download_case(wenshu, case_matrix, court)
    #dump2csv(case_matrix, 'phase2_' + court)
    
def phase3(court):
    #case_matrix = read_csv('phase1_' + court)
    #wenshu = Spider.WenShu()
    #wenshu.setSearchCriteria(search_criteria)
    #print(case_matrix['name2'])
    #download_case(wenshu, case_matrix, court)
    #dump2csv(case_matrix, 'phase2_' + court)
    #case_matrix = read_csv(court)
    #wenshu = Spider.WenShu()
    #wenshu.setSearchCriteria(search_criteria)
    #total_number = wenshu.getTotalItemNumber()
    #print('%s %s' % (total_number, len(case_matrix['name'])
    #sys.exit(0)
    #if int(total_number) == len(case_matrix['name']):
    file_list = os.listdir('.')
    for file in file_list:
        if file[-3:] == 'csv':
            case_matrix = read_csv(file[:-4])
            if len(case_matrix['name']) == 20:
                print(file)
                os.remove(file)

                #print(case_matrix['name'])

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
    parser.add_argument('-l', '--court_list', action='store')    
    args = parser.parse_args()
    #search_criteria = "案件类型:刑事案件,审判程序:一审,法院地域:四川省,裁判年份:2016,文书类型:判决书," + "基层法院:" + args.court
    #search_criteria = "案件类型:刑事案件,审判程序:一审,法院地域:四川省,裁判年份:2016,文书类型:判决书,法院层级:中级法院," + "中级法院:" + args.court
    if args.phase == 'all':
        for court in CourtList.court_list[int(args.court_list)]:
            search_criteria = "案件类型:刑事案件,审判程序:一审,法院地域:四川省,裁判年份:2015,文书类型:判决书," + "基层法院:" + court
            csv_file = court + '.csv'
            if not os.path.exists(csv_file):
                phase1(search_criteria, court)
            else:
                phase2(search_criteria, court)
                #phase3(search_criteria, court)
        
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
