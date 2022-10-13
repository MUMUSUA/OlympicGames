# -*- codeing = utf-8 -*-
# @Time: 2022/4/10 13:56
# @Author:0304190209 李梦婷
# @File : olympic-games.py
# @Software: PyCharm
import datetime
from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，文字匹配
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行EXCEL操作
import sqlite3  # 进行SQLITE数据库操作
import json



def main():
    baseurl="https://olympics.com/_next/data/m-kk1GaANUjWeZqbj94Fv/zh/mobile/olympic-games/beijing-2008.json"
     #1，爬取网页
    urlList=getData(baseurl)
    savepath=".\\历届奥运会url.xls"
    # 3，保存数据
    saveData(urlList,savepath)
    #askURL(baseurl)
    saveToDB(urlList,"OlympicTest.db")




# 1，爬取网页
def getData(baseurl):
    urlList=[]
    html=askURL(baseurl)#保存获取到的网页源码
    data=re.findall(r"\"olympicGames\":(.+?),\"olympicGameState\"",html)
    # print(data)
    js_html=json.loads(data[0])
    for item in js_html:
        year = re.findall("\d+", str(item['meta']['slug']))
        if int(year[0])>datetime.datetime.today().year:
            continue
        data = []
        data.append(item['name'])
        data.append(item['season'])
        data.append("https://olympics.com/zh/olympic-games/"+item['meta']['slug'])
        urlList.append(data)

    # for item in urlList:
    #     print(item)
    return urlList

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
    worksheet=workbook.add_sheet('奖牌数',cell_overwrite_ok=True)
    #单元格写入内容,(行，列，内容)
    col=("届数","季节","url",)
    for i in range(0,3):
        worksheet.write(0,i,col[i])
    for i in range(0,len(datalist)):
        print("第%d条"%(i+1))
        data=datalist[i]
        for j in range(0,3):
            worksheet.write(i+1,j,data[j])

    #保存表格
    workbook.save(savepath)
#
def saveToDB(datalist,dbpath):
    initDB(dbpath)
    conn=sqlite3.connect(dbpath)#打开或创建数据库文件
    cursor=conn.cursor()#获取游标
    for data in datalist:
        for index in range(len(data)):
            data[index]='"'+data[index]+'"'
        sql='''
            insert into urlList
            (name,season,url)
            values
            (%s)'''%",".join(data)
        #执行sql语句
        cursor.execute(sql)
        conn.commit()#提交数据库操作
    cursor.close()
    conn.close()#关闭数据库连接
    print("已保存至数据库中")
#
#
#
def initDB(dbpath):
    sql='''create table urlList
    (
    id integer primary key  autoincrement,
    name varchar ,
    season varchar ,
    url text
    )'''
    #创建数据表
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