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
    for i in range(0, int(len(temps)/2)):

        outtemp = int(temps[i * 2:i * 2 + 2], 16)
        #print(temps[i * 2:i * 2 + 2])
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

    return #TBL파일을 읽어옵니다
def countline():
    tempFp = open(readfile, "r",encoding="utf-8")
    temp=0
    while True:
        line = tempFp.readline()
        if not line: break
        if(line[0]!="\n"): #공백 개행일 경우 넘어가버립니다.
            temp+=1
    return temp#라인의 총 갯수를 셉니다 #라인의 총 갯수를 셉니다
def big_to_little_end(tempinput): #빅 엔디안으로 계산된걸 룬팩토리2에 읽을수있게 스몰 엔디안으로 만들어줍니다
    if(len(tempinput)==1):
        output="0"+tempinput+"000000"
    if(len(tempinput)==2):
        output=tempinput[0:2]+"000000"
    if(len(tempinput)==3): #123 -> 23010000
        
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
result=0
lastresult=0
texts=[]
INSERT_TEXT_TABLE=[]
INSERT_TEXT=""
TBLword = [] #테이블 파일중 단어
TBLhex = [] #테이블 파일중 16진수값
RUNE_FACTORY_3 =1#------------------------------------------------------룬팩 3을 하는경우 체크!
WQSG = 0 #-----------------------------------------------------WQSG사용을 하는경우 반드시 1로 설정해주세요


readfile=sys.argv[1]
#readfile="C:\\Users\\Jun Fac porta03\\Desktop\\rf2TxtCalendar.txt"

try:
    writefile = sys.argv[2]
except:
    writefile=readfile
    writefile+=".out"
tablefile=sys.argv[3]
#tablefile="수정UTF_수정_실전_대사삽입용.tbl"
inFp=open(readfile,"r",encoding="utf-8")
outFp=open(writefile,"wb")


tableread() #테이블파일읽기
tpcountline=countline() # 총 라인수(불변)
print(tpcountline)
tempcountline=tpcountline #총 라인수(가변)
lentexts=hex(tpcountline)
lentexts=(big_to_little_end(lentexts[2:]))
#print(lentexts)
outlabel=b'TEXT'
outFp.write(outlabel)
string_hex_to_hex(lentexts) #------------------------------텍스트의 총 갯수를  씁니다
#string_hex_to_hex("00000000")  #---------------------------------- 텍스트의 길이를 사용해야합니다
#--------------inFp를 읽으면서 한 글자씩 써야 합니다
print(tpcountline)
for a in range(0,tpcountline):
#for a in range(0,5):
    openline=inFp.readline()
    openline = openline.replace(u"\ufeff", '') #BOM 고유오류 수정
    openline = openline.replace("\\n",'|')
    print(openline)
    if(WQSG == 1):
        templines=openline.split(",")
        print(templines)
        openline=""
        for i in range(0,len(templines)-2):
            openline+=templines[i+2] #--------------앞의 두개의 ,를 생략해 저장합니다(WQSG 대비)
            openline+=","
    openline=openline.replace("\n","")
    #openline=openline[0:-1]
    print(openline)
    lastresult = result
    result=0
    INSERT_TEXT=""
    for i in range(0,len(openline)):
        if((openline[i])=="|"):
            result+=1
            INSERT_TEXT+="0A" #줄넘김 을 일부러 수정했습니다
        else:
            for k in range(0,len(TBLword)):
                if(openline[i] == TBLword[k]):
                    result+=len(TBLhex[k])/2
                    INSERT_TEXT+=TBLhex[k]
                    break
    INSERT_TEXT+="00"
    if(RUNE_FACTORY_3==1):
        INSERT_TEXT+="00"
    print(INSERT_TEXT)


    #print("DEBUG")
    #print(int(result))
    #print(hex(#int(result)))
    string_hex_to_hex((big_to_little_end(str(hex(int(result)))[2:]))) #-------------최종 결과값(대사길이)을 결과에 씁니다
    if(a == 0):
        tempcountline=hex(tpcountline * 8+8) #대사시작 오프셋 계산()
        countlineresult=big_to_little_end(str(tempcountline)[2:]) #-------------첫번째 오프셋의 경우 직접 계산합니다
        string_hex_to_hex(countlineresult)
    else:

        tempcountline=hex(int(tempcountline,16)+(int(lastresult))+1+RUNE_FACTORY_3) #hex값을 10진수로 계산해 더한다음 다시 16진수로 변환한후 이를 ROM에 기록 ★★★★★ 맨뒤에 00까지 다음포인터 계산때 필요하기때문에 1을 더합니다!!!!!!!!!!!!!!!!!!!!
        countlineresult=big_to_little_end(str(tempcountline)[2:])
        string_hex_to_hex(countlineresult)
    INSERT_TEXT_TABLE.append(INSERT_TEXT)
print("DONE")
for b in range(0,tpcountline):

    string_hex_to_hex(INSERT_TEXT_TABLE[b])




