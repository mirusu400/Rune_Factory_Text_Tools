# -*- coding:utf-8 -*-
import sys
try:
    _in = sys.argv[1]
except:
    _in = input("input text file")
try:
    _out = sys.argv[2]
except:
    _out = input("input output file")
chars=[]
with open(_in, "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        for char in line:
            if char not in chars:
                chars.append(char)
    chars.sort()

with open(_out, "w", encoding="utf-8") as f:
    for char in chars:
        f.write(char)
        f.write("\n")