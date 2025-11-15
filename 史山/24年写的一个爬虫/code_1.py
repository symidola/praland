#coding = utf-8
import urllib.error
import urllib.request
from bs4 import BeautifulSoup
import re
import xlwt
import pandas as pd
from openai import OpenAI
import matplotlib.pyplot as plt
from pylab import mpl
# 设置显示中文字体
mpl . rcParams [ "font.sans-serif" ] = [ "SimHei" ]
# 有时候，字体更改后，会导致坐标轴中的部分字符无法正常显示，此时需要更改 axes.unicode_minus 参数：
mpl . rcParams [ "axes.unicode_minus" ] = False
def spid(url):                #获取网页内容
    headers = {'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8','Accept-Encoding': 'gzip, deflate, br, zstd','Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6','Cache-Control': 'no-cache','Connection': 'keep-alive','Cookie':' _trs_uv=m987cg07_6252_acn; _trs_ua_s_1=m99z9uuf_6252_i630; Hm_lvt_c758855eca53e5d78186936566552a13=1744098716,1744187917,1744206093; ,HMACCOUNT=A054B1500077CAA9; Hm_lpvt_c758855eca53e5d78186936566552a13=1744206263','Host': 'weather.cma.cn','Pragma': 'no-cache','Referer': 'https://weather.cma.cn/web/weather/54857.html','Sec-Fetch-Dest': 'image','Sec-Fetch-Mode': 'no-cors','Sec-Fetch-Site': 'same-origin','User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0','sec-ch-ua': '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"','sec-ch-ua-mobile':' ?0','sec-ch-ua-platform': '"Windows"'}
    req = urllib.request.Request(url=url,headers=headers)
    try:
        resp=urllib.request.urlopen(req,timeout=4)
        respp=resp.read().decode("utf-8")
        return respp
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
def weth7day(urlfile):     #获取未来七天的天气数据
    we7d = []
    var1 = urlfile.find_all(class_='row hb days')
    var2 = var1[0].find_all(text=re.compile("\S"))
    for j in var2:
        outp = re.search("\S+",j).group()
        we7d.append(outp)
    return we7d
def weth24h(urlfile):      #获取今日24h内的天气数据
    we24h = []
    lis1 = urlfile.find_all("tr")
    for k in range(0,9):
        lis2 = lis1[k].find_all("td")
        for i in lis2:
            we24h.append(i.string)
    return we24h
def chartcre(bs):          #创建关于天气数据的表格
    workbook = xlwt.Workbook(encoding="utf-8")
    workbook2 = xlwt.Workbook(encoding="utf-8")
    worksheet =  workbook.add_sheet("sheet1")
    worksheet.write(0,0,"日期")
    worksheet.write(0,1,"时间")
    worksheet.write(0,2,"晨间天气")
    worksheet.write(0,3,"晨间风向")
    worksheet.write(0,4,"晨间风强")
    worksheet.write(0,5,"晨间温度")
    worksheet.write(0,6,"夜间温度")
    worksheet.write(0,7,"夜间天气")
    worksheet.write(0,8,"夜间风向")
    worksheet.write(0,9,"夜间风强")
    flag=0
    lineflag=1
    for i in weth7day(bs):
        worksheet.write(lineflag,flag,i)
        flag+=1
        if flag==10:
            flag=0
            lineflag+=1
    worksheet2 =  workbook2.add_sheet("sheet2")
    worksheet2.write(0,0,"时间")
    worksheet2.write(0,1,"气温")
    worksheet2.write(0,2,"降水情况")
    worksheet2.write(0,3,"风速")
    worksheet2.write(0,4,"风向")
    worksheet2.write(0,5,"气压")
    worksheet2.write(0,6,"湿度")
    worksheet2.write(0,7,"云量")
    flag2=0
    lineflag2=1
    for o in weth24h(bs):
        if o == None :
            continue
        else:
            worksheet2.write(lineflag2,flag2,o)
            lineflag2+=1
            if lineflag2 == 9:
                lineflag2=1
                flag2+=1
    workbook.save("we_rp")
    workbook2.save("we_rp2") 
def aianaly(sheet1str,sheet2str):  #使用deepseek分析天气数据
    client = OpenAI(api_key="sk-0a88fc685e9244d3b038d9b329a479de", base_url="https://api.deepseek.com")
    contentx = "请为我分析以下关于青岛未来七日的天气数据:"+"\n"+sheet1str
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": contentx},
        ],
        stream=False
    )

    print(response.choices[0].message.content)
    client = OpenAI(api_key="sk-0a88fc685e9244d3b038d9b329a479de", base_url="https://api.deepseek.com")
    contentxx = "请为我分析以下关于青岛今日的天气数据:"+"\n"+sheet2str
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": contentxx},
        ],
        stream=False
    )

    print(response.choices[0].message.content)
def exc(list1):            #将摄氏度温度转为整数便于制表
    tdlst = []
    for i in list1:
        ele = int(re.search("\d*",i).group())
        tdlst.append(ele)
    return tdlst           #将摄氏度温度转为小数便于制表
def exc2(list1):           #将摄氏度温度转为小数便于制表
    tdlst = []
    for i in list1:
        ele = float(re.search("\d*.\d",i).group())
        tdlst.append(ele)
    return tdlst
def plotcre7():            #生成未来七天温度状况
    data = pd.read_excel("we_rp")
    date1 = data["时间"].tolist()
    tempd = data["晨间温度"].tolist()
    tempn = data["夜间温度"].tolist()
    tempdi = exc(tempd)
    tempni = exc(tempn)
    x = date1
    yd = tempdi
    yn = tempni
    plt.figure(figsize=(20, 8), dpi=40)
    y_ticks = range(40)
    plt.yticks(y_ticks[::1])
    # 2.绘制折线图
    plt.plot(x, yd,c="r")
    plt.plot(x, yn,c="g")
    # 3.显示图像
    plt.xlabel("时间")
    plt.ylabel("温度(℃)")
    plt.title("未来七日日间温度变化", fontsize=20)
    plt.show()
def plotcre24():
    data = pd.read_excel("we_rp2")
    date1 = data["时间"].tolist()
    tempd = data["气温"].tolist()
    tempdi = exc(tempd)
    x = date1
    yd = tempdi
    plt.figure(figsize=(20, 8), dpi=40)
    y_ticks = range(40)
    plt.yticks(y_ticks[::1])
    # 2.绘制折线图
    plt.plot(x, yd,c="b",marker="*")
    # 3.显示图像
    plt.xlabel("时间")
    plt.ylabel("温度(℃)")
    plt.title("今日24小时间温度变化", fontsize=20)
    plt.show()
def wet24():
    data = pd.read_excel("we_rp2")
    date1 = data["时间"].tolist()
    we = data["湿度"].tolist()
    ca = data['云量'].tolist()
    xt=range(1,92,12)
    xt2=range(2,92,12)
    wei = exc(we)
    cai = exc(ca)
    x = date1
    bar_width = 1
    plt.figure(figsize=(20, 8), dpi=40)
    y_ticks = range(105)
    plt.yticks(y_ticks[::5])
    plt.xticks(xt,x)
    plt.xlim(-1,94)
    # 2.绘制折线图
    plt.bar(xt, wei)
    plt.bar(xt2, cai,bar_width,color="r")
    # 3.显示图像
    plt.xlabel("时间")
    plt.ylabel("湿度（蓝），云量（红）")
    plt.title("24小时内的湿度与云量", fontsize=20)
    plt.show()
if __name__ == "__main__": #启动！！！
    url = "https://weather.cma.cn/web/weather/54857.html"
    print("若出现timeout报错重新运行即可(可能要重复几次)")
    try:     #爬取中国气象网山东青岛的气象信息
        html = spid(url)
        bs = BeautifulSoup(html,"html.parser")
        try:
            bs = BeautifulSoup(html,"html.parser")
            chartcre(bs)
            sheet1=pd.read_excel("we_rp")
            sheet1str=str(sheet1)
            print(sheet1str)
            sheet2=pd.read_excel("we_rp2")
            sheet2str=str(sheet2)
            print(sheet2str)
        except:
            print("error")
        try:
            aianaly(sheet1str,sheet2str)
        except:
            print("aierror")
        try:
            plotcre7()
            plotcre24()
            wet24()
        except:
            print("charterror")
    except:
        print("timeout")
