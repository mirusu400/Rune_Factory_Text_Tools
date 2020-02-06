# Check Texts that above 20~22 texts
# If texts above 20~22 without newline, it cannot shown in screen


fp = open("본대사/rf2mc.ko.txt","rt",encoding="utf-8")
lines = fp.readlines()
for line in lines:
    line = line.replace("\n","")
    print(line)
    tmp = line.split("_")
    for j in tmp:
        tmp = len(j)
        tmp -= j.count(" ") / 2
        tmp -= j.count(",") / 2
        tmp -= j.count(".") / 2
        if(tmp > 22):
            print("Wrong")
            print(tmp)
            print(j)
            input()