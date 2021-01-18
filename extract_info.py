
import re


def get_data(path):
    struct_data = []
    with open(path, "r") as f:
        for line in f.readlines():
            line = line.strip()
            line = re.sub('&nbsp;|&gt',"",line)
            if line:
                struct_data.append(line)
    return struct_data


def classify_email(struct_data):
    for line in struct_data:
        print(line)
        res = re.search("Subject:",line)
        if res:
            if "挖掘" in line:
                return 1
    return 0


def get_headers(line):
    if len(line) > 5 and (line[:5] == "发件时间：" or line[:5] == "From:"):
        print("time: " + line)
        return "time",line[4:].strip()
    if len(line) > 4 and (line[:4] == "收件人：" or line[:3] == "To:"):
        print("to: " + line)
        return "to", line[4:].strip()
    if line[:3] == "抄送：":
        print("cc: " + line)
        return "cc", line[3:].strip()
    elif line[:3] == "主题：":
        print("sub:" + line)
        return "subject", line[3:].strip()
    elif line[:8] == "Subject:":
        print("sub:" + line)
        return "subject", line[8:].strip()
    return "",""


def parse_email(data):
    info = [{}]
    content = []
    signature = []
    content_mode = True
    signature_mode = False
    for line in data:
        header_name, header_value = get_headers(line)
        if header_name:  #找到了header信息
            info[-1][header_name] = header_value

        if '------' in line:
            continue
        elif len(line) > 5 and line[:4] == "发件人：" or line[:5] == "From:":
            print("From: "+line)
            signature_mode = False
            content_mode = True
            info[-1]["signature"] = '\n'.join(signature)
            signature = []
            info.append({})
            info[-1]["from"] = line[5:].strip()

        elif "更聪明的大数据分析软件" in line:
            print("Signature: " + line)
            content_mode,signature_mode = False,True
            signature.append(line)
            info[-1]["content"] = '\n'.join(content)
            content = []
        else:
            if content_mode:
                print("Content: " + line)
                content.append(line)
            elif signature_mode:
                print("Sig: " + line)
                signature.append(line)
    if signature:
        info[-1]["signature"] = '\n'.join(signature)
    return info


if __name__ == '__main__':
    path = "output/test.txt"
    data = get_data(path)
    info = parse_email(data)
    print(info)