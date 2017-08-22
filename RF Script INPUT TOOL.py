# -*- coding:utf-8 -*-
"""
스크립트 인풋 툴입니다
WQSG 형태든 일반 텍스트든 읽어오게 만드는게 목적입니다


★★★ 무조건 인코딩을 UTF-8로 설정해야합니다!!! ★★★
"""
import time
import sys
import struct
global readfile
global writefile
global tablefile
global inFp3
global outFp
def string_hex_to_hex(temps): #string안에 저장된 hex값을 읽어와 쓰게해줍니다.
    print(int(len(temps)/2))
    for i in range(0, int(len(temps)/2)):

        outtemp = int(temps[i * 2:i * 2 + 2], 16)
        print(temps[i * 2:i * 2 + 2])
        outtemp2 = struct.pack("B", outtemp)
        outFp.write((outtemp2))

def tableread():
    global TBLword
    global TBLhex
    inFp4=open(tablefile,"r",encoding='utf-16-le')
    while True:
        line=inFp4.readline()
        line=line.replace("\n","")
        line=line.split("=")
        if (line == ['']):
            break
        line[0] = line[0].replace(u"\ufeff", '') #BOM고유오류 조정
        TBLword.append(line[1])
        TBLhex.append(line[0])
    print(TBLword)
    print(TBLhex)

    return
def countline():
    tempFp = open(readfile, "r",encoding="utf-8")
    temp=0
    while True:
        line = tempFp.readline()
        if not line: break
        if(line[0]!="\n"): #공백 개행일 경우 넘어가버립니다.
            temp+=1
    return temp
def big_to_little_end(tempinput): #빅 엔디안으로 계산된걸 룬팩토리2에 읽을수있게 스몰 엔디안으로 만들어줍니다
    if(len(tempinput)==1):
        output="0"+tempinput+"000000"
    if(len(tempinput)==2):
        output=tempinput[0:2]+"000000"
    if(len(tempinput)==3): #123 -> 23010000
        print("hi")
        output=tempinput[1:3]+"0"+tempinput[0]+"0000"
    if(len(tempinput)==4):
        output=tempinput[2:]+tempinput[0:2]+"0000"
    if(len(tempinput)==5):
        output=tempinput[3:5]+tempinput[1:3]+"0"+tempinput[0]+"00"
    if(len(tempinput)==6):
        output=tempinput[4:6]+tempinput[2:4]+tempinput[0:2]+"00"
    if(len(tempinput)==7):
        output=tempinput[5:7]+tempinput[3:5]+tempinput[1:3]+"0"+tempinput[0]
    if(len(tempinput)==8):
        output=tempinput[6:8]+tempinput[4:6]+tempinput[2:4]+tempinput[0:2]
    output=output.upper()

    return output


readfile=sys.argv[1]
try:
    writefile = sys.argv[2]
except:
    writefile=readfile
    writefile+=".out"
tablefile=sys.argv[3]
inFp=open(readfile,"r",encoding="utf-8")
outFp=open(writefile,"wb")
texts=[]
TBLword = [] #테이블 파일중 단어
TBLhex = [] #테이블 파일중 16진수값
tableread() #테이블파일읽기
tpcountline=countline()

lentexts=hex(tpcountline)
lentexts=(big_to_little_end(lentexts[2:]))
print(lentexts)
outlabel=b'TEXT'
outFp.write(outlabel)
string_hex_to_hex(lentexts) #스트링에 있는값을 그대로 씁니다
string_hex_to_hex("00000000")

tpcountline=hex(tpcountline * 8+8)
tpcountline=big_to_little_end(tpcountline[2:])
string_hex_to_hex(tpcountline)

