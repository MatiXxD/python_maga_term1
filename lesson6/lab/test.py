import re

file = open("log.log", 'r')
text = file.read()
temp = re.findall("//.+", text)

urls = list()
for url in temp:
    urls.append(url.split()[0])

count = dict()
for url in urls:
    count[url] = count.get(url, 0) + 1

sortCount = list(reversed(sorted(count.items(), key=lambda x:x[1])))
for i in range(5):
    res.append(sortCount[i][1])

timeSort = list(reversed(sorted(meanTime.items(), key = lambda x : x[1])))
res = []
for i in range(5):
    res.append(timeSort[i][1])

print(res)