#!/usr/bin/python
# generate_bcf.py
import argparse
import os
import numpy
from os.path import join

parser = argparse.ArgumentParser()

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
def ls_png(dir)
	if os.isdir(dir)
		files = [os.path.abspath('%s/%s'%(dir,f) for f in os.listdir(dir)]
		pngfiles = [f for f in files if f.endswith('.PNG') and os.path.isfile(f)]
		return pngfiles
	else:
		return None
	
def make_label(labelStore)
	return numpy.uint32(labelStore)
	
def make_bcfstore(bcfpath, pngdir, test):
	if not test in range(3):
		test = 0
	
	labelStore = 0	
    file_base = {0:'train', 1:'val', 2:'test'}
	for root, dirs ,files in os.walk(pngdir):
		for dir in dirs:
			if dir.endswith('.otf'):
				labelStore++
				
			pngfiles = ls_png(dir)
			if len(pngfiles) > 0:
				os.mkdir(join(bcfpath, dir))
				
				# generate .bcf file
				fo = open(join(join(bcfpath,dir), "%s.bcf"%file_base[test]), "wb")
				fo.write(make_bcf_header(pngfiles))
				fo.write(make_bcf_body(pngfiles))
				fo.close()
				
				# generate .label file
				flabel = open(join(join(bcfpath,dir), "%s.label"%file_base[test]), "wb")
				flabel.write(make_label(labelStore))
				flabel.close()
