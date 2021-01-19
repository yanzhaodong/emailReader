
import re
from collections import OrderedDict
import pandas as pd
import numpy as np
import glob
from tqdm import trange
import sys
import codecs
SUPPORT = True

def is_support(info):
    for dct in info:
        to = dct.get("to", "")
        sub = dct.get("sub","")
        cc = dct.get("cc","")
        if "support" in to+sub+cc:
            return 1
    return 0

def get_data(path):
    struct_data = []
    with codecs.open(path, "r",encoding='utf-8',errors='ignore') as f:
        for line in f.readlines():
            line = line.strip()
            line = re.sub('&nbsp;|&gt',"",line)
            if line:
                struct_data.append(line)
    return struct_data


def classify_email(struct_data):
    for line in struct_data:
        res = re.search("Subject:",line)
        if res:
            if "挖掘" in line:
                return 1
    return 0


def get_headers(line):
    if len(line) > 5 and (line[:5] == "发件时间：" or line[:5] == "Date:"):
        #print("time: " + line)
        return "time",line[4:].strip().lower()
    if len(line) > 4 and (line[:4] == "收件人：" or line[:3] == "To:"):
        #print("to: " + line)
        return "to", line[4:].strip().lower()
    if line[:3] == "抄送：" or line[:3] == "Cc:":
        #print("cc: " + line)
        return "cc", line[3:].strip().lower()
    if line[:3] == "主题：":
        #print("sub:" + line)
        return "subject", line[3:].strip().lower()
    if line[:8] == "Subject:":
        #print("sub:" + line)
        return "subject", line[8:].strip().lower()
    return "",""


def parse_email(data):
    info = [{}]
    content = []
    signature = []
    content_mode = True
    signature_mode = False
    text = ""
    for line in data:
        header_name, header_value = get_headers(line)
        if header_name:  #找到了header信息
            info[-1][header_name] = header_value
        elif '------' in line:
            continue
        elif len(line) > 5 and line[:4] == "发件人：" or line[:5] == "From:":
            #print("From: "+line)
            signature_mode = False
            content_mode = True
            info[-1]["signature"] = '\n'.join(signature)
            signature = []
            info.append({})
            info[-1]["from"] = line[5:].strip()
        elif "更聪明的大数据分析软件" in line:
            #print("Signature: " + line)
            content_mode,signature_mode = False,True
            signature.append(line)
            info[-1]["content"] = '\n'.join(content)
            content = []
        else:
            if content_mode:
                #print("Content: " + line)
                content.append(line)
            elif signature_mode:
                #print("Sig: " + line)
                signature.append(line)
        text += line + "\n"
    if signature:
        info[-1]["signature"] = '\n'.join(signature)
    text = text.lower()
    return info, text


def get_tag(emails):
    for email in emails:
        sub = email.get("sub", "")
        content = email.get("content", "")
        cc = email.get("cc", "")
        text = sub + cc + content
        if "挖掘" in sub or "ETL" in sub or \
                "挖掘" in content or "ETL" in content or\
                    "抄送给mining" in content or "抄送给Mining" in content or\
                        "挖掘" in cc:
            return 1
    return 0

if __name__ == '__main__':
    BINum = 100   #最大获取的BI样本数
    paths = glob.glob(r'emails/*.txt')
    n = len(paths)
    arr = []
    for i in trange(n):
        data = get_data("emails/email"+str(i)+".txt")
        info,text = parse_email(data)
        if "支持" in text or "Support" in text:   #给一个空值，之后再处理
            tag = get_tag(info)
            BINum += tag - 1
            if BINum == 0 and tag == 0:
                continue
            arr.append(["", tag])

        else:
            arr.append([text, get_tag(info)])
    arr = np.asarray(arr,dtype="str")
    df = pd.DataFrame(arr, index=list(range(n)),columns=['email','tags'])
    df.to_csv("output/output.csv", encoding = "utf-8", index=False)