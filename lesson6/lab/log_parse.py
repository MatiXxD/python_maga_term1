import re

def parse(ignore_files = False, slow_queries = False, ignore_www = False):

    file = open("log.log", 'r')
    res = []

    text = file.read()
    if ignore_www: text = text.replace("www.", '')
    temp = re.findall("//.+", text)
    

    if not slow_queries:
        urls = list()
        for url in temp:
            urls.append(url.split()[0])
        
        count = dict()
        for url in urls:
            count[url] = count.get(url, 0) + 1

        sortCount = list(reversed(sorted(count.items(), key=lambda x:x[1])))
        for i in range(5):
            res.append(sortCount[i][1])
    
    else:
        times = dict()
        for item in temp:
            url = item.split()[0]
            time = int(item.split()[-1])           

            if times.get(url, 0) == 0:
                times[url] = [1, time]
            else:
                times[url][0] += 1
                times[url][1] += time

        meanTime = dict()
        for k, v in times.items():
            meanTime[k] = v[1] // v[0]

        timeSort = list(reversed(sorted(meanTime.items(), key = lambda x : x[1])))
        #timeSort = list(reversed(sorted(times.items(), key = lambda x : x[1][1] // x[1][0])))
        for i in range(5):
            res.append(timeSort[i][1])          

    file.close()
    return res