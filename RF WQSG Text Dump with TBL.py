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

-------------------프로그램 구조
맨 처음 포인터를 찾고(foundoffset) 대사를 찾은후 포인터를 찾고(nextoffset) 이를 txt에 기록합니다.
유니코드일경우 TBL을 탐색하여 그 TBL에 해당하는 글자가 있으면 그 TBL로 추출하고 없을경우 오류메세지를 띄우는 기능입니다

-------------------상대 오프셋 디버깅에 관하여(DEBUG_RELATIVE_OFFSET)
룬팩 파일 내에는 대사의 길이가 내장되있습니다. 디버깅 모드를 켜면 그것을 이용해 WQSG 스크립트의 대사를 측정하며
끌 경우에는 이 프로그램 내에서 일일히 하나하나 셉니다
자세한 것은 아래 주석을 참고하세요.
★★★★★ 현재는 사용 불가능합니다 사용할 필요성을 못느꼈습니다.


-------------------상대 어드레스 디버깅에 관하여(DEBUG_RELATIVE_ADDRESS)
룬팩 파일 내에는 대사의 길이가 내장되있습니다. 디버깅 모드를 켜면 그것을 이용해 WQSG 스크립트의 대사를 측정하며
끌 경우에는 이 프로그램 내에서 일일히 하나하나 셉니다
자세한 것은 아래 주석을 참고하세요.
★★★★ 어드레스 디버깅을 사용하면 강제로 오프셋 디버깅 또한 사용하게 됩니다.

inFp3 = 포인터 쪽을 읽어드리는 부분입니다.
inFp2 = 총 대사를 읽어드리는 부분입니다
"""
"""
주의!!!
추출했을때 \n 은 줄띄는 "새줄 문자"라는 것으로 제어코드로 "0A" 입니다
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

def nextoffset(nextoffset):
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


DEBUG_RELATIVE_OFFSET=1 #---------------------디버그 이용
DEBUG_RELATIVE_ADDRESS=1 #---------------------디버그 이용

"""
상대 어드레스 디버그 이용
0 -> 직접 주소값을 세 WQSG의 어드레스에 입력합니다
1 -> 롬파일에 기록된 어드레스를 읽어내 WQSG의 길이에 입력합니다


사용처
대사를 삽입했을때 길이와 글자수가 일치하는지 검사하기위해 사용할 예정입니다.
"""

"""
상대 오프셋 디버그 이용
0 -> 직접 글자수를 세 WQSG의 길이에 입력합니다
1 -> 롬파일에 기록된 글자수를 세 WQSG의 길이에 입력합니다


사용처
대사를 삽입했을때 길이와 글자수가 일치하는지 검사하기위해 사용할 예정입니다.
"""
if (DEBUG_RELATIVE_OFFSET == 0):  # ------------------디버그가 1일 경우 shortoffset 대신 롬파일에서 읽어옵니다!
    print("YOU ARE IN DEBUG_RELATIVE_OFFSET MODE! READ LENGTH FROM ROM")
    time.sleep(1)
if (DEBUG_RELATIVE_ADDRESS == 1):  # ------------------디버그가 1일 경우 shortoffset 대신 롬파일에서 읽어옵니다!
    print("YOU ARE IN DEBUG_RELATIVE_ADRESS MODE! READ LENGTH AND ADREES FROM ROM")
    time.sleep(1)
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
if (DEBUG_RELATIVE_OFFSET == 1) or (DEBUG_RELATIVE_ADDRESS==1):
    inFp3.close()
    inFp3 = open(readfile, "rb")
    inFp3.read(0x8)

lenscrpit=0

if (DEBUG_RELATIVE_ADDRESS==1):  # 롬 안의 메모리를 읽어오는경우
    inFp3.close()
    inFp3 = open(readfile, "rb")
    inFp3.read(0x4)
    looptime=int(little_end_to_big_end(inFp3), 16)
    inFp.close()
    beforeaddress = 0
    for kig in range(0,looptime):
        inFp = open(readfile, "rb")

        length = int(little_end_to_big_end(inFp3), 16) #롬의 길이를 읽어냅니다
        address = int(little_end_to_big_end(inFp3), 16) #롬의 주소값을 알아냅니다
        inFp.read(address) #열었다 닫았따 하기때문에 바로 주소에서 읽어내도 상관이 없습니다
        result=inFp.read(length)
        result=str(result)
        result=result[2:-1]
        foundregester=0
        lenresult=result
        result=result.replace("\\'","'")
        for i in range(0,len(lenresult)): #대사에서 TBL에 있는 것들을 검색해야합니다.
            #i +=(foundregester*(-1))
            try:
                if((result[i]) == ('\\') and not result[i:i+2] == ('\\n')): #검색한것이 줄띄어쓰기가 아니고 ASCII코드에 없는경우
                    if not(result[i:i+4] == str('\\x00')) and not (result[i:i+4] == "\\xc") and not (result[i:i+4]==str(b'\xa0')): #특수한 경우를 제외합니다

                        #------------------3바이트, 2바이트, 1바이트 차례를 읽어와 테이블과 대조해야합니다!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        foundregester+=1 #왜 추가해야되는지 몰겠어요 ㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ
                        for t in range(0,3):
                            tblresult = ""  # tbl 찾는값
                            tblresult = result[i:i + (12-4*t)] #3바이트 2바이트 1바이트 차례로 읽어옴 읽어오기
                            tblresult = tblresult.replace("'", "")
                            tblresult = tblresult.replace("x", "")
                            tblresult = tblresult.replace("\\", "")
                            tblresult = tblresult.upper()  # 테이블 파일을 읽기위해 3바이트 HEX로 치환
                            check = 0
                            for k in range(0, len(TBLhex)):  # 3바이트 HEX가     테이블파일에 있는지 검사
                                if (tblresult == str(TBLhex[k])):
                                    tblresult = str(TBLword[k])
                                    check = 1
                                    break
                            if(check==1):
                                break
                        if (check == 0):
                            talk = "TBL FILE CANNOT FOUND HEX CODES IN SCRPIT! HEX CODE ::  "
                            talk += tblresult
                            print(talk)
                            print("10초 후 계속됩니다.")
                            time.sleep(10)
                            break
                        temp0=result[0:i] #문자열을 두 부분으로 나눈다음 가운데를 방금 찾은 테이블표 값을 입력한후 다시 합칩니다.
                        temp1=result[i+12-4*t:len(result)]
                        result=""
                        result+=temp0
                        result+=tblresult
                        result+=temp1

                    else:
                        length+=1
            except:
                break
        print(result)
        address=str(hex(address))
        address=address.replace("x","")
        address=address.upper()
        if(len(address)==1):
            address="0000000"+address
        if(len(address)==2):
            address="000000"+address
        if(len(address)==3):
            address="00000"+address
        if(len(address)==4):
            address="0000"+address
        if(len(address)==5):
            address="000"+address
        if(len(address)==6):
            address="00"+address
        if(len(address)==7):
            address="0"+address
        outFp.write(str(address))  # 시작오프셋
        outFp.write(",")
        outFp.write(str(length))  # 길이
        outFp.write(",")
        outFp.write(str(result))
        outFp.write("\n")
        length += 1
        inFp.close()
        lenscrpit+=1
if(DEBUG_RELATIVE_ADDRESS==0):
    while True:
        s = inFp.read(1) #한칸한칸 읽어 대사의 마지막까지 검사합니다.
        if (len(s)==0):
            break
        if s == '':
            break
        if(ord(s)==00): #마지막일경우
            result=""
            if(lenscrpit==0):
                if(DEBUG_RELATIVE_OFFSET==0):
                    resultoffset = nextoffset(0)
                else: # ------------------디버그가 1일 경우 shortoffset 대신 롬파일에서 읽어옵니다!------------shortoffset 올라가는건 맨 아래에 있습니다.
                    lengthoffset = int(little_end_to_big_end(inFp3),16)  # 길이 = 롬에서 읽어옴
                    resultoffset=nextoffset(0) #디버그가 1일경우 nextoffset을 4칸 건너뛴 곳에서 하지않고, 바로 읽어야합니다.
            else:
                if(DEBUG_RELATIVE_OFFSET==0):
                    resultoffset=nextoffset(4)
                else: # ------------------디버그가 1일 경우 shortoffset 대신 롬파일에서 읽어옵니다!
                    lengthoffset = int(little_end_to_big_end(inFp3),16)   # 길이 = 롬에서 읽어옴
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
            if(DEBUG_RELATIVE_OFFSET == 1):
                shortoffset = lengthoffset
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
outFp.close()
inFp3.close()

