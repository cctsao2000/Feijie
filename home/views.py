from django.shortcuts import render
from datetime import datetime
import matplotlib.pyplot as plt
import sqlite3 as db

def conSearch(keyword):
    if(len(keyword) == 0):
        command = (f"SELECT Consumable_ID, Consumable_Name, Consumable_Quantity FROM Consumable")
    elif keyword[0] == "C" and len(keyword)<=3:
        command = (f"SELECT Consumable_ID, Consumable_Name, Consumable_Quantity FROM Consumable WHERE Consumable_ID = '{keyword}'")
    else:
        command = (f"SELECT Consumable_ID, Consumable_Name, Consumable_Quantity FROM Consumable WHERE Consumable_Name LIKE '%{keyword}%'")
    queryResult = dbSearchList(command)
    result = []
    for i in queryResult:
        row = list(i)
        row.append(calROP(row[0],datetime.now().month))
        row.append(calEOQ(row[0]))
        row.insert(0,orderAlert(row[0],datetime.now().month))
        result.append(row)
    return result

def empSearch(keyword):
    if(len(keyword) == 0):
        command = (f"SELECT * FROM Employee")
    elif keyword[0] == "E" and len(keyword)<=3:
        command = (f"SELECT * FROM Employee WHERE Employee_ID = '{keyword}'")
    else:
        command = (f"SELECT * FROM Employee WHERE Employee_Name LIKE '%{keyword}%'")
    return dbSearchList(command)

def cusSearch(keyword):
    if(len(keyword) == 0):
        command = (f"SELECT * FROM Customer")
    elif keyword[0] == "A" and len(keyword)<=3:
        command = (f"SELECT * FROM Customer WHERE Customer_ID = '{keyword}'")
    else:
        command = (f"SELECT * FROM Customer WHERE Customer_Name LIKE '%{keyword}%'")
    return dbSearchList(command)

def checkConsumableAlert():
    alertList = []
    i = 1
    while i <= 21:
        productID = "C" + str(i)
        if orderAlert(productID,datetime.now().month) == True:
            alertList.append(productID)
        i += 1
    print(alertList)
    return alertList

def productOrder(productID):
    calEOQ(productID)
    calROP(productID,datetime.now().month)

def salesSearch(month,year):
    sales(month,year)

def salesGrowthSearch(before,after,year):
    sgr(before,after,year)

def salesPlot(year):
    showSales(year)
    showSgr(year)

def rateSearch(period,year):
    rr(period,year)
    sr(period,year)
    lr(period,year)

def aitSearch(customerID,period):
    ait(customerID,period)

def rfmSearch(period):
    rfm(period)

# mm
# 銷售額
def sales(time, year):
    conn = db.connect('db.sqlite3')
    conn.row_factory = db.Row
    cursor = conn.cursor()
    cursor.execute("select Order_Time, Order_Amount from Order_All")
    rows = cursor.fetchall()

    sum = 0
    for row in rows:
        if year + '-' + time in row[0]:
            sum += row[1]
    
    conn.close()
    
    return sum

# 顯示銷售額狀況
def showSales(year):
    x = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12
    ]
    
    y = [
        sales('01', year),
        sales('02', year),
        sales('03', year),
        sales('04', year),
        sales('05', year),
        sales('06', year),
        sales('07', year),
        sales('08', year),
        sales('09', year),
        sales('10', year),
        sales('11', year),
        sales('12', year)
    ]

    plt.title('Sales of ' + year)
    plt.xlabel('Month')
    plt.ylabel('Sales')
    plt.plot(x, y, marker=".")

    return plt.show()

# 銷售成長率(月): (本期銷售額-上期銷售額)/上期銷售額
def sgr(time_before, time_after, year):
    conn = db.connect('db.sqlite3')
    conn.row_factory = db.Row
    cursor = conn.cursor()
    cursor.execute("select Order_Time, Order_Amount from Order_All")
    rows = cursor.fetchall()
    
    sum_before = 0
    for row in rows:
        if year + '-' + time_before in row[0]:
            sum_before += row[1]
    
    sum_after = 0
    for row in rows:
        if year + '-' + time_after in row[0]:
            sum_after += row[1]
    
    sgr = (sum_after - sum_before) / sum_before

    conn.close()
    
    return sgr

# 顯示銷售成長率狀況
def showSgr(year):
    x = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12
    ]
    
    y = [
        0,
        sgr('01', '02', year),
        sgr('02', '03', year),
        sgr('03', '04', year),
        sgr('04', '05', year),
        sgr('05', '06', year),
        sgr('06', '07', year),
        sgr('07', '08', year),
        sgr('08', '09', year),
        sgr('09', '10', year),
        sgr('10', '11', year),
        sgr('11', '12', year)
    ]

    plt.title('Sales Growth Rate of ' + year)
    plt.xlabel('Month')
    plt.ylabel('Sales Growth Rate')
    plt.plot(x, y, marker=".")
    
    return plt.show()

# 留存率(月): 現在仍購買顧客數/之前購買的顧客數
def rr(t, year):
    conn = db.connect('db.sqlite3')
    conn.row_factory = db.Row
    cursor = conn.cursor()
    cursor.execute("select Order_Time, Customer_ID from Order_All")
    rows = cursor.fetchall()
    
    t = int(t)
    year = int(year)
    
    time_before = ''
    time_after = ''
    if t in range(1, 9):
        time_before = '0' + str(t)
        time_after = '0' + str((t + 1))
    elif t == 9:
        time_before = '0' + str(t)
        time_after = str((t + 1))
    elif t in range(10, 12):
        time_before = str(t)
        time_after = str((t + 1))
    
    customer_before = []
    customer_after = []
    customer_same = []
    
    for row in rows:
        if str(year) + '-' + time_before in row[0]:
            customer_before.append(row[1])
        
        if str(year) + '-' + time_after in row[0]:
            customer_after.append(row[1])
    
    for customer in customer_after:
        if customer in customer_before:
            customer_same.append(customer)

    rr = float(len(customer_same) / len(customer_before))
    
    conn.close()
    
    return rr

# 存活率(月):
def sr(t, year):
    t = int(t)
    
    if t == 1:
        sr_final = float(rr(t, year))
    else:
        sr_final = float(rr(t, year)) * float(sr(str(t-1), year))
    
    return sr_final
        
# 流失率(月): 1-rr
def lr(t, year):
    lr = float(1 - rr(t, year))
    return lr

# 平均購買間隔時間: 1/某特定期間內的購買次數
def ait(customerID, period):
    conn = db.connect('db.sqlite3')
    conn.row_factory = db.Row
    cursor = conn.cursor()
    
    if period == '30days':
        cursor.execute("SELECT * FROM Order_All WHERE Customer_ID=? AND julianday('now') - julianday(Order_Time) <= 30", (customerID,))
        rows = cursor.fetchall()
        li = []
        for row in rows:
            li.append(row[0])
        if len(li) == 0:
            ait = customerID + ' 在這段時間沒購買任何東西喔!'
            conn.close()
            return ait
        else:
            ait = customerID + ' 的平均購買間隔時間是 ' + str(1 * 30 / len(li)) + ' 天'
            conn.close()
            return ait
    
    elif period == '90days':
        cursor.execute("SELECT * FROM Order_All WHERE Customer_ID=? AND julianday('now') - julianday(Order_Time) <= 90", (customerID,))
        rows = cursor.fetchall()
        li = []
        for row in rows:
            li.append(row[0])
        if len(li) == 0:
            ait = customerID + ' 在這段時間沒購買任何東西喔!'
            conn.close()
            return ait
        else:
            ait = customerID + ' 的平均購買間隔時間是 ' + str(1 * 90 / len(li)) + ' 天'
            conn.close()
            return ait
    
    elif period == '180days':
        cursor.execute("SELECT * FROM Order_All WHERE Customer_ID=? AND julianday('now') - julianday(Order_Time) <= 180", (customerID,))
        rows = cursor.fetchall()
        li = []
        for row in rows:
            li.append(row[0])
        if len(li) == 0:
            ait = customerID + ' 在這段時間沒購買任何東西喔!'
            conn.close()
            return ait
        else:
            ait = customerID + ' 的平均購買間隔時間是 ' + str(1 * 180 / len(li)) + ' 天'
            conn.close()
            return ait
    
    elif period == '365days':
        cursor.execute("SELECT * FROM Order_All WHERE Customer_ID=? AND julianday('now') - julianday(Order_Time) <= 365", (customerID,))
        rows = cursor.fetchall()
        li = []
        for row in rows:
            li.append(row[0])
        if len(li) == 0:
            ait = customerID + ' 在這段時間沒購買任何東西喔!'
            conn.close()
            return ait
        else:
            ait = customerID + ' 的平均購買間隔時間是 ' + str(1 * 365 / len(li)) + ' 天'
            conn.close()
            return ait
    
    elif period == 'sofar':
        cursor.execute("select Order_Time from Order_All where Customer_ID=?", (customerID,))
        rows = cursor.fetchall()
        li = []
        for row in rows:
            li.append(row[0])
        if len(li) == 0:
            ait = customerID + ' 在這段時間沒購買任何東西喔!'
            conn.close()
            return ait
        else:
            ait = customerID + ' 的平均購買間隔時間是 ' + str(1 * 365 / len(li)) + ' 天'
            conn.close()
            return ait

#RFM-recency
def recency(customerID):
    conn = db.connect('db.sqlite3')
    conn.row_factory = db.Row
    cursor = conn.cursor()
    cursor.execute("select Order_Time from Order_All where Customer_ID = ? order by Order_Time DESC Limit 1", (customerID,))
    rows = cursor.fetchall()
    
    Now = datetime.now()
    data = ''
    for row in rows:
        data += row['Order_Time']
    data = data.split('-')
    before = datetime(int(data[0]), int(data[1]), int(data[2]))
    rec = (Now - before).days
    
    conn.close()
    
    return rec

#RFM-frequency
def frequency(customerID, period):
    if ait(customerID, period) == customerID + ' 在這段時間沒購買任何東西喔!':
        return 0
    
    else:
        days = float(ait(customerID, period).rstrip(' 天').lstrip(customerID + ' 的平均購買間隔時間是 '))
        freq = int(1 * 365 / days)
    
    return freq

#RFM-monetary value
def monetaryValue(customerID):
    conn = db.connect('db.sqlite3')
    conn.row_factory = db.Row
    cursor = conn.cursor()
    cursor.execute("select Order_Amount from Order_All where Customer_ID=?", (customerID,))
    rows = cursor.fetchall()
    
    sum = 0
    for row in rows:
        sum += row[0]
    sum = int(sum)

    conn.close()
    
    return sum

#RFM-show
def rfm(period):
    conn = db.connect('db.sqlite3')
    conn.row_factory = db.Row
    cursor = conn.cursor()
    cursor.execute("select Customer_ID, Customer_Name from Customer")
    rows = cursor.fetchall()

    li = []
    for row in rows:
        li.append([row[0], recency(row[0]), frequency(row[0], period), monetaryValue(row[0]), row[1]])
    
    li_1 = []
    li_2 = []
    
    li = sorted(li, key=lambda x: x[1]) #用recency排序
    
    i = 0
    for thing in li:
        if i == len(li):
            break
        if i < int(len(li)/2):
            li_1.append(thing)
            i += 1
        else:
            li_2.append(thing)
            i += 1
    
    li_1 = sorted(li_1, key=lambda x: x[2]) #用frequency排序
    li_2 = sorted(li_2, key=lambda x: x[2]) #用frequency排序
    
    li_3 = [] #新客戶群
    li_4 = [] #VIP客戶群
    li_5 = [] #潛在客戶群
    li_6 = [] #流失客戶群
    
    j = 0
    for thing in li_1:
        if j == len(li_1):
            break
        if j < int(len(li_1)/2):
            li_3.append(thing)
            j += 1
        else:
            li_4.append(thing)
            j += 1
    
    k = 0
    for thing in li_2:
        if k == len(li_2):
            break
        if k < int(len(li_2)/2):
            li_5.append(thing)
            k += 1
        else:
            li_6.append(thing)
            k += 1
    
    li_3 = sorted(li_3, reverse=True, key=lambda x: x[3]) #用monetary value排序
    li_4 = sorted(li_4, reverse=True, key=lambda x: x[3]) #用monetary value排序
    li_5 = sorted(li_5, reverse=True, key=lambda x: x[3]) #用monetary value排序
    li_6 = sorted(li_6, reverse=True, key=lambda x: x[3]) #用monetary value排序
    
    for customer in li_3:
        customer.insert(0, '新客戶群')
    
    for customer in li_4:
        customer.insert(0, 'VIP客戶群')
    
    for customer in li_5:
        customer.insert(0, '潛在客戶群')
    
    for customer in li_6:
        customer.insert(0, '流失客戶群')
    
    result = [li_3, li_4, li_5, li_6]
    
    return result

CONSUMECOE = 300
# 作業管理功能
# 訂購時間與訂購量安排試算
# - 撰寫計算各項耗材安全存量函式
# - 撰寫計算訂購時間函式


def dbSearchCon(command,productID):
    con = db.connect("db.sqlite3")
    cur = con.cursor()
    result = cur.execute(command,(productID,)).fetchone()
    con.close()
    return result

def dbSearchList(command):
    con = db.connect("db.sqlite3")
    cur = con.cursor()
    result = cur.execute(command).fetchall()
    con.close()
    return result

def getDemand(productID): # 年需求量
    sqlCommand = "SELECT Total_Use FROM TConsumable WHERE Consumable_ID = ?"
    demand = dbSearchCon(sqlCommand,productID)[0]
    return demand*CONSUMECOE
def getSetup(productID): # 訂購成本
    sqlCommand = "SELECT Order_Cost FROM Consumable WHERE Consumable_ID = ?"
    setup = dbSearchCon(sqlCommand,productID)[0]
    return setup
def getHold(productID): # 持有成本
    sqlCommand = "SELECT Carrying_Cost FROM Consumable WHERE Consumable_ID = ?"
    hold = dbSearchCon(sqlCommand,productID)[0]
    return hold
def getLT(productID):
    sqlCommand = "SELECT Request_Time FROM Consumable WHERE Consumable_ID = ?"
    lt = dbSearchCon(sqlCommand,productID)[0]
    return lt
def getStd(productID):
    sqlCommand = "SELECT Request_Time_Std FROM Consumable WHERE Consumable_ID = ?"
    std = dbSearchCon(sqlCommand,productID)[0]
    return std
def getStock(productID):
    sqlCommand = "SELECT Consumable_Quantity FROM Consumable WHERE Consumable_ID = ?"
    stock = dbSearchCon(sqlCommand,productID)[0]
    return stock

highlowMonth = { # 預測：時間序列 -- 季節
1:"low",2:"high",3:"normal",4:"normal",
5:"high",6:"high",7:"low",8:"low",
9:"high",10:"normal",11:"normal",12:"high"}
zVal = {"high":2.33,"normal":1.65,"low":1.28} # 服務水準 99%; 95%; 90%
monthRate = {"high":0.12,"normal":0.07,"low":0.04} # 月需求量比例

# EOQ 最佳訂購量
def calEOQ(productID):
    d = getDemand(productID)
    s = getSetup(productID)
    h = getHold(productID)
    eoq = round(((2*d*s)/h)**0.5) # EOQ = (2DS/H)**0.5
    return eoq

# ROP 再訂購點
def calROP(productID,month):
    dr = getDemand(productID)*monthRate[highlowMonth[month]]/30
    lt = getLT(productID)
    std = getStd(productID)
    rop = round(dr*lt+zVal[highlowMonth[month]]*std*(lt**0.5))
    return rop

#orderAlert
def orderAlert(productID,month):
    alert = ""
    if getStock(productID) < calROP(productID,month):
        alert = "Order Now"
    return alert

def getWeekdayOrder():
    con = db.connect("db.sqlite3")
    cur = con.cursor()
    command = "SELECT Order_Weekday, Count(*) FROM Order_All GROUP BY Order_Weekday"
    result = cur.execute(command).fetchall()
    resultNum = []
    hr = []
    for r in result:
        resultNum.append(r[1])
        hr.append(round(r[1]/4))
    con.close()
    return resultNum,hr

def getResEmp():
    resEmp = ["阿行","阿明、小資、阿奇","阿行、小花","阿明、小資","阿明、小資","阿行","阿行"] 
    return resEmp

def getAvgService():
    avgService = [8.0,7.5,8.1,7.9,7.9,8.0,8.0]
    return avgService
# Default: call all
employee_list = empSearch("")
customer_list = cusSearch("")
consumable_list = conSearch("")
schedule_list = getWeekdayOrder()[0]
hr = getWeekdayOrder()[1]
resEmployee_list = getResEmp()
avgService_list = getAvgService()

def index(request):
    return render(request, 'index.html')
def crm(request):
    if request.method == 'POST' and 'rateSearch' in request.POST:
        return render(request, 'crm.html', {'rr':rr(request.POST['period_rr'], request.POST['year_rr']), 'sr':sr(request.POST['period_sr'], request.POST['year_sr']), 'lr':lr(request.POST['period_lr'], request.POST['year_lr'])})
    elif request.method == 'POST' and 'aitSearch' in request.POST:
        return render(request, 'crm.html', {'ait':ait(request.POST['id'], request.POST['period_ait'])})
    elif request.method == 'POST' and 'rfmSearch' in request.POST:
        return render(request, 'crm.html', {'rfm':rfm(request.POST['period_rfm'])})
    else:
        return render(request, 'crm.html')
def ma(request):
    if request.method == 'POST' and 'salesSearch' in request.POST:
        return render(request, 'ma.html', {'sales':sales(request.POST['month_sales'], request.POST['year_sales'])})
    elif request.method == 'POST' and 'salesGrowthSearch' in request.POST:
        return render(request, 'ma.html', {'sgr':sgr(request.POST['time_before'], request.POST['time_after'], request.POST['year_sgr'])})
    # elif request.method == 'POST' and 'salesPlot' in request.POST:
    #     return render(request, 'ma.html', {'sales_plot':showSales(request.POST['year_plot_sales'])})
    # elif request.method == 'POST' and 'sgrPlot' in request.POST:
    #     return render(request, 'ma.html', {'sgr_plot':showSgr(request.POST['year_plot_sgr'])})
    else:
        return render(request, 'ma.html')
def cons(request):
    if request.method == 'POST' and 'search' in request.POST:
        return render(request,'cons.html',{'consumable_list':conSearch(request.POST['keyword'])})
    else:
        return render(request,'cons.html',{'consumable_list':consumable_list})
def emp(request):
    if request.method == 'POST' and 'search' in request.POST:
        return render(request,'emp.html',{'employee_list':empSearch(request.POST['keyword'])})
    else:
        return render(request,'emp.html',{'employee_list':employee_list})
def cus(request):
    if request.method == 'POST' and 'search' in request.POST:
        return render(request,'cus.html',{'customer_list':cusSearch(request.POST['keyword'])})
    else:
        return render(request,'cus.html',{'customer_list':customer_list})
def sch(request):
    if request.method == 'POST' and 'scheduling' in request.POST:


        return render(request,'sch.html',{'schedule_list':schedule_list,'hr_list':hr,'resEmployee_list':resEmployee_list,'avgService_list':avgService_list})
    else:
        return render(request,'sch.html',{'schedule_list':schedule_list,'hr_list':hr})
