import os
exit_code = os.system('ping www.baidu.com')
if exit_code:
    raise Exception('connect failed.')
else:
    print("connection succeeded")