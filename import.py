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

# NULLBYTES
# 룬팩토리2는 항상 00 이고
# 룬팩토리3는 메인대사는 00,
# 그 외 대사는 0000 으로 하면 됩니다.

NULLBYTES = "00"
REPLACE = True
tbldict = {}
tbldict[" "] = "20"
tbldict["　"] = "E38080"
tbldict["="] = "3D"
replacedict = {
    "A": "Ａ", "B": "Ｂ", "C": "Ｃ", "D": "Ｄ", "E": "Ｅ", "F": "Ｆ", "G": "Ｇ",
    "H": "Ｈ", "I": "Ｉ", "J": "Ｊ", "K": "Ｋ", "L": "Ｌ", "M": "Ｍ", "N": "Ｎ",
    "O": "Ｏ", "P": "Ｐ", "Q": "Ｑ", "R": "Ｒ", "S": "Ｓ", "T": "Ｔ", "U": "Ｕ",
    "V": "Ｖ", "W": "Ｗ", "X": "Ｘ", "Y": "Ｙ", "Z": "Ｚ", "a": "ａ", "b": "ｂ",
    "c": "ｃ", "d": "ｄ", "e": "ｅ", "f": "ｆ", "g": "ｇ", "h": "ｈ", "i": "ｉ",
    "j": "ｊ", "k": "ｋ", "l": "ｌ", "m": "ｍ", "n": "ｎ", "o": "ｏ", "p": "ｐ",
    "q": "ｑ", "r": "ｒ", "s": "ｓ", "t": "ｔ", "u": "ｕ", "v": "ｖ", "w": "ｗ",
    "x": "ｘ", "y": "ｙ", "z": "ｚ", "0":"０", "1":"１", "2":"２", "3":"３",
    "4":"４", "5":"５", "6":"６", "7":"７", "8":"８", "9":"９", ":":"：", "·":"･",
}
replacedict_to_2byte = {
    "？": "?", "！": "!", "（": "(", "）": ")", "，": ",", "．": ".",
    "：": ":", "；": ";",
    "。": ".", "、": ","
}
replacestr_2byte = "？！（），．：；？。、"
replacestr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789:·"
hexlist = []
valuelist = []
index=0
lengths=[]
offsets=[]


def readtable(tbl):
    global tbldict
    global hexlist
    global valuelist
    with open(tbl, "r", encoding="utf-8") as f:
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
            tbldict[_word] = _hex
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
    index = len(tlines)
    print(index)
    for i in range(index):
        line = lines[i].replace("\\n", "_").replace("\n","").replace(u"\xa0"," ")
        thex = ""
        for j in line:
            try:
                if REPLACE:
                    if j in replacestr:
                        char = replacedict[j]
                    elif j in replacestr_2byte:
                        char = replacedict_to_2byte[j]
                    else:
                        char = j
                else:
                    if j in replacestr_2byte:
                        char = replacedict_to_2byte[j]
                    else:
                        char = j
                # key = valuelist.index(j)
                # print(j, tbldict[j])
                thex += tbldict[char]
            except:
                print(line)
                print("알 수 없는 에러! 특정한 글자가 테이블에 없습니다.")
                raise
        thex += NULLBYTES
        hexs.append(thex)
        if i == 0:
            offsets.append(8 + (index*8))
        else:
            offsets.append(offsets[i-1] + lengths[i-1] + (len(NULLBYTES) // 2))

        lengths.append((len(thex) // 2) - (len(NULLBYTES) //2 ))
    
    # Write 
    _out.write("TEXT".encode("ascii"))
    _out.write(struct.pack("<I",index))
    
    for i in range(index):
        _out.write(struct.pack("<I", lengths[i]))
        _out.write(struct.pack("<I", offsets[i
        ]))
    
    for i in range(index):
        _out.write(shex2bhex(hexs[i]))
        
if __name__ == "__main__":
    try:
        infile = sys.argv[1]
    except:
        infile = input("텍스트 파일을 선택해주세요\n")
    try:
        outfile = sys.argv[2]
    except:
        outfile = infile + ".out"
    try:
        tblfile = sys.argv[3]
    except:
        tblfile = input("테이블 파일을 선택해주세요\n")
    readtable(tblfile)
    instream = open(infile, "r", encoding="utf-8")
    outstream = open(outfile, "wb")
    write(instream, outstream)
    instream.close()
    outstream.close()