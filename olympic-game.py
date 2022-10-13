# -*- codeing = utf-8 -*-
# @Time: 2022/4/10 15:41
# @Author:0304190209 李梦婷
# @File : olympic-game.py
# @Software: PyCharm

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re  # 正则表达式，文字匹配
import urllib.request, urllib.error  # 制定URL，获取网页数据
import xlwt  # 进行EXCEL操作
import sqlite3  # 进行SQLITE数据库操作
import time

def main():
    #baseurl="https://olympics.com/zh/olympic-games/beijing-2022"
    urlList=getUrl("OlympicTest.db")
     #1，爬取网页
    datalist=getData(urlList)
    #datalist=getData(baseurl)
    savepath=".\\历届奥运会.xls"
    # 3，保存数据
    saveData(datalist,savepath)
    #askURL(baseurl)
    saveToDB(datalist,"OlympicTest.db")

findName=re.compile(r'<h1 class="styles__Title-sc-1w4me2-1 HngV">(.*)<br/>')
findCountry=re.compile(r'<div class="styles__FactItems-sc-1w4me2-2 daFleI"><span>国家</span>(.*?)</div>')
findDate=re.compile(r'<div class="styles__FactItems-sc-1w4me2-2 daFleI"><span>日期</span>(.*?)</div>')
findAthletes=re.compile(r'<div class="styles__FactItems-sc-1w4me2-2 daFleI"><span>运动员</span>(\d*)</div>')
findTeam=re.compile(r'<div class="styles__FactItems-sc-1w4me2-2 daFleI"><span>运动队</span>(\d*)</div>')
findSports=re.compile(r'<div class="styles__FactItems-sc-1w4me2-2 daFleI"><span>赛事</span>(\d*)</div>')
findVideo=re.compile(r'<a class="secondary" data-cy="next-link" href="(.*?)">')

# 1，爬取网页
def getData(urlList):
    datalist=[]

    for item in urlList: #调用获取页面信息的函数
        # url=item[0]
        print(item[0])
        html=askURL(item[0])#保存获取到的网页源码
        time.sleep(10)
        # 2，逐一解析数据
        soup=BeautifulSoup(html,"html.parser")
        for item in soup.find_all('section', class_="styles__Facts-sc-1w4me2-0 jtVoog"):
            data=[]
            data.append(re.findall(findName, str(item)))
            data.append(re.findall(findCountry, str(item)))
            data.append(re.findall(findDate, str(item)))
            data.append(re.findall(findAthletes, str(item)))
            data.append(re.findall(findTeam, str(item)))
            data.append(re.findall(findSports, str(item)))
            # data.append(re.findall(findVideo, str(item)))
            print(data)
            datalist.append(data)

    return datalist

#得到指定一个URL的网页内容
def askURL(url):
    #模拟浏览器头部信息，向其服务器发送消息

    head={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    }
    #用户代理表示告诉豆瓣服务器我们是什么类型的机器，浏览器，告诉浏览器我们能接受什么水平的文件
    request=urllib.request.Request(url,headers=head)
    html=''
    try:
        response=urllib.request.urlopen(request,timeout=10)
        html=response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

def getUrl(dbpath):
    conn=sqlite3.connect(dbpath)#打开或创建数据库文件
    cursor=conn.cursor()#获取游标
    sql='''select url from urlList'''
   #执行sql语句
    list=cursor.execute(sql)
    conn.commit()#提交数据库操作
    #cursor.close()
    #conn.close()#关闭数据库连接
    # for item in list:
    #     print(item[0])
    return list

# 3，保存数据
def  saveData(datalist,savepath):
        #以utf-8编码创建一个Excel对象
        workbook=xlwt.Workbook(encoding="utf-8",style_compression=0)
        #创建一个Sheet表
        worksheet=workbook.add_sheet('奥运会',cell_overwrite_ok=True)
        #单元格写入内容,(行，列，内容)
        col=("届数","国家","举办日期","运动员","运动队","赛事",)
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
    m=0
    conn=sqlite3.connect(dbpath)#打开或创建数据库文件
    cursor=conn.cursor()#获取游标
    for row in datalist:
        row=datalist[m]
        m+=1
        sql='''
            insert into olympicGames
            (name,country,date,athletes,team,sports,video)
            ('%s','%s','%s',%d,%d,%d)''' % (str(row[0]),str(row[1]),str(row[2]),int(row[3]),int(row[4]),int(row[5]))
        #执行sql语句
        cursor.execute(sql)
        conn.commit()#提交数据库操作
    cursor.close()
    conn.close()#关闭数据库连接
    print("已保存至数据库中")



def initDB(dbpath):
    sql='''
    create table olympicGames
    (
    id integer primary key  autoincrement,
    name varchar ,
    country varchar ,
    date varchar,
    athletes numeric ,
    team numeric ,
    sports numeric ,
    video text
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