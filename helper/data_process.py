#!/usr/bin/python
# encoding=utf8
__author__ = 'fucus'
import os
import sys

if len(sys.argv) < 2:
    print "usage: ./data_process.py {file_path}"
    print "example:"
    print "./data_process.py /Users/fucus/Desktop/SogouQ.sample"
    exit()
test_file_path = sys.argv[1]

check_after_process = True
if len(sys.argv) > 2 and sys.argv[2] == 'force':
    check_after_process = False

after_process_file_path = '%s.after_process' % test_file_path
if check_after_process and os.path.exists(after_process_file_path):
    print "file %s already exists" % after_process_file_path
    exit()

after_file = open(after_process_file_path, 'w')
for line in open(test_file_path):
    split_line = line.split('\t')
    query = split_line[2].decode('gbk').rstrip(']').lstrip('[')
    doc = split_line[4].rstrip('\n')
    after_file.write('%s\t%s\n' % (doc, query.encode('utf8')))
after_file.close()
