import sys
def tableread(inFps):
    TBLword=[]
    TBLhex=[]
    while True:
        line=inFps.readline()
        line=line.replace("\n","")
        line=line.split("=")
        if (line == ['']):
            break
        line[0] = line[0].replace(u"\ufeff", '') #BOM고유오류 조정
        TBLword.append(line[1])
        TBLhex.append(line[0])


    return TBLword, TBLhex #TBL파일을 읽어옵니다
NFTRTBL=sys.argv[1]
UTF8TBL=sys.argv[2]
OUTPUTTBL=sys.argv[3]
FinalTBL=[]
inFp=open(NFTRTBL,"r",encoding="utf-8")
inFp2=open(UTF8TBL,"r",encoding="utf-8")
inFp3=open(OUTPUTTBL,"w",encoding="utf-8")
tblresult1=tableread(inFp)
tblresult2=tableread(inFp2)
#---------------------tblresult[0] 은 글자,
#---------------------tblresult[1] 은 hex값이 됩니다
for i in range(0,len(tblresult1[0])):
    temp=0
    for k in range(0,len(tblresult2[0])):
        if(tblresult1[0][i] == tblresult2[0][k]):
            result=tblresult2[1][k]+"="+tblresult1[0][i]
            temp=1
            break
    if(temp==0):
        result = (tblresult1[0][i].encode('utf-8', 'ignore'))
        result = str(result)
        result = result[2:]
        result = result.replace("\\x", "")
        result = result.replace("'", "")
        result = result.upper()
        result+="="+tblresult1[0][i]
        FinalTBL.append(result)
    if(temp==1):
        FinalTBL.append(result)
print(FinalTBL)
for i in range(0,len(FinalTBL)):
    inFp3.write(FinalTBL[i])
    inFp3.write("\n")
print("DONE!")