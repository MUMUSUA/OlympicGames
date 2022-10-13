# -*- coding = utf-8 -*-
# @Time : 2022/4/12 21:13
# @Author : lff
# @File : bilibili.py
# @Software : PyCharm

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# 弹幕保存文件
file_name = 'bili2.txt'

# 获取页面
cid = 501328374
url = "https://comment.bilibili.com/" + str(cid) + ".xml"
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
request = requests.get(url=url, headers=headers)
request.encoding = 'utf-8'

# 提取弹幕
soup = BeautifulSoup(request.text, 'lxml')
results = soup.find_all('d')

# 数据处理
data = [data.text for data in results]
# 正则去掉多余的空格和换行
for i in data:
    i = re.sub('\s+', '', i)

# 查看数量
print("弹幕数量为：{}".format(len(data)))

# 输出到文件
df = pd.DataFrame(data)
df.to_csv(file_name, index=False, header=None, encoding="utf_8_sig")
print("写入文件成功")

