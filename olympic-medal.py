# -*- codeing = utf-8 -*-
# @Time: 2022/4/10 13:56
# @Author:0304190209 LMT
# @File : olympic-medal.py
# @Software: PyCharm

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，文字匹配
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行EXCEL操作
import sqlite3  # 进行SQLITE数据库操作
import json
import time


def main():
    # baseurl="https://olympics.com/zh/olympic-games/beijing-2022/medals"
     #1，爬取网页
    urlList = getUrl("OlympicTest.db")
    datalist=getData(urlList)
    savepath=".\\奖牌数.xls"
    # 3，保存数据
    saveData(datalist,savepath)
    #askURL(baseurl)
    saveToDB(datalist,"movieTest.db")

findName=re.compile(r'<h1 class="styles__Header-sc-31x12v-0 cCWdvF"><span>(.*)</span>')
findMedal=re.compile(r'<span class="(.*)" data-cy="medal-main">(\d*)</span>')
findCountry=re.compile(r'<div class="styles__CountryCompleteName-sc-fehzzg-3 gBsPrM" data-cy="country-complete-name" data-row-id="country-medal-row-(\d*)">(.*)</div>')

# 1，爬取网页
def getData(url):

    datalist=[]
    for item in url: #调用获取页面信息的函数
        sea = ''
        medals = []
        countries = []
        url = item[1]+str('/medals')
        print(url)
        html=askURL(url)#保存获取到的网页源码
        time.sleep(30)
        # 2，逐一解析数据
        soup=BeautifulSoup(html,"html.parser")
        num=0
        sea=item[0]

        for item in soup.find_all('div',class_="Medalstyles__Wrapper-sc-1tu6huk-0 kXFxTL"): #查找符合要求的字符串，形成列表
            medal = re.findall(findMedal, str(item))
            if len(medal) == 0:
                medal = [('0','0')]
            medals.append(medal[0][1])


        for item2 in soup.find_all('div',class_="styles__CountryCompleteName-sc-fehzzg-3 gBsPrM"):
            country=re.findall(findCountry,str(item2))
            countries.append(country[0][1].replace("\r", ""))

        for n in range(len(countries)):
            data=[]
            data.append(sea)
            data.append(countries[n])
            for num in range(0,4):
                data.append(medals[4*n+num])
            print(data)
            datalist.append(data)


    for data in datalist:
        print(data)
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
        response=urllib.request.urlopen(request,timeout=30)
        html=response.read().decode("utf-8")
        #print("完了"+html+"好像是")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

def getUrl(dbpath):
    conn=sqlite3.connect(dbpath)#打开或创建数据库文件
    cursor=conn.cursor()#获取游标
    sql='''select name,url from urlList'''
   #执行sql语句
    list=cursor.execute(sql)
    conn.commit()#提交数据库操作
    #cursor.close()
    #conn.close()#关闭数据库连接
    return list


# 3，保存数据
def  saveData(datalist,savepath):
    #以utf-8编码创建一个Excel对象
    workbook=xlwt.Workbook(encoding="utf-8",style_compression=0)
    #创建一个Sheet表
    worksheet=workbook.add_sheet('奖牌数',cell_overwrite_ok=True)
    #单元格写入内容,(行，列，内容)
    col=("届数","国家","金牌","银牌","铜牌","总数",)
    for i in range(0,6):
        worksheet.write(0,i,col[i])
    for i in range(0,len(datalist)):
        print("第%d条"%(i+1))
        data=datalist[i]
        for j in range(0,6):
            worksheet.write(i+1,j,data[j])

    #保存表格
    workbook.save(savepath)
#
def saveToDB(datalist,dbpath):
    n=0
    initDB(dbpath)
    conn=sqlite3.connect(dbpath)#打开或创建数据库文件
    cursor=conn.cursor()#获取游标
    for row in datalist:
        row = datalist[n]
        n+=1
        sql='''
            insert into Medal
            (name,country,gold,silver,bronze,total)
            values
            ('%s','%s',%d,%d,%d,%d)'''% (str(row[0]),str(row[1]),int(row[2]),int(row[3]),int(row[4]),int(row[5]))
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
    sql='''
    create table Medal
    (
    id integer primary key  autoincrement,
    name varchar ,
    country varchar ,
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