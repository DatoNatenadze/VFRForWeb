#!/usr/bin/python
import glob
import os
import sys
import numpy

def make_bcf_header(files):
    result = numpy.int64(len(files))
    for f in files:
        result = numpy.append(result, os.stat(f).st_size)
    return result

def make_bcf_body(files):
    str_list = []
    for f in files:
        fi = open(f, 'rb')
        str_list.append(fi.read())
        fi.close()
    return ''.join(str_list)
    
def write_bcf_body(files, fo):
    str_list = []
    for f in files:
        fi = open(f, 'rb')
        fo.write(fi.read())
        fi.close()
    return ''.join(str_list)
    
if __name__ == "__main__":
    files = []
    for f in sys.argv[2:]:
        files.extend(glob.glob(f))
    #print "%d files" % len(files)
    fo = open(sys.argv[1], 'wb')
    fo.write(make_bcf_header(files))
    #fo.write(make_bcf_body(files)) #In-memory version
    write_bcf_body(files, fo)
    fo.close()
