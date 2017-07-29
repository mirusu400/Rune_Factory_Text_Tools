# -*- coding:utf-8 -*-
"""
-------------------구조
맨 처음 포인터를 찾고(foundoffset) 대사를 찾은후 포인터를 찾고(nextoffset) 이를 txt에 기록합니다.
유니코드일경우 TBL을 탐색하여 그 TBL에 해당하는 글자가 있으면 그 TBL로 추출하고 없을경우 오류메세지를 띄우는 기능입니다(예정)
"""

global readfile
global writefile
global tablefile
global inFp3

import time
import sys


def foundoffset(inFp):
    blank=[]
    inFp = open(readfile, "rb")
    inFp.read(0xC)
    for i in range(1,5):
        startpath=inFp.read(1)
        temp=hex(ord(startpath))
        if(temp=="0x0"):
            temp="0x00"
        blank.append(temp) #각각 읽어 blank에 추가
    blank.reverse() #리틀엔디안->빅엔디안
    pointer=""
    pointer += blank[0]
    pointer += blank[1]
    pointer += blank[2]
    pointer += blank[3]
    pointer=pointer.replace("0x","")
    result="0x"+pointer
    inFp.close()
    return int(result,16)

def nextoffset(nextoffset):
    blank=[]
    inFp3.read(nextoffset)
    for i in range(1,5):
        startpath=inFp3.read(1)
        temp=hex(ord(startpath))
        if(temp=="0x0"):
            temp="0x00"
        if(temp=="0x1"):
            temp="0x01"
        if(temp=="0x2"):
            temp="0x02"
        if(temp=="0x3"):
            temp="0x03"
        if(temp=="0x4"):
            temp="0x04"
        if(temp=="0x5"):
            temp="0x05"
        if(temp=="0x6"):
            temp="0x06"
        if(temp=="0x7"):
            temp="0x07"
        if(temp=="0x8"):
            temp="0x08"
        if(temp=="0x9"):
            temp="0x09"
        if(temp=="0xa"):
            temp="0x0A"
        if(temp=="0xb"):
            temp="0x0B"
        if(temp=="0xc"):
            temp="0x0C"
        if(temp=="0xd"):
            temp="0x0D"
        if(temp=="0xe"):
            temp="0x0E"
        if(temp=="0xf"):
            temp="0x0F"
        blank.append(temp) #각각 읽어 blank에 추가

    blank.reverse() #리틀엔디안->빅엔디안
    pointer=""
    pointer += blank[0]
    pointer += blank[1]
    pointer += blank[2]
    pointer += blank[3]
    pointer=pointer.replace("0x","")
    result=""
    result+=pointer
    result=result.upper()

    return result

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

readfile=sys.argv[1]
try:
    writefile = sys.argv[2]
except:
    writefile=readfile
    writefile+=".txt"
tablefile=sys.argv[3]
inFp=0
texts=[]
longoffset=0 #시작부터 끝까지 0으로 초기화가 안됨
shortoffset=0 #한번 찾으면 바로 초기화
TBLword = [] #테이블 파일중 단어
TBLhex = [] #테이블 파일중 16진수값
startoffset=foundoffset(inFp) #오프셋찾기(0x0c)
tableread() #테이블파일읽기
inFp=open(readfile,"rb")
outFp=open(writefile,"w",encoding='utf-16-le')
inFp3 = open(readfile, "rb")
inFp3.read(0xC)

s = inFp.read(startoffset)
lenscrpit=0

while True:
    if s == '':
        break
    s = inFp.read(1)
    if (len(s)==0):
        break
    if s == '':
        break
    if(ord(s)==00): #마지막일경우
        result=""
        if(lenscrpit==0):
            resultoffset = nextoffset(0)
        else:
            resultoffset=nextoffset(4)
        lenscrpit += 1
        inFp2 = open(readfile, "rb")
        a=inFp2.read(startoffset) #처음 커서까지 이동
        if(longoffset!=0):
            a = inFp2.read(longoffset)  # 방금까지의 오프셋으로 이동
            length=0
            tempoffset = shortoffset
            while True:  # 총 대사길이 읽기
                if(length==tempoffset):
                    break
                a = inFp2.read(1)
                a = str(a)
                if(len(a)==7) and not(a==str(b'\x00'))  and not(a=="b'\\xc'") and not(a==str(b'\xa0')): #ASCII 코드에 없는경우
                    tblresult="" #tbl 찾는값

                    tempoffset-=2 #2개를 더읽어오므로 미리추가
                    b = inFp2.read(2)
                    b = str(b)
                    tblresult+=a[3:]
                    tblresult+=b[3:]
                    tblresult = tblresult.replace("'", "")
                    tblresult = tblresult.replace("x", "")
                    tblresult = tblresult.replace("\\", "")
                    tblresult=tblresult.upper() #테이블 파일을 읽기위해 3바이트 HEX로 치환
                    check=0
                    for i in range(0,len(TBLhex)): #3바이트 HEX가 테이블파일에 있는지 검사
                        if(tblresult == str(TBLhex[i])):
                            tblresult = str(TBLword[i])
                            check=1
                            print(tblresult)
                            break
                    if(check==0):
                        talk="TBL FILE CANNOT FOUND HEX CODES IN SCRPIT!"
                        talk+=tblresult
                        print(talk)
                        break

                    result+=tblresult
                else:
                    result+=a[2:-1]
                length+=1

        else:
            length=0
            tempoffset = shortoffset
            while True:  # 총 대사길이 읽기
                if(length==tempoffset):
                    break
                a = inFp2.read(1)
                a = str(a)
                if(len(a)==7) and not(a==str(b'\x00'))  and not(a=="b'\\xc'") and not(a==str(b'\xa0')): #ASCII 코드에 없는경우
                    tblresult="" #tbl 찾는값
                    tempoffset-=2 #2개를 더읽어오므로 미리추가
                    b = inFp2.read(2)
                    b = str(b)
                    tblresult+=a[3:]
                    tblresult+=b[3:]
                    tblresult = tblresult.replace("'", "")
                    tblresult = tblresult.replace("x", "")
                    tblresult = tblresult.replace("\\", "")
                    tblresult=tblresult.upper() #테이블 파일을 읽기위해 3바이트 HEX로 치환
                    check=0
                    for i in range(0,len(TBLhex)): #3바이트 HEX가 테이블파일에 있는지 검사
                        if(tblresult == str(TBLhex[i])):
                            tblresult = str(TBLword[i])
                            check=1
                            break
                    if(check==0):
                        talk="TBL FILE CANNOT FOUND HEX CODES IN SCRPIT!"
                        talk+=tblresult
                        print(talk)
                        break

                else:
                    result+=a[2:-1]
                length += 1
        longoffset+=shortoffset+1 #방금까지 오프셋 추가
        a=str(a)


        outFp.write(str(resultoffset))
        outFp.write(",")
        outFp.write(str(shortoffset))
        outFp.write(",")
        outFp.write(result)
        outFp.write("\n")
        a=inFp.read(1)
        shortoffset = 0  # 대사길이 초기화
    shortoffset+=1 #대사길이 추가
print("Done!")
inFp.close()
inFp3.close()
outFp.close()