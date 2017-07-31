# -*- coding:utf-8 -*-
"""
-------------------구조
맨 처음 포인터를 찾고(foundoffset) 대사를 찾은후 포인터를 찾고(nextoffset) 이를 txt에 기록합니다.
유니코드일경우 TBL을 탐색하여 그 TBL에 해당하는 글자가 있으면 그 TBL로 추출하고 없을경우 오류메세지를 띄우는 기능입니다

-------------------디버깅 모드에 관하여
룬팩 파일 내에는 대사의 길이가 내장되있습니다. 디버깅 모드를 켜면 그것을 이용해 WQSG 스크립트의 대사를 측정하며
끌 경우에는 이 프로그램 내에서 일일히 하나하나 셉니다
자세한 것은 아래 주석을 참고하세요./
"""
"""
주의!!!
추출했을때 \n 은 줄띄는 제어코드로 "0A" 입니다
삽입시 이를 replace 해야될겁니다.
"""
global readfile
global writefile
global tablefile
global inFp3

import time
import sys


def foundoffset(inFp):
    inFp = open(readfile, "rb")
    inFp.read(0xC)
    result=little_end_to_big_end(inFp)
    inFp.close()
    return int(result,16)

def little_end_to_big_end(inFpset):
    blank=[]
    for i in range(1,5):
        startpath=inFpset.read(1)
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


def romlength():
    result = little_end_to_big_end(inFp3)
    result=int(result,16)
    return result

def nextoffset(nextoffset):
    blank=[]
    inFp3.read(nextoffset)
    result = little_end_to_big_end(inFp3)
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


DEBUG=0 #---------------------디버그 이용



"""
디버그 이용
0 -> 직접 글자수를 세 WQSG의 길이에 입력합니다
1 -> 롬파일에 기록된 글자수를 세 WQSG의 길이에 입력합니다


사용처
대사를 삽입했을때 길이와 글자수가 일치하는지 검사하기위해 사용할 예정입니다.
"""
if (DEBUG == 1):  # ------------------디버그가 1일 경우 shortoffset 대신 롬파일에서 읽어옵니다!
    print("YOU ARE IN DEBUG MODE! READ LENGTH FROM ROM")
    time.sleep(1.5)

#------------------init-----------------------------
longoffset=0 #시작부터 끝까지 0으로 초기화가 안됨 - 시작되는 어드레스를 뜻합니다
shortoffset=0 #한번 찾으면 바로 초기화 - 총 길이를 뜻합니다
lengthoffset=0
TBLword = [] #테이블 파일중 단어
TBLhex = [] #테이블 파일중 16진수값
#---------------------------------------------------


startoffset=foundoffset(inFp) #오프셋찾기(0x0c)
tableread() #테이블파일읽기
inFp=open(readfile,"rb")
outFp=open(writefile,"w",encoding='utf-8')
inFp3 = open(readfile, "rb")

inFp3.read(0xC)


s = inFp.read(startoffset)
if (DEBUG == 1):
    inFp3.close()
    inFp3 = open(readfile, "rb")
    inFp3.read(0x8)

lenscrpit=0

while True:
    if s == '':
        break
    s = inFp.read(1) #한칸한칸 읽어 대사의 마지막까지 검사합니다.
    if (len(s)==0):
        break
    if s == '':
        break
    if(ord(s)==00): #마지막일경우
        result=""
        if(lenscrpit==0):
            if(DEBUG==0):
                resultoffset = nextoffset(0)
            else: # ------------------디버그가 1일 경우 shortoffset 대신 롬파일에서 읽어옵니다!
                lengthoffset = romlength()  # 길이 = 롬에서 읽어옴
                resultoffset=nextoffset(0) #디버그가 1일경우 nextoffset을 4칸 건너뛴 곳에서 하지않고, 바로 읽어야합니다.
        else:
            if(DEBUG==0):
                resultoffset=nextoffset(4)
            else: # ------------------디버그가 1일 경우 shortoffset 대신 롬파일에서 읽어옵니다!
                lengthoffset = romlength()  # 길이 = 롬에서 읽어옴
                resultoffset=nextoffset(0) #디버그가 1일경우 nextoffset을 4칸 건너뛴 곳에서 하지않고, 바로 읽어야합니다.
        lenscrpit += 1
        inFp2 = open(readfile, "rb")
        a=inFp2.read(startoffset) #처음 커서까지 이동
        if (longoffset != 0):
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
                        break
                if(check==0):
                    talk="TBL FILE CANNOT FOUND HEX CODES IN SCRPIT!"
                    talk+=tblresult

                    print(talk)
                    break
                result+=tblresult
            else:
                result+=a[2:-1]
            length += 1
        longoffset+=shortoffset+1 #방금까지 오프셋 추가
        a=str(a)
        if(DEBUG == 1):
            shortoffset = lengthoffset
        print(resultoffset)
        print(result)
        outFp.write(resultoffset) #시작오프셋
        outFp.write(",")
        outFp.write(str(shortoffset)) #길이
        outFp.write(",")
        outFp.write(str(result))
        outFp.write("\n")
        a=inFp.read(1)
        shortoffset = 0  # 대사길이 초기화
    shortoffset+=1 #대사길이 추가
print("Done!")
inFp.close()
inFp3.close()
outFp.close()