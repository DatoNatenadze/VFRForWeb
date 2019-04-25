#!/usr/bin/python
# generate_fontlist.py
import argparse
import os
from os.path import join
from os.path import isdir
import numpy as np


# Diretory structure
# input parameter : pngdir
# /pngdir
#		/HelveticaLTStd-Comp.otf (directory)
#				/1
#					/0000.png
#						...
#					/1000.png
#				/2
#					/1001.png
#						...
#					/1892.png
#		/HypatiaSansPro-Light.otf (directory)
#				....................

# output parameter: bcfpath
# /bcfpath
#		/HelveticaLTStd-Comp.otf (directory)
#			/1
#				/train.bcf
#				/val.bcf
#				/test.bcf

def ls_png(dir):
    if os.path.isdir(dir):
        files = [os.path.abspath('%s/%s' % (dir, f)) for f in os.listdir(dir)]
        pngfiles = [f for f in files if f.endswith('.png') and os.path.isfile(f)]
        return pngfiles
    else:
        return []


def valid_oftfolders(pngdir):
    otffolders = list()
    for f in os.listdir(pngdir):
        if f.endswith(".otf"):  # yes, it is otf folder
            traindir = join(join(pngdir, f), "train")
            testdir = join(join(pngdir, f), "test")

            train_pngfiles = ls_png(traindir)
            test_pngfiles = ls_png(testdir)
            if isdir(traindir) and isdir(testdir) and len(train_pngfiles) == 1000 and len(test_pngfiles) == 892:
                otffolders.append(f)
    return np.sort(otffolders)


def write_fontnames(pngdir, destfile):
    try:
        fdest = open(destfile, "w")
    except EnvironmentError:
        print("Error occured while opening %s file...\n" % destfile)

    otffolders = valid_oftfolders(pngdir)
    for fontname in otffolders:
        print(fontname)
        fdest.write("%s\n" % fontname[0:(len(fontname) - 4)])


#
#    fdest.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('topdir', help='path to a directory contains fonttype folders')
    parser.add_argument('destfile', help='file path to store fontnames')

    args = parser.parse_args()
    write_fontnames(args.topdir, args.destfile)
