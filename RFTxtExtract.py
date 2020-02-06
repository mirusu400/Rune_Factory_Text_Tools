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

tablefile="수정UTF_일어_대사추출.tbl"
TBLhex=[]
TBLword=[]
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
        TBLword.append(line[1])
        TBLhex.append(line[0])
    return



readfile=sys.argv[1]
try:
    writefile = sys.argv[2]
except IndexError:
    writefile=readfile
    writefile+=".txt"
readTBL("C:/Pythonproj/Rune_Factory_Text_Tools/수정UTF_일어_대사추출.tbl")

Fp = open(readfile, "rb")
outFp = open(writefile, "w", encoding="utf-8")
Fp.seek(0x04)
buf = Fp.read(4)
textIndex = struct.unpack("<I",buf)[0]
outFp.write(str(textIndex))
outFp.write("\n")

textOffset = []
textLength = []

for i in range(0,textIndex):
    Fp.seek(0x08 + i*0x08)
    buf = Fp.read(4)
    textLength.append(struct.unpack("<I",buf)[0])
    buf = Fp.read(4)
    textOffset.append(struct.unpack("<I",buf)[0])
print(textOffset)
print(textLength)
for i in range(0,len(textOffset)):
    offset = textOffset[i]
    length = textLength[i]
    ResultOutput = ""
    Fp.seek(offset)
    while Fp.tell() < (offset + length):
        buf = Fp.read(1)
        ConvHex = binascii.hexlify(buf).decode('utf-8').upper()
        if ConvHex == "00":
            break
        # TempSwitch = 0
        # print(str(k) + "," + str(ConvHex))
        try:
            Temp = TBLhex.index(ConvHex)
            ResultOutput += TBLword[Temp]
        except ValueError:
            buf += Fp.read(2)
            ConvHex = binascii.hexlify(buf).decode('utf-8').upper()
            try:
                Temp = TBLhex.index(ConvHex)
                ResultOutput += TBLword[Temp]
            except ValueError:
                if Fp.tell() >= offset + length:
                    break
                print(ResultOutput)
                print("Error")
                input()
                raise
    print(str(ResultOutput))
    outFp.write(str(ResultOutput) + "\n")
outFp.close()
Fp.close()