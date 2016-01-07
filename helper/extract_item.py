#!/usr/bin/python
__author__ = 'fucus'
from os import listdir
from os.path import isfile, join
from subprocess import call
mypath = '/Users/fucus/Documents/buaa/IR/data'
onlyfiles=[f for f in listdir(mypath) if isfile(join(mypath, f))]
for file_path in onlyfiles:
    if file_path.endswith('decode.filter'):
        print 'process %s' % file_path
        call(['./data_process.py', '%s/%s' % (mypath, file_path), 'force'])