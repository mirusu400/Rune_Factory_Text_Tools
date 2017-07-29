# -*- coding:utf-8 -*-
global readfile
global writefile
global inFp3
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


readfile=sys.argv[1]
try:
    writefile = sys.argv[2]
except:
    writefile=readfile
    writefile+=".txt"
inFp=0
texts=[]
longoffset=0 #시작부터 끝까지 0으로 초기화가 안됨
shortoffset=0 #한번 찾으면 바로 초기화

startoffset=foundoffset(inFp) #오프셋찾기(0x0c)
inFp=open(readfile,"rb")
outFp=open(writefile,"w")
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
        if(lenscrpit==0):
            resultoffset = nextoffset(0)
        else:
            resultoffset=nextoffset(4)
        lenscrpit += 1
        inFp2 = open(readfile, "rb")
        a=inFp2.read(startoffset) #처음 커서까지 이동
        if(longoffset!=0):
            a = inFp2.read(longoffset)  # 방금까지의 오프셋으로 이동
            a = inFp2.read(shortoffset)  # 총 대사길이 읽기
        else:
            a = inFp2.read(shortoffset)  # 총 대사길이 읽기
        longoffset+=shortoffset+1 #방금까지 오프셋 추가
        a=str(a)

        print(a[1:])
        outFp.write(str(resultoffset))
        outFp.write(",")
        outFp.write(str(shortoffset))
        outFp.write(",")
        outFp.write(a[2:-1])
        outFp.write("\n")
        a=inFp.read(1)
        shortoffset = 0  # 대사길이 초기화
    shortoffset+=1 #대사길이 추가
print("Done!")
inFp.close()
inFp3.close()
outFp.close()