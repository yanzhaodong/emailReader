
import re
from collections import OrderedDict
import pandas as pd
import numpy as np
import glob
from tqdm import trange
import sys
import codecs
SUPPORT = True

def get_email_tag(emails):
    for email in emails:
        sub = email.get("subject", "")
        content = email.get("content", "")
        cc = email.get("cc", "")
        to = email.get("to", "")
        text = sub + '------'+cc + '------'+to+content
        text = re.sub("快速挖掘企业","",text)
        text = re.sub("数据挖掘部署", "", text)
        text = re.sub("挖掘安装", "", text)
        text = re.sub("挖掘及etl的安装", "", text)
        text = re.sub("数据挖掘引擎", "", text)
        text = re.sub("etl工程", "", text)
        text = re.sub("若有使用数据挖掘功能", "", text)
        text = re.sub("数挖引擎一起更新", "", text)
        text = re.sub("interpretloop", "", text)
        text = re.sub("getlogger", "", text)
        text = re.sub("etl^\w", "", text)

        if get_tag(text) or 'mining' in cc or 'mining' in sub:
        # if "挖掘" in sub or "ETL" in sub or \
        #         "挖掘" in content or "ETL" in content or \
        #         "数挖" in content or "数挖" in sub or \
        #         "抄送给mining" in content or "抄送给Mining" in content or\
        #                 "挖掘" in cc:
            return 1
    return 0

def is_support(info):
    for dct in info:
        to = dct.get("to", "")
        sub = dct.get("sub","")
        cc = dct.get("cc","")
        text = to+sub+cc

        if "support" in text or "支持" in text:
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

def get_headers(line):
    if len(line) > 5 and (line[:5] == "发件时间：" or line[:5] == "date：" or line[:5] == "发送时间："):
        #print("time: " + line)
        return "time",line[4:].strip().lower()
    if len(line) > 4 and (line[:4] == "收件人：" or line[:3] == "to："):
        #print("to: " + line)
        return "to", line[4:].strip().lower()
    if line[:3] == "抄送：" or line[:3] == "cc：":
        #print("cc: " + line)
        return "cc", line[3:].strip().lower()
    if line[:3] == "主题：":
        #print("sub:" + line)
        return "subject", line[3:].strip().lower()
    if line[:8] == "subject：":
        #print("sub:" + line)
        return "subject", line[8:].strip().lower()
    return "",""

def E_trans_to_C(string):
    E_pun = u':'
    C_pun = u'：'
    table= {ord(f):ord(t) for f,t in zip(E_pun,C_pun)}
    return string.translate(table)
def preprocess(line):
    return E_trans_to_C(line).lower()



def parse_email(data):
    info = [{}]
    content = []
    signature = []
    content_mode = True
    signature_mode = False
    text = ""
    for line in data:
        line = preprocess(line)
        header_name, header_value = get_headers(line)

        if header_name:  #找到了header信息
            info[-1][header_name] = header_value
            #print(header_name+": "+header_value)
        elif '------' in line:
            continue
        elif len(line) > 5 and (line[:4] == "发件人：" or line[:5] == "from：" or line[:4] == "发件人："):
            #print("From: "+line)
            signature_mode = False
            content_mode = True
            if signature:
                info[-1]["signature"] = '\n'.join(signature)
            if content:
                info[-1]["content"] = '\n'.join(content)
            signature = []
            info.append({})
            info[-1]["from"] = line[5:].strip()
        # elif len(line) > 11 and line[:11] == "广州思迈特软件有限公司" and content:
        #     name = re.sub(" ","",line[11:])
        #     if len(name) in [2,3]:
        #         print("Signature: " + line)
        #         content_mode, signature_mode = False, True
        #         signature.append(line)
        #         info[-1]["content"] = '\n'.join(content)
        #         print('\n'.join(content))
        #         content = []

        elif "更聪明的大数据分析软件" in line or "领跑商业智能15年" in line:
            if content == []:
                continue
            #print("Signature: " + line)
            content_mode,signature_mode = False,True
            signature.append(line)
            info[-1]["content"] = '\n'.join(content)
            #print('\n'.join(content))
            content = []
        else:
            if content_mode:
                #print("Content: " + line)
                content.append(line)
            elif signature_mode:
                #print("Sig: " + line)
                signature.append(line)
            else:
                #print("UE: "+line)
                pass
        text += line + "\n"
    if signature:
        info[-1]["signature"] = '\n'.join(signature)
    return info, text

def print_email(structEmails):
    for email in structEmails:
        for k,v in email.items():
            print(k+": "+v)
    return

def get_tag(line):
    if "挖掘" in line or "etl" in line or "数挖" in line or "mining" in line:
        return True
    return False
def find_seg(text):
    for segment in ["快速挖掘企业", "数据挖掘部署", "挖掘安装", "挖掘及etl的安装", "数据挖掘引擎", "etl工程", "若有使用数据挖掘功能"
        , "数挖引擎一起更新", "interpretloop", "getlogger"]:
        if segment in text:
            return True
    return False

if __name__ == '__main__':
    BINum = 30   #最大获取的BI样本数
    confusionNum = 10
    paths = glob.glob(r'emails\*.txt')
    n = len(paths)
    arr = []
    for i in trange(n):
        data = get_data(paths[i])
        info,text = parse_email(data)
        if "support" in text:
            tag = get_email_tag(info)

            BINum += (int(tag) - 1)
            if BINum < 0 and tag == 0:
                continue
            if tag == 0 and find_seg(text):
                confusionNum -= 1
                BINum += 1
                if confusionNum < 0:
                    continue

            arr.append([text, get_email_tag(info)])

    arr = np.asarray(arr,dtype="str")
    df = pd.DataFrame(arr, index=list(range(arr.shape[0])),columns=['email','tags'])
    df.to_csv("output/output.csv", encoding = "utf-8", index=False)