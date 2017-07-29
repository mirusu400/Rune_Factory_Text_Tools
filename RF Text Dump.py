# -*- coding:utf-8 -*-
global readfile
global writefile
import sys

def init(inFp):
    inFp.close()
    inFp = open(readfile, "rb")
    return inFp

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
    return int(result,16)


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
print(startoffset)
inFp=open(readfile,"rb")
outFp=open(writefile,"w")


inFp=open(readfile,"rb")
s = inFp.read(startoffset)


while True:
    s = inFp.read(1)
    #if #s == '': break
    #print ('%02X' % int(ord(s)))  # 1바이트씩 출력
    if s == '':
        break
    if(ord(s)==00):
        inFp=init(inFp) #닫고 다시염
        a=inFp.read(startoffset) #처음 커서까지 이동
        if(longoffset!=0):
            a = inFp.read(longoffset+1)  # 방금까지의 오프셋으로 이동
            a = inFp.read(shortoffset-1)  # 총 대사길이 이동
        else:
            a = inFp.read(shortoffset)  # 총 대사길이 이동
        longoffset+=shortoffset
        shortoffset=0 #대사길이 초기화

        a=str(a)
        print(a[1:])
        outFp.write(a[2:-1])
        outFp.write("\n")
        a=inFp.read(1)

    shortoffset+=1 #대사길이 추가

inFp.close()
outFp.close()