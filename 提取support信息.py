
global resultDct
resultDct = {}

def headers(email):
    '''
    提取邮件头部信息
    返回提取出来的dictionary
    '''
    dct = {}
    for i in range(len(email)):
        tmp = email[i].split("：",1)
        if len(tmp) == 2:
            dct[tmp[0]] = tmp[1]
        else:
            dct["#剩余信息"] = email[i:]
            break
    return dct


'''
emails = []
cur = 0
for i in range(len(data)+1):
    if i==len(data) or data[i][:4] == '发件人：':
        emails.append(data[cur:i])
        cur = i
emails = emails[::-1]

for i in range(len(emails)):
    emails[i] = headers(emails[i])
print(emails[0])
'''

import re
data = []
with open("output/test.txt", "r") as f:
    for line in f.readlines():
        line = line.strip('\n')
        if line:
            data.append(line)
resDct = {}


for line in data:
    if re.search("JIRA",line):
        span  = re.search("[A-Z]{4}-[0-9]{5}",line)
        if span:
            resDct["JIRA"] = span.group(0)

    if re.search("交付时间",line):
        span  = re.search("[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])",line)
        if span:
            resDct["交付时间"] = span.group(0)



for i in range(len(data)):
    if re.search("需求场景",data[i]):
        tmp = re.split('[：:]', data[i], maxsplit=1)
        resDct["需求场景"] = tmp[1]

    if re.search("手机",data[i]):
        tmp = re.split('[：:]', data[i], maxsplit=1)
        resDct["手机"] = tmp[1]

i = 0
while i < len(data):
    tmp = re.split('[：:]', data[i], maxsplit=1)
    if len(tmp) != 2:
        i += 1
        continue
    k, v = tmp
    k = k.strip().split("，")[-1]
    if "定制方案" in k:
        if v:
            resDct["定制方案"] = v
            i += 1
        else:
            content = ""
            i += 1
            while i < len(data) and (re.search("^\s*\d", data[i]) or not re.search("[：:]", data[i])):
                content += data[i]
                i += 1
            resDct["定制方案"] = content
    else:
        i += 1



resKey = ["手机","邮箱","场景","工作量","交付时间","JIRA","定制方案"]
for k in resKey:
    for key in resDct:
        if k in key:
            print(key+": "+resDct[key])





