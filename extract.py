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
tblfile = None
tbldict = {}
index=0
lengths=[]
offsets=[]
def readtable(tbl):
    global tblfile
    global tbldict
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
    return

def readheader(f):
    global index
    global lengths
    global offsets
    f.seek(4)
    index = struct.unpack("<I", f.read(4))[0]
    for i in range(index):
        f.seek(8 + i * 8)
        length = struct.unpack("<I", f.read(4))[0]
        offset = struct.unpack("<I", f.read(4))[0]
        lengths.append(length)
        offsets.append(offset)
    
def write(_in, _out):
    for i in range(index):
        length = lengths[i]
        offset = offsets[i]
        output = ""
        _in.seek(offset)
        while _in.tell() < offset + length:
            _hex = binascii.hexlify(_in.read(1)).decode("utf-8").upper()
            if _hex == "00":
                break
            
            try:
                output += tbldict[_hex]
            except ValueError:
                _hex += binascii.hexlify(_in.read(2)).decode("utf-8").upper()
                try:
                    output += tbldict[_hex]
                except ValueError:
                    if _in.tell() >= offset + length:
                        break
                    else:
                        print(output)
                        print("UnExcepted Error! Maybe the hex is not in table")
                        print("Hex : " + _hex)
                        input()
                        raise
        _out.write(output)
        _out.write("\n")
        
        
if __name__ == "__main__":
    try:
        infile = sys.argv[1]
    except:
        infile = input("Select input file")
    try:
        outfile = sys.argv[2]
    except:
        outfile = infile + ".out"
    try:
        tblfile = sys.argv[3]
    except:
        tblfile = input("Select tbl file")
    
    instream = open(infile, "rb")
    outstream = open(outfile, "w", encoding="utf-8")
    readheader(instream)
    write(instrea, outstream)
    instream.close()
    outstream.close()
        