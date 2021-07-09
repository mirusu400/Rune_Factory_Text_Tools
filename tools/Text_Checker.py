PDMacro = ["ヒーロー", "会話モン", "アイテム０", "アイテム１", "アイテム２", "アイテム３", "アイテム４",
           "アイテム５", "アイテム６", "アイテム７", "アイテム８", "アイテム９",
           "数字０", "数字１", "数字２", "数字３", "数字４", "数字５", "数字６", "数字７", "数字８", "数字９",
           "キャラ０", "キャラ１", "キャラ２", "キャラ３", "子供０", "カレンダー０", "マップ０", "マップ１", "マップ２", "マップ３",
           "色", "黒", "０", "１", "２", "３", "４", "５", "牧場", "小屋０", "小屋１", "小屋２", "小屋３", "小屋４", "小屋５"]
Bef_replace = ["1","2","3","4","5","6","7","8","9","0",
               "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z",
               "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
Aft_replace = ["１","２","３","４","５","６","７","８","９","０",
               "Ａ","Ｂ","Ｃ","Ｄ","Ｅ","Ｆ","Ｇ","Ｈ","Ｉ","Ｊ","Ｋ","Ｌ","Ｍ","Ｎ","Ｏ","Ｐ","Ｑ","Ｒ","Ｓ","Ｔ","Ｕ","Ｖ","Ｗ","Ｘ","Ｙ","Ｚ",
               "ａ", "ｂ", "ｃ", "ｄ", "ｅ", "ｆ", "ｇ", "ｈ", "ｉ", "ｊ", "ｋ", "ｌ", "ｍ", "ｎ", "ｏ", "ｐ", "ｑ", "ｒ", "ｓ", "ｔ", "ｕ", "ｖ", "ｗ", "ｘ", "ｙ", "ｚ"]

fp = open("rfText_modi.txt", "rt", encoding="utf-8")
fp2 = open("out.txt", "wt", encoding="utf-8")
lines = fp.readlines()
idx = 1
def check_indent_name(line):
    line = line.replace("@", "＠")

    if "＠" in line:
        arr = line.split("＠")
        errorlevel = 0
        for item in range(0, len(arr)):
            if item % 2 == 0: continue
            if arr[item] in PDMacro:
                errorlevel = 1
                break
        if errorlevel == 0:
            print(arr)
            print(idx)
            input("ERROR")
            return 1
    return 0

def check_newline(line):
    for i in range(0, len(line)):
        errorlevel = 0
        try:
            if line[i] == "n":
                if not line[i - 1] == "\\":
                    print(idx)
                    input("ERROR")
                    return 1
            if line[i] == "\\":
                if not (line[i + 1] == "n" or line[i + 1] == "＋"):
                    print(idx)
                    input("ERROR")
                    return 1
        except:
            pass
    return 0

def replace_line(line):
    for idx in range(0,len(Bef_replace)):
        line = line.replace(Bef_replace[idx],Aft_replace[idx])
    return line

for line in lines:
    line = line.replace("\n", "")
    print(line)
    # Check predefined macro between ＠
    check_indent_name(line)
    # Check_newline(line)
    line = replace_line(line)
    fp2.write(line)
    fp2.write("\n")
    idx += 1
fp.close()
fp2.close()
