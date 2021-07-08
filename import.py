# -*- coding:utf-8 -*-
"""
-------------------룬팩 2,3,4 데이터 구조
맨 처음에 헤더가 남습니다. 리틀엔디안 방식으로 4바이트로 끊어서
[매직스탬프 TEXT]    [총 대사 갯수]   [대사길이]  [대사 시작오프셋]
[대사길이]           [대사 시작오프셋][대사길이]  [대사 시작오프셋]
[대사길이]           [대사 시작오프셋][대사길이]  [대사 시작오프셋]
[대사길이]           [대사 시작오프셋][대사길이]  [대사 시작오프셋]
...
반복입니다.

주의!!!
추출했을때 \n 은 줄띄는 "새줄 문자"라는 것으로 제어코드로 "0A" 입니다
삽입시 이를 replace 해야될겁니다.
"""

import time
import sys
import binascii
import struct
import os
NULLBYTES = "0000"
tblfile = None
tbldict = {}
hexlist = []
valuelist = []
index=0
lengths=[]
offsets=[]


def readtable(tbl):
    global tblfile
    global tbldict
    global hexlist
    global valuelist
    with open(tblfile, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == "" or line is None:
                continue
            if line[0] == "/" or line[0] == "#":
                continue
            if len(line.split("=")) > 2:
                _hex = line.split("=")[0]
                _word = "="
            else: _hex, _word = line.split("=")
            _hex = _hex.upper()
            tbldict[_hex] = _word
    hexlist = list(tbldict)
    valuelist = list(tbldict.values())
    return

def shex2bhex(shex):
    return binascii.unhexlify(shex)

def write(_in, _out):
    hexs = []
    lines = _in.readlines()
    tlines = []
    
    # Temporary save hexes on array
    for line in lines:
        line = line.strip()
        if line == "" or line is None:
            continue
        else:
            tlines.append(line)
    index = len(line)
    for i in range(index):
        line = lines[i].replace("\\n", "_")
        thex = ""
        for j in line:
            try:
                key = valuelist.index(j)
                thex += hexlist[key]
            except:
                raise
        thex += NULLBYTES
        hexs.append(thex)
        if i == 0:
            offsets.append(8 + (index*8))
        else:
            offsets.append(offsets[i-1] + length[i-1] + (len(NULLBYTES) // 2))

        lengths.append((len(thexs) // 2) + (len(NULLBYTES) // 2))
    
    # Write 
    _out.write("TEXT".encode("ascii"))
    _out.write(struct.pack("<I",index))
    
    for i in range(index):
        _out.write(struct.pack("<I", lengths[i]))
        _out.write(struct.pack("<I", lengths[i]))
    
    for i in range(index):
        _out.write(shex2bhex(hexs[i]))
        
if __name__ == "__main__":
    try:
        infile = sys.argv[1]
    except:
        infile = input("Select input file")
    try:
        outfile = sys.argv[2]
    except:
        outfile = infile + ".txt"
    try:
        tblfile = sys.argv[3]
    except:
        tblfile = input("Select tbl file")
    
    instream = open(infile, "w", encoding="utf-8")
    outstream = open(outfile, "wb")
    write(instrea, outstream)
    instream.close()
    outstream.close()