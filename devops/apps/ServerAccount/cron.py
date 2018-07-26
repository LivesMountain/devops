import re
text = "likun@guoshengtianfeng.com"
if re.match(r'[0-9a-zA-Z_]{0,19}@guoshengtianfeng.com',text):
    print(re.match(r'[0-9a-zA-Z_]{0,19}@guoshengtianfeng.com',text))
    print('Email address is Right!')
else:
    print('Please reset your right Email address!')