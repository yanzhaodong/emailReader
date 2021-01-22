from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

host_server = 'smtp.163.com'
sender_qq = 'yanzhaodong2021@163.com'
pwd = 'QCZHBCJZWVQBBSDE' ## xh**********bdc
sender_qq_mail = 'yanzhaodong2021@163.com'
receiver = '1583814493@qq.com'
mail_content = '你好，这是使用python登录qq邮箱发邮件的测试'
mail_title = 'Maxsu的邮件'
smtp = SMTP_SSL(host_server)
smtp.set_debuglevel(1)
smtp.ehlo(host_server)
smtp.login(sender_qq, pwd)

msg = MIMEText(mail_content, "plain", 'utf-8')
msg["Subject"] = Header(mail_title, 'utf-8')
msg["From"] = sender_qq_mail
msg["To"] = receiver
smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
smtp.quit()


