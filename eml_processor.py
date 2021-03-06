# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import codecs
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import glob
import re
from tqdm import trange
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value
def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset
def get_content(msg):
    for part in msg.walk():
        content_type = part.get_content_type()
        charset = guess_charset(part)
        #如果有附件，则直接跳过
        if part.get_filename()!=None:
            continue
        email_content_type = ''
        content = ''
        if content_type == 'text/plain':
            email_content_type = 'text'
        elif content_type == 'text/html':
            continue #不要html格式的邮件
            email_content_type = 'html'
        if charset:
            try:
                content = part.get_payload(decode=True).decode(charset,errors='ignore')
            except AttributeError:
                print('type error')
            except UnicodeDecodeError:
                print("unknown encoding: utf-8")
        if email_content_type =='':
            continue
            #如果内容为空，也跳过
        return ''+ content
def get_header(msg):
    ISMINING = False
    res = ""
    for header in ['From', 'To', 'Subject', 'Date','Cc']:
        value = msg.get(header, '')
        if value:
            #文章的标题有专门的处理方法
            if header == 'Subject':
                value = decode_str(value)
            elif header == "Date":
                value = str(decode_str(value))
            elif header == "Cc":
                value = str(decode_str(value))
            elif header in ['From','To']:
            #地址也有专门的处理方法
                hdr, addr = parseaddr(value)
                value = decode_str(addr)
            try:
                res += header + ': ' + value + '\n'
            except TypeError:
                continue
    return res

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    paths = glob.glob(r'raw_emails\*.eml')
    for i in trange(30):
        if '(1)' in paths[i]:
            continue
        newFileName = re.sub(".eml$",".txt",paths[i])
        newFileName = re.sub(r"raw_emails","emails",newFileName)
        with codecs.open(paths[i], "r", encoding='utf-8', errors='ignore') as f:
            text =f.read()
            msg = Parser().parsestr(text)
            header = get_header(msg)
            msg_content = get_content(msg)
            if not header:
                header = ""
            if not msg_content:

                msg_content = ""
            print(msg_content)
            msg_content = header + msg_content
            f = codecs.open(newFileName, "w", "utf-8")
            f.write(msg_content)
            f.close()
