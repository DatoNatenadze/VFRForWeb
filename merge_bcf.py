#!/usr/bin/python
import sys
import numpy


def read_bcf_header(fi):
    size = numpy.fromstring(fi.read(8), dtype=numpy.int64)
    offsets = numpy.fromstring(fi.read(size * 8), dtype=numpy.int64)
    return size, offsets


if __name__ == "__main__":
    bcf_files = sys.argv[3:]

    sizes = numpy.int64([])
    offsets = numpy.int64([])
    for f in bcf_files:
        fi = open(f)
        s, o = read_bcf_header(fi)
        sizes = numpy.append(sizes, s)
        offsets = numpy.append(offsets, o)
        fi.close()

    # Write merged BCF file
    fo = open(sys.argv[1], 'wb')
    fo.write(numpy.sum(sizes))
    fo.write(offsets)
    for f in bcf_files:
        fi = open(f)
        read_bcf_header(fi)  # skip header
        fo.write(fi.read())
        fi.close()
    fo.close()

    # Write size file
    fo = open(sys.argv[2], 'wb')
    fo.write(sizes)
    fo.close()
