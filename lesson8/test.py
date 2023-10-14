from DirDict import *

dct = DirDict("data/")

files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.txt", "file6.txt"]
info = ["test1", "test2", "test3", "test4", "test5", "test6"]
for i in range(len(files)):
    dct[files[i]] = info[i]

for k, v in dct.items():
    print(k, v)

print(dct)

dct.clear()
