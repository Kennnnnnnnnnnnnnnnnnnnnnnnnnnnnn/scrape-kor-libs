import os
import sys
import argparse
import time

from title import stripTitle
from libs import *
from files import *
'''
pyinstaller -F -w --exclude numpy main.py
pyinstaller -F -w --exclude numpy --add-binary  "chromedriver.exe;." main.py
'''

list_black_prefix = [ 'ping ']
list_black_in = [ '#' ]


def getArgs():
    parser = argparse.ArgumentParser(description='[[ Help ]]')

    parser.add_argument('-i', '--file_in', default='input.xlsx',
                        type=str, help='choose input file')
    parser.add_argument('-o', '--file_out', default='input.xlsx',
                        type=str, help='choose output file')
    '''
    parser.add_argument('-i', '--file_in', default='vector_in_short.xml',
                        type=str, help='choose input file')
    parser.add_argument('-o', '--file_out', default='vector_out_short.xml',
                        type=str, help='choose output file')
    '''
    '''
    parser.add_argument('-i', '--file_in', default='vector_in.xml', type=str, help='choose input file')
    parser.add_argument('-o', '--file_out', default='vector_out.xml', type=str, help='choose output file')
    '''

    parser.add_argument('-m', '--filter', default='pat1', type=str, choices=['normal', 'pat1'], help='choose title filter')
    parser.add_argument('-v', '--verbose', default=0, type=int, help='show detailed information')
    parser.add_argument('-f', '--bit_flag', default=0, type=int)

    return parser.parse_args()

def iterateCreate(obj, item, _list, flag):
    obj.create_values('name')
    obj.create_values('valid')

    # instantiate available libraries
    title = obj.get_value_iter('name')
    valid = obj.get_value_iter('valid')
    while title != 'END' and title != '':
        if valid == 'O':
            obj1 = item.create(_list, title, flag)
            if not obj1 is None:
                obj1.addBlacks(list_black_prefix, list_black_in)
        # print("build: %s, %s" % (name, valid))
        title = obj.get_value_iter('name')
        valid = obj.get_value_iter('valid')

def createLibs(obj, _list, flag):
    name = obj.get_dir_iter()
    while name.startswith("지역_"):
        area = name.split('_')[1]
        for item in list_a_libs:
            if area == item.area_name:
                iterateCreate(obj, item, _list, flag)
        name = obj.get_dir_iter()

def buildLists(obj, _list_kwd, _list_author):
    obj.set_dir('keyword')
    obj.create_values('title')
    obj.create_values('author')

    title = obj.get_value_iter('title')
    author = obj.get_value_iter('author')
    # print("build: %s, %s" % (title, author))
    while isinstance(author, str) and title != 'END' and title != '':
        # print("build: %s" % (val))
        _list_kwd.append(title)
        _list_author.append(author)
        # print("-- build: %s, %s" % (title, author))
        title = obj.get_value_iter('title')
        author = obj.get_value_iter('author')

def main():
    start = time.time()
    args = getArgs()
    path_in = args.file_in
    path_out = args.file_out
    flag = args.bit_flag
    # use xml as test vectors
    if os.path.splitext(path_in)[1] == '.xml':
        flag = flag | BIT_LIB_FLAG_IGNORE_EXISTENCE

    list_kwds = list()
    list_author = list()
    list_libs = list()

    ### open source file and get active libraries
    iofile = None
    for item in list_a_files:
        iofile = item.create(path_in, path_out, list_libs)
        if not iofile is None:
            break
    if iofile is None:
        print("%s or %s has an extention that isn't supported " % (path_in, path_out))
        sys.exit(1)

    ### build libraries
    createLibs(iofile, list_libs, flag)
    buildLists(iofile, list_kwds, list_author)

    worstSearchedKeyword = ""
    worstSearchedNum = 0
    total = 0
    for place in list_libs:
        print("[[ %s ]]" % place.name)
        iofile.init_result(place.name)

        totalEntries = 0
        for _title, _author in zip(list_kwds, list_author):
            adv = 0
            author = ''
            if isinstance(_author, str) and _author != '':
                adv = 1
                author = _author

            totalEntries += 1
            iofile.create_keyword_iter(totalEntries)
            title = _title
            if args.filter == 'pat1':
                title = stripTitle(title)
            # for too long book name
            if len(title) > 70:
                title = title[:69]
            # print("%d: %s %s %s" % (totalEntries, _title, title, author))
            iofile.insert_keyword_iter(_title)
            iofile.insert_keyword_iter(title)
            iofile.insert_keyword_iter(author)

            if place.checkTitle(title):
                continue

            # start getting records
            url = place.getUrl(adv, title, author)
            totalNumBooks_org = totalNumBooks = place.getTotalNumBooks(url)
            total += totalNumBooks
            if totalNumBooks > worstSearchedNum:
                worstSearchedKeyword = title
                worstSearchedNum = totalNumBooks

            res_searched = "Keyword: %s, %d books searched" % (title, totalNumBooks)
            if adv == 1:
                res_searched += " (author: %s)" % author
            print(res_searched)
            page = 1
            while totalNumBooks > 0:
                url_cur = place.getUrlPerPage(url, page)
                print("++ %s" % url_cur) ###
                numBooks = place.createBooks(url_cur)
                # print("tt %d / %d" % (numBooks, totalNumBooks)) ###
                totalNumBooks -= numBooks

                for i in range(0, numBooks):
                    list_val = []
                    place.setValues(list_val, i)
                    iofile.create_value_iter(totalEntries + i)
                    # print("tt %d " % (totalEntries + i))
                    for cell_data in list_val:
                        iofile.insert_value_iter(cell_data)
                totalEntries += numBooks
                page += 1
            if totalNumBooks_org != 0:
                totalEntries -= 1
        print("")

    end = time.time()
    del iofile
    print("\nTotal %d gathered successfully (%f secs)!!!" % (total, end - start))
    if worstSearchedNum != 0:
        print("- '%s' mostly searched: %d books \n" % (worstSearchedKeyword, worstSearchedNum))
    # os.system('pause')
    os.system(r'input.xlsx')

if __name__ == '__main__':
    main()
