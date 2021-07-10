# -*- coding:utf-8 -*-
import sys
try:
    _in = sys.argv[1]
except:
    _in = input("input text file")
try:
    _tbl = sys.argv[2]
except:
    _tbl = input("input tbl file: ")
try:
    _out = sys.argv[3]
except:
    _out = input("input output file: ")
if _out == "" or _out == None:
    _out = _in + ".txt"
chars=[]
tbls=[]
with open(_in, "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        for char in line:
            if char not in chars:
                chars.append(char)
    chars.sort()

with open(_tbl, "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line == "" or line is None:
            continue
        if line[0] == "/" or line[0] == "#":
            continue
        if len(line.split("=")) > 2:
            _word = "="
        else: _hex, _word = line.split("=")
        tbls.append(_word)
    
with open(_out, "w", encoding="utf-8") as f:
    for char in chars:
        if char not in tbls:
            f.write(char)
            f.write("\n")