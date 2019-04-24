#!/usr/bin/python
# generate_bcf.py
import argparse
import bcf

parser = argparse.ArgumentParser()
parser.add_argument('pngdir',help='path to a directory full of pngs')
parser.add_argument('bcfpath',help='path to store bcf files')

args = parser.parse_args()
bcf.make_bcfstore(args.bcfpath,args.pngdir)