# -*- codeing = utf-8 -*-
# @Time: 2022/4/14 21:13
# @Author:0304190209 LMT
# @File : china.py
# @Software: PyCharm
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，文字匹配
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行EXCEL操作
import sqlite3  # 进行SQLITE数据库操作
import json


def main():
    baseurl="https://en.wikipedia.org/wiki/China_at_the_Olympics"
     #1，爬取网页
    datalist=getData(baseurl)
    savepath=".\\中国各项奖牌数.xls"
    # 3，保存数据
    saveData(datalist,savepath)
    #askURL(baseurl)
    saveToDB(datalist,"OlympicTest.db")

findMedal=re.compile(r'<td>(\d*)</td>')
findSports=re.compile(r'at the Olympics">(.*?)</a></th><td>')


# 1，爬取网页
def getData(baseurl):
    datalist=[]
    html=askURL(baseurl)#保存获取到的网页源码
    # 2，逐一解析数据
    soup=BeautifulSoup(html,"html.parser")
    k=0
    season="Summer"
    for item in soup.find_all('table',class_="wikitable sortable plainrowheaders jquery-tablesorter"): #查找符合要求的字符串，形成列表
        if k==1:
            season="Winter"
        sports = re.findall(findSports, str(item))
        medal=re.findall(findMedal,str(item))
        for i in range(0,len(sports)):
            data=[]
            data.append(season)
            data.append(sports[i])
            for num in range(0,4):
                data.append(medal[4*i+num])
            datalist.append(data)
        k+=1






    # for item2 in soup.find_all('a',class_="mw-redirect"): #查找符合要求的字符串，形成列表
    #
    #     print(sports)
    print(datalist)
    print(len(datalist))

    return datalist;




#得到指定一个URL的网页内容
def askURL(url):
    #模拟浏览器头部信息，向其服务器发送消息

    head={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    }
    #用户代理表示告诉豆瓣服务器我们是什么类型的机器，浏览器，告诉浏览器我们能接受什么水平的文件
    request=urllib.request.Request(url,headers=head)
    html=''
    try:
        response=urllib.request.urlopen(request,timeout=5)
        html=response.read().decode("utf-8")
        #print("完了"+html+"好像是")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html
# 3，保存数据
def  saveData(datalist,savepath):
    #以utf-8编码创建一个Excel对象
    workbook=xlwt.Workbook(encoding="utf-8",style_compression=0)
    #创建一个Sheet表
    worksheet=workbook.add_sheet('各项奖牌数',cell_overwrite_ok=True)
    #单元格写入内容,(行，列，内容)
    col=("季节","项目","金牌","银牌","铜牌","总数",)
    for i in range(0,6):
        worksheet.write(0,i,col[i])
    for i in range(0,len(datalist)):
        print("第%d条"%(i+1))
        data=datalist[i]
        for j in range(0,6):
            worksheet.write(i+1,j,data[j])

    #保存表格
    workbook.save(savepath)

def saveToDB(datalist,dbpath):
    initDB(dbpath)
    conn=sqlite3.connect(dbpath)#打开或创建数据库文件
    cursor=conn.cursor()#获取游标
    for row in datalist:

        sql='''
            insert into ChinaMedal
            (season,sport,gold,silver,bronze,total)
            values
              ('%s','%s',%d,%d,%d,%d)'''% (str(row[0]),str(row[1]),int(row[2]),int(row[3]),int(row[4]),int(row[5]))
        #执行sql语句
        cursor.execute(sql)
        conn.commit()#提交数据库操作
    cursor.close()
    conn.close()#关闭数据库连接
    print("已保存至数据库中")



def initDB(dbpath):
    sql='''
    create table ChinaMedal
    (
    id integer primary key  autoincrement,
    season varchar ,
    sport varchar ,
    gold numeric ,
    silver numeric ,
    bronze numeric ,
    total numeric 
    )
    '''#创建数据表
    conn=sqlite3.connect(dbpath)
    print("open database successfully")
    cursor=conn.cursor()
    cursor.execute(sql)
    print("create table successfully")
    conn.commit()
    conn.close()


if __name__=="__main__":
    main()
    print("爬取完毕")
