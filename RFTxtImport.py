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

tablefile="수정UTF_수정_실전_대사삽입용.tbl"
NULLBYTES = "00"
TBLhex=[]
TBLword=[]
WriteHexArr=[]
WriteOffsetArr=[]
WriteLengthArr=[]
def readTBL(TBL):
    global TBLword
    global TBLhex
    file=open(TBL,"r",encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        if line == "":
            continue
        line = line.replace("\n","")
        line = line.replace(u"\ufeff", '')  # BOM고유오류 조정
        line = line.split("=")
        if line == ['']:
            continue
        TBLword.append(line[1])
        TBLhex.append(line[0])
    print(TBLword)
    print(TBLhex)
    return

def string_hex_to_hex(str, dst):
    for i in range(0, int(len(str)/2)):
        outtemp = int(str[i * 2:i * 2 + 2], 16)
        outtemp2 = struct.pack("B", outtemp)
        dst.write(outtemp2)
readfile=sys.argv[1]
try:
    writefile = sys.argv[2]
except IndexError:
    writefile=readfile
    writefile+=".out"
readTBL(tablefile)

inFp=open(readfile,"r",encoding="utf-8")
outFp=open(writefile,"wb")

lineIndex = int(inFp.readline())

for i in range(0,lineIndex):
    WriteHex = ""
    line = inFp.readline().replace("\n","")
    print(line)
    for j in range(0,len(line)):
        try:
            Temp = TBLword.index(line[j])
            WriteHex += TBLhex[Temp]
        except:
            raise
    WriteHex += (NULLBYTES)
    WriteHexArr.append(WriteHex)
    if i == 0:
        WriteOffsetArr.append(0x08 + (lineIndex * 0x08))
    else:
        WriteOffsetArr.append(WriteOffsetArr[i-1] + WriteLengthArr[i-1] + 1)
    WriteLengthArr.append((len(WriteHex) // 2) - 1)
outFp.write("TEXT".encode('ascii'))
outFp.write(struct.pack("<I",lineIndex))
for i in range(0,lineIndex):
    outFp.write(struct.pack("<I", WriteLengthArr[i]))
    outFp.write(struct.pack("<I", WriteOffsetArr[i]))

for i in range(0,lineIndex):
    string_hex_to_hex(WriteHexArr[i],outFp)
inFp.close()
outFp.close()