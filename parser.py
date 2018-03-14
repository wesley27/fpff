#!/usr/bin/env python2

import sys
import struct
from datetime import datetime

""" Known data constants. """
MAGIC = 0xbefedade
VERSION = 1

""" Known byte constants. """
WORD = 4
DWORD = 8
DOUBLE = 8
SECT_BASE = 2 * WORD

INC = 0

""" Exits program when som ething fails. """
def err(msg):
    sys.exit(msg)

""" Obtain header data from file. """
def parse_header(data):
    global INC
    magic, version = struct.unpack('<LL', data[INC:2 * WORD])
    INC += 2 * WORD

    timestamp,  = struct.unpack('<L', data[INC:INC+WORD])
    INC += WORD

    author, = struct.unpack('8s', data[INC:INC+DWORD])
    INC += DWORD

    nsects, = struct.unpack('<L', data[INC:INC+WORD])
    INC += WORD

    #confirm accuracy of header values
    if magic != MAGIC:
        err('Bad magic! Got %s, expected %s' % (hex(magic), hex(MAGIC)))
    if version != VERSION:
        err('Bad version! Got %d, expected %d' % (int(version), int(VERSION)))
    if timestamp < 0 or timestamp > 2147483647:
        err('Bad timestamp! Got %d. This cannot be unix time.' % timestamp)
    if not all(ord(c) < 128 for c in str(author)):
        err('Bad author! Got %s, which includes non-ASCII characters.')
    if nsects < 0:
        err('Bad section count! God %d, expected something > 0.' % nsects)


    print('------- File Header -------')
    print('Magin: %s' % hex(magic))
    print('Version: %d' % version)
    print('Unix Timestamp: %d\nStandard Timestamp: %s' % (timestamp, datetime.fromtimestamp(timestamp)))
    print('Author: %s' % author)
    print('Section Count: %d' % nsects)

    return nsects

""" Obtain body data from file. """
def parse_body(data, nsects):
    global INC

    loc = INC
    vals = ['-------  File Body  -------']
    png_num = 0 # tracks number of png images found to allow auto-saving of parsed PNGs

    while loc < len(data):
        stype, slen = struct.unpack('<LL', data[INC:INC + SECT_BASE])
        INC += SECT_BASE

        if slen != 0:
            if stype == 1:
                svalue, = struct.unpack('<%ds' % slen, data[INC:INC + slen])
                if not all(ord(c) < 128 for c in str(svalue)):
                    err('Bad value in ASCII section at position: %d. %s is not ASCII.' % (INC, svalue))
                vals.append(('ASCII: %s' % svalue).strip())
            if stype == 2:
                svalue, = struct.unpack('<%ds' % slen, data[INC:INC + slen])
                try:
                    str(svalue).decode('utf-8')
                except UnicodeError:
                    err('Bad value in UTF-8 section at position: %d. %s is not UTF-8.' % (INC, svalue))
                vals.append('UTF-8: %s' % svalue)
            if stype == 3:
                svalue = struct.unpack('<%dL' % (slen/4), data[INC:INC + slen])
                vals.append('Words: %s' % str(svalue))
            if stype == 4:
                svalue = struct.unpack('<%dQ' % (slen/8), data[INC:INC + slen])
                vals.append('Double Words: %s' % str(svalue))
            if stype == 5:
                svalue = struct.unpack('<%dQ' % (slen/8), data[INC:INC + slen])
                vals.append('Doubles: %d' % svalue)
            if stype == 6:
                sval1, sval2 = struct.unpack('<dd', data[INC:INC + slen])
                if sval1 < -90 or sval1 > 90:
                    err('Bad coordinates! %d is not a valid latitudinal coordinate!' % sval1)
                if sval2 < -180 or sval2 > 180:
                    err('Bad coordinates! %d is not a valid longitudinal coordinate!' % sval2)
                vals.append('Coordinates: (%s, %s)' % (sval1, sval2))
            if stype == 7:
                if slen != 4:
                    err('Bad section length! Got %d, expected 4!' % slen)
                svalue, = struct.unpack('<L', data[INC:INC + WORD])
                if svalue < 0 or svalue > nsects-1:
                    err('Bad section index! %d is not a valid section index' % svalue)
                vals.append('Section Index: %s' % svalue)
            if stype == 8:
                svalue = struct.unpack('%dB' % slen, data[INC:INC + slen])
                png = (0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A) + svalue
                with open('./%d.png' % png_num, 'w') as f:
                    f.write(struct.pack('<%dB' % len(png), *png))
                    f.close()
                vals.append('PNG: PNG section found, PNG saved to ./%d.png' % png_num)
                png_num += 1

            INC += slen
            loc = INC
    for s in vals:
        print(s)

""" Main program execution. """
def main():
    # ensure script was executed properly
    if len(sys.argv) is not 2:
        err('./parser.py input_file.fpff')
    
    # open fpff and get contents
    with open(sys.argv[1], 'rb') as rcff:
        data = rcff.read()

    print('')
    nsects = parse_header(data)
    parse_body(data, nsects)
    print('')

main()
