import sqlite3

from flask import Flask, render_template
import random


def randomcolor():
    colorArr = ['#FFE4E1', '#FFF0F5', '#E6E6FA', '#F0F8FF', '#F5F5DC', '#F0FFF0', '#FFE4B5', '#C1CDC1', '#D8BFD8',
                '#FFC1C1', '#FFFFE0', '	#D1EEEE', '#87CEFA', '#B0C4DE', '#FFDAB9', '#FFDEAD', '#C6E2FF', '#E0EEE0',
                '#CAE1FF', '#BFEFFF', '	#BCD2EE']
    return colorArr[random.randint(0, len(colorArr) - 1)]


app = Flask(__name__)


@app.route('/')
def hello_world():
    list1 = []
    child = []
    listAll=[]
    con = sqlite3.connect("OlympicTest.db")
    cur = con.cursor()
    sql = "select country,count(country) from olympicGames group by country"
    data = cur.execute(sql)
    for item in data:
        listAll.append(item)
        dic = {"name": item[0],
               "itemStyle": randomcolor(),
               "children": child
               }
        list1.append(dic)

    for i in range(0, len(list1)):
        sql2 = "select name from olympicGames where country='%s'" % (list1[i]['name'])
        children = cur.execute(sql2)
        childs = []
        for n in children:
            c = {
                "name": n[0],
                "value": 1,
                "itemStyle": randomcolor()
            }
            childs.append(c)
        list1[i]['children'] = childs
    return render_template("index.html", relist=list1,listAll=listAll)


@app.route('/index')
def index():  # put application's code here
    return render_template("index.html")

@app.route('/athlete')
def athlete():  # put application's code here
    age = []
    con = sqlite3.connect("OlympicTest.db")
    cur = con.cursor()
    sql = "select count(*) from athlete_events where  Medal='Gold' and age>10 and age<20"
    data = cur.execute(sql)
    for item in data:
        age.append(item[0])
    sql = "select count(*) from athlete_events where  Medal='Gold' and age>=20 and age<30"
    data = cur.execute(sql)
    for item in data:
        age.append(item[0])
    sql = "select count(*) from athlete_events where  Medal='Gold' and age>=30 and age<40"
    data = cur.execute(sql)
    for item in data:
        age.append(item[0])
    sql = "select count(age) from athlete_events where  Medal='Gold' and age>=40 "
    data = cur.execute(sql)
    for item in data:
        age.append(item[0])

    numM=[]
    sql1="select games,count(*) from athlete_events where Sex='M'and Season='Summer'  group by games"
    data1 = cur.execute(sql1)
    for item in data1:
        numM.append(item)

    numF=[]
    sql2="select games,count(*) from athlete_events where Sex='F'and Season='Summer'  group by games"
    data2 = cur.execute(sql2)
    for item in data2:
        numF.append(item)

    numMW=[]
    sql3="select games,count(*) from athlete_events where Sex='M'and Season='Winter' group by games"
    data3 = cur.execute(sql3)
    for item3 in data3:
        numMW.append(item3)

    numFW=[]
    sql4="select games,count(*) from athlete_events where Sex='F'and Season='Winter' group by games"
    data4 = cur.execute(sql4)
    for item4 in data4:
        numFW.append(item4)

    return render_template("athlete.html",age=age,numM=numM,numF=numF,numMW=numMW,numFW=numFW)


@app.route('/winter')
def winter():  # put application's code here
    return render_template("winter.html")

@app.route('/team')
def team():  # put application's code here
    return render_template("team.html")

@app.route('/chart')
def chart():  # put application's code here
    list1 = []
    child = []

    con = sqlite3.connect("OlympicTest.db")
    cur = con.cursor()
    sql = "select country,count(country) from olympicGames group by country"
    data = cur.execute(sql)
    for item in data:
        dic = {"name": item[0],
               "itemStyle": randomcolor(),
               "children": child
               }
        list1.append(dic)

    for i in range(0, len(list1)):
        sql2 = "select name from olympicGames where country='%s'" % (list1[i]['name'])
        children = cur.execute(sql2)
        childs = []
        for n in children:
            c = {
                "name": n[0],
                "value": 1,
                "itemStyle": randomcolor()
            }
            childs.append(c)
        list1[i]['children'] = childs

    return render_template("chart.html", relist=list1)


@app.route('/tables')
def tables():
    datalist = []
    datalist1 = []
    datalist2 = []
    medal=[]
    medal1=[]
    medal2=[]
    conn = sqlite3.connect("OlympicTest.db")
    cur = conn.cursor()
    sql = "select * from olympicGames,urlList where olympicGames.name = urlList.name"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    sql1 = "select * from olympicGames where name like '%奥运会'"
    data1 = cur.execute(sql1)
    for item in data1:
        datalist1.append(item)
    sql2 = "select * from olympicGames where name like '%冬奥会'"
    data2 = cur.execute(sql2)
    for item in data2:
        datalist2.append(item)

    sql3="select * from Medal "
    data3 = cur.execute(sql3)
    for item in data3:
        medal.append(item)

    sql4="select * from Medal where name like '%奥运会'"
    data4 = cur.execute(sql4)
    for item in data4:
        medal1.append(item)

    sql5="select * from Medal where name like '%冬奥会'"
    data5 = cur.execute(sql5)
    for item in data5:
        medal2.append(item)

    cur.close()
    conn.close()
    return render_template("tables.html", datalist=datalist, datalist1=datalist1, datalist2=datalist2,medal=medal,medal1=medal1,medal2=medal2)

@app.route('/medal')
def medal():

    medal=[]
    medal1=[]
    medal2=[]
    conn = sqlite3.connect("OlympicTest.db")
    cur = conn.cursor()


    sql3="select * from Medal "
    data3 = cur.execute(sql3)
    for item in data3:
        medal.append(item)

    sql4="select * from Medal where name like '%奥运会'"
    data4 = cur.execute(sql4)
    for item in data4:
        medal1.append(item)

    sql5="select * from Medal where name like '%冬奥会'"
    data5 = cur.execute(sql5)
    for item in data5:
        medal2.append(item)

    cur.close()
    conn.close()
    return render_template("Medal.html",  medal=medal,medal1=medal1,medal2=medal2)


@app.route('/China')
def China():
    total = []
    name = []
    gold = []
    silver = []
    bronze = []
    name1 = []
    total1 = []
    total2 = []
    total3 = []
    total4 = [0, 0, 0]
    total5 = []
    totalw = []
    namew = []
    goldw = []
    silverw = []
    bronzew = []
    name1w = []
    total1w = []
    total2w = []
    total3w = []
    total4w = [0, 0, 0,0,0,0]
    total5w = []
    conn = sqlite3.connect("OlympicTest.db")
    cur = conn.cursor()
    sql = "select name,gold,silver,bronze,total from Medal  where country='中国'and name like '%奥运会' group by name"
    data = cur.execute(sql)
    for item in data:
        name.append(item[0])
        gold.append(item[1])
        silver.append(item[2])
        bronze.append(item[3])
        total.append(item[4])
    sql = "select name,total from Medal  where country='美国'and id>=560 and name like '%奥运会' group by name"
    data = cur.execute(sql)
    for item in data:
        name1.append(item[0])
        total1.append(item[1])
    sql = "select total from Medal  where country='法国'and id>=560 and name like '%奥运会' group by name"
    data = cur.execute(sql)
    for item in data:
        total2.append(item[0])
    sql = "select total from Medal  where country='英国'and id>=560 and name like '%奥运会' group by name"
    data = cur.execute(sql)
    for item in data:
        total3.append(item[0])
    sql = "select total from Medal  where country='中国'and id>=560 and name like '%奥运会' group by name"
    data = cur.execute(sql)
    for item in data:
        total4.append(item[0])
    sql = "select total from Medal  where country='日本'and id>=560 and name like '%奥运会' group by name"
    data = cur.execute(sql)
    for item in data:
        total5.append(item[0])

    #冬奥会
    sql = "select name,gold,silver,bronze,total from Medal  where country='中国'and name like '%冬奥会' group by name"
    data = cur.execute(sql)
    for item in data:
        namew.append(item[0])
        goldw.append(item[1])
        silverw.append(item[2])
        bronzew.append(item[3])
        totalw.append(item[4])
    sql = "select name,total from Medal  where country='美国'and id>=545 and name like '%冬奥会' group by name"
    data = cur.execute(sql)
    for item in data:
        name1w.append(item[0])
        total1w.append(item[1])
    sql = "select total from Medal  where country='挪威'and id>=545 and name like '%冬奥会' group by name"
    data = cur.execute(sql)
    for item in data:
        total2w.append(item[0])
    sql = "select total from Medal  where country='芬兰'and id>=545 and name like '%冬奥会' group by name"
    data = cur.execute(sql)
    for item in data:
        total3w.append(item[0])
    sql = "select total from Medal  where country='中国'and id>=545 and name like '%冬奥会' group by name"
    data = cur.execute(sql)
    for item in data:
        total4w.append(item[0])
    sql = "select total from Medal  where country='瑞典'and id>=545 and name like '%冬奥会' group by name"
    data = cur.execute(sql)
    for item in data:
        total5w.append(item[0])
    sport = []
    child = []
    sql = "select sport,gold,silver,bronze,total from ChinaMedal where season='Summer'"
    data = cur.execute(sql)
    sport = []
    for item in data:
        data1 = []
        sname = item[0] + ":" + "🥇" + str(item[1]) + "🥈" + str(item[2]) + "🥉" + str(item[3])
        data1.append(sname)
        data1.append(item[4])
        sport.append(data1)

    sport1 = []
    sql = "select sport,gold,silver,bronze,total from ChinaMedal where season='Winter'"
    data = cur.execute(sql)

    for item in data:
        data2 = []
        sname1 = item[0] + ":" + "🥇" + str(item[1]) + "🥈" + str(item[2]) + "🥉" + str(item[3])
        data2.append(sname1)
        data2.append(item[4])
        sport1.append(data2)

    cur.close()
    conn.close()
    return render_template("China.html", total1=total1, name1=name1, total2=total2, total3=total3, total4=total4,
                           total5=total5, total=total, name=name, gold=gold, silver=silver, bronze=bronze,
                           total1w=total1w, name1w=name1w, total2w=total2w, total3w=total3w, total4w=total4w,
                           total5w=total5w, totalw=totalw, namew=namew, goldw=goldw, silverw=silverw, bronzew=bronzew,
                           sport=sport,sport1=sport1)


@app.route('/most')
def most():
    data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11,data12,data13,data14,data15 = [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
    con = sqlite3.connect("OlympicTest.db")
    cur2 = con.cursor()
    sql1 = 'select country, count(*) from olympicGames group by country order by count(*) desc limit 3'
    datalist1 = cur2.execute(sql1)
    for item in datalist1:
        data1.append(item)

    sql2 = "select name,athletes from olympicGames where name like '%奥运会%' order by athletes desc limit 3"
    datalist2 = cur2.execute(sql2)
    for item in datalist2:
        data2.append(item)
    sql3 = "select name,athletes from olympicGames where name like '%冬奥会%' order by athletes desc limit 3"
    datalist3 = cur2.execute(sql3)
    for item in datalist3:
        data3.append(item)
    sql4 = "select name,team from olympicGames where name like '%奥运会%' order by team desc limit 3"
    datalist4 = cur2.execute(sql4)
    for item in datalist4:
        data4.append(item)
    sql5 = "select name,team from olympicGames where name like '%冬奥会%' order by team desc limit 3"
    datalist5 = cur2.execute(sql5)
    for item in datalist5:
        data5.append(item)
    sql6 = "select name,sports from olympicGames where name like '%奥运会%' order by sports desc limit 3"
    datalist6 = cur2.execute(sql6)
    for item in datalist6:
        data6.append(item)
    sql7 = "select name,sports from olympicGames where name like '%冬奥会%'  order by sports desc limit 3"
    datalist7 = cur2.execute(sql7)
    for item in datalist7:
        data7.append(item)
    sql8 = "select name,country,total from Medal where name like '%奥运会%'  order by total desc limit 3"
    datalist8 = cur2.execute(sql8)
    for item in datalist8:
        data8.append(item)
    sql9 = "select name,country,total from Medal where name like '%冬奥会%'  order by total desc limit 3"
    datalist9 = cur2.execute(sql9)
    for item in datalist9:
        data9.append(item)
    sql10 = "select name,country,gold from Medal where name like '%奥运会%'  order by gold desc limit 3"
    datalist10 = cur2.execute(sql10)
    for item in datalist10:
        data10.append(item)
    sql11 = "select name,country,gold from Medal where name like '%冬奥会%'  order by gold desc limit 3"
    datalist11 = cur2.execute(sql11)
    for item in datalist11:
        data11.append(item)
    sql12 = "select name,Age,Team,Games,Sport,Event,Medal from athlete_events where Medal !='NA' and Season='Summer' order by Age desc limit 3"
    datalist12 = cur2.execute(sql12)
    for item in datalist12:
        data12.append(item)
    sql13 = "select name,Age,Team,Games,Sport,Event,Medal from athlete_events where Medal !='NA' and Season='Winter' order by Age desc limit 3"
    datalist13 = cur2.execute(sql13)
    for item in datalist13:
        data13.append(item)
    sql14 = "select name,Height,Team,Games,Sport,Event,Medal from athlete_events where Medal !='NA' and Season='Summer' AND Height!='NA' GROUP BY NAME  order by Height desc  limit 3"
    datalist14 = cur2.execute(sql14)
    for item in datalist14:
        data14.append(item)
    sql15 = "select name,Height,Team,Games,Sport,Event,Medal from athlete_events where Medal !='NA' and Season='Winter' AND Height!='NA' GROUP BY NAME  order by Height desc  limit 3"
    datalist15 = cur2.execute(sql15)
    for item in datalist15:
        data15.append(item)
    return render_template("Most.html", data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6,
                           data7=data7, data8=data8, data9=data9, data10=data10, data11=data11,data12=data12,
                           data13=data13,data14=data14,data15=data15 )




if __name__ == '__main__':
    app.run()
