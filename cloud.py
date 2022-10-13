# -*- coding = utf-8 -*-
# @Time : 2022/4/12 21:55
# @Author : lff
# @File : cloud.py
# @Software : PyCharm

import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud,STOPWORDS
from PIL import Image
import numpy as np
import re

with open("bili2.txt", encoding="utf-8") as f:
    data = f.read()

# 文本预处理  去除一些无用的字符   只提取出中文出来
new_data = re.findall('[\u4e00-\u9fa5]+', data, re.S)
new_data = "/".join(new_data)
cut = jieba.cut(new_data, cut_all=False)
string = ' '.join(cut)

list1=string.split()

list2 = list(set(list1))
fre={}
for item in list2:
    n = 0
    for item2 in list1:
        if item==item2:
            n+=1

    fre[item]=n

print(fre)


img = Image.open(r"./static/assets/img/13.jpeg")
img_array = np.array(img)
wc = WordCloud(
    background_color='white',
    mask=img_array,
    font_path="msyh.ttc",
    stopwords={"我" ,"的", "了", "们" ,"我们" ,"在","亲爱"}
).generate_from_text(string)

fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')
plt.show()
# plt.savefig(r'.\static\assets\img\img.jpeg')