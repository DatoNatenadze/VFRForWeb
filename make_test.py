#!/usr/bin/python
# generate_bcf.py
import argparse
from os.path import join, isdir
import os
import make_bcf
import numpy as np
import merge_bcf


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
def readlines(filename):
    """Returns a list of all the lines in a file, except for those starting with a #. 
    filename is a string containing the name of a file. 
    The lines returned must not end in new-line characters."""
    try:
        f = open(filename, "r")
        result = [line.rstrip('\n') for line in f if line.strip()[0] != '#']
        f.close()
        return result  # return
    except EnvironmentError:
        print("Can't read from the file: ", filename)
        return []


def valid_oftfolders(pngdir):
    otffolders = list()

    for otfdir in os.listdir(pngdir):
        otffolders.append(join(pngdir, otfdir))

    return np.sort(otffolders)


def ls_png(dir):
    if os.path.isdir(dir):
        files = [os.path.abspath('%s/%s' % (dir, f)) for f in os.listdir(dir)]
        pngfiles = [f for f in files if f.endswith('.png') and os.path.isfile(f)]
        return pngfiles
    else:
        return []


def make_teststore(bcfpath, pngdir, labelfile):
    # otffolders = [f for f in os.listdir(pngdir) if f.endswith(".otf")]

    otfdirs = valid_oftfolders(pngdir)
    fontlist = readlines(labelfile)

    if not (os.path.exists(bcfpath) and os.path.isdir(bcfpath)):
        os.makedirs(bcfpath)

    try:
        ftest = open(join(bcfpath, "test.bcf"), "wb")
        ftest_label = open(join(bcfpath, "test.label"), "wb")
    except EnvironmentError:
        print("Error occured while opening files...\n")
        return

    imagescount = 0
    for fdir in otfdirs:
        basename, fontnameotf = os.path.split(fdir)
        if fontnameotf in fontlist:
            pngfiles = ls_png(fdir)
            imagescount = imagescount + len(pngfiles)

    print("Total images: %d" % imagescount)
    ftest.seek(8, os.SEEK_SET)

    test_bodyoffset = 8 + 8 * imagescount
    testcount = 0

    for otfdir in otfdirs:
        print("processing %s directory..." % otfdir)

        labelStore = 0
        try:
            basename, fontnameotf = os.path.split(otfdir)
            labelStore = fontlist.index(fontnameotf)

            test_pngfiles = ls_png(otfdir)
            testsizes = np.empty(0, dtype=np.int64)
            testlabels = np.empty(0, dtype=np.uint32)

            for f in test_pngfiles:
                testsizes = np.append(testsizes, np.int64(os.stat(f).st_size))
                testlabels = np.append(testlabels, np.uint32(labelStore))

            ftest.seek(8 + 8 * testcount, os.SEEK_SET)
            ftest.write(testsizes)
            testcount = testcount + len(test_pngfiles)

            ftest.seek(test_bodyoffset, os.SEEK_SET)
            ftest.write(make_bcf.make_bcf_body(test_pngfiles))
            test_bodyoffset = test_bodyoffset + np.sum(testsizes)

            ftest_label.write(testlabels)

        except ValueError:
            print("[ERROR:] %s is not in the fontlist" % fontnameotf)

    ftest.seek(0, os.SEEK_SET)
    ftest.write(np.int64(imagescount))

    ftest.close()
    ftest_label.close()

    print("All done successfully!\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('pngdir', help='path to a directory full of pngs')
    parser.add_argument('bcfpath', help='path to store bcf files')
    parser.add_argument('fontlist', help='path to fontlist file generated from make_fontlist.py')

    args = parser.parse_args()
    make_teststore(args.bcfpath, args.pngdir, args.fontlist)
