# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# coding=utf-8
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from tqdm import trange
import codecs
import time
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

def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            #print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        #for n, part in enumerate(parts):
            #print('%spart %s' % ('  ' * indent, n))
            #print('%s--------------------' % ('  ' * indent))
            #print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            #print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            #print('%sAttachment: %s' % ('  ' * indent, content_type))
            pass
            
def get_header(msg):
    ISMINING = False
    res = ""
    for header in ['From', 'To', 'Subject', 'Date','Cc']:
        value = msg.get(header, '')
        if value:
            #文章的标题有专门的处理方法
            if header == 'Subject':
                value = decode_str(value)
                if "挖掘" in value:
                    ISMINING = True
            elif header == "Date":
                value = str(decode_str(value))
            elif header == "Cc":
                value = str(decode_str(value))
                if "挖掘" in value:
                    ISMINING = True
            elif header in ['From','To']:
            #地址也有专门的处理方法
                hdr, addr = parseaddr(value)
                value = decode_str(addr)
            res += header + ': ' + value + '\n'
    return res, ISMINING
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
            #这里遇到了几种由广告等不满足需求的邮件遇到的错误，直接跳过了
            except AttributeError:
                print('type error')
            except UnicodeDecodeError:
                print("unknown encoding: utf-8")
        if email_content_type =='':
            continue
            #如果内容为空，也跳过
        return ''+ content
        #print(email_content_type + ' -----  ' + content)
        
poplib._MAXLINE=204800
"""POP的服务器信息"""
SEVER_NAME='imap.exmail.qq.com'
USER_NAME='huangpeng@smartbi.com.cn'
USER_PASSWORD='Hp9876504321'

# 连接到POP3服务器:
server = poplib.POP3(SEVER_NAME)
# 可以打开或关闭调试信息:
server.set_debuglevel(1)
# 可选:打印POP3服务器的欢迎文字:
#print(server.getwelcome().decode('utf-8'))
 
# 身份认证:
server.user(USER_NAME)
server.pass_(USER_PASSWORD)
 
# stat()返回邮件数量和占用空间:
print('Messages: %s. Size: %s' % server.stat())
# list()返回所有邮件的编号:
resp, mails, octets = server.list()
# 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
index = len(mails)
for i in range(20,index-1):
    st = time.time()
    # 获取最新一封邮件, 注意索引号从1开始:
    print("开始")
    resp, lines, octets = server.retr(i+1)  #来了新邮件可能又会有重复的内容
    # lines存储了邮件的原始文本的每一行,
    # 可以获得整个邮件的原始文本:
    msg_content = b'\r\n'.join(lines).decode('utf-8',errors='ignore')
    # 稍后解析出邮件:
    msg = Parser().parsestr(msg_content)
    header,ISMINING = get_header(msg)
    if ISMINING:
        msg_content = get_content(msg)
        if not header:
            header = ""
        if not msg_content:
            msg_content = ""
        msg_content = header + msg_content

        f = codecs.open("emails/email"+str(i)+".txt", "w", "utf-8")
        f.write(msg_content)
        # with open("emails/email"+str(i)+".txt","w",encoding='utf-8') as f:
        #     f.write(msg_content)
        f.close()
server.quit()