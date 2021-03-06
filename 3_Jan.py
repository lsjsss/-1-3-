import requests
import re

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"

def parsePage(ilt,html):
    try:
        vedio_titles = re.findall(r'<a title=\".*?\"', html)
        vedio_links = re.findall(r'a href=\"//www.bilibili.com/video/av.*?\"', html)
        up_names = re.findall(r'up-name\">.*?</a>', html)
        up_links = re.findall(r'a href=\"//space.bilibili.com/.*?\"', html)
        watch_nums = re.findall(r'icon-playtime\"></i>.*?</span>', html, re.S)
        subtitle_nums = re.findall(r'icon-subtitle\"></i>.*?</span>', html, re.S)
        up_dates = re.findall(r'icon-date\"></i>.*?</span>', html, re.S)
        for i in range(len(vedio_titles)):
            vedio_title = vedio_titles[i].split('"')[1]
            vedio_link = re.split(r'"//|"', vedio_links[i])[1]
            up_name = re.split(r'">|</', up_names[i])[1]
            up_link = re.split(r'"//|"', up_links[i])[1]
            watch_num = re.split(r'\n', watch_nums[i])[1]
            subtitle_num = re.split(r'\n', subtitle_nums[i])[1]
            up_date = re.split(r'\n', up_dates[i])[1]
            ilt.append([vedio_title, vedio_link, up_name, up_link, watch_num, subtitle_num, up_date])
    except Exception as e:
        print(e)


def printUSERList(ilt):
    tplt = "{:4}\t{:10}\t{:20}\t{:10}\t{:20}\t{:4}\t{:4}\t{:10}"
    print(tplt.format("视频编号", "视频标题", "视频链接", "up主", "up主主页链接", "播放量", "弹幕量", "上传时间"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1], g[2], g[3], g[4], g[5], g[6]))

def saveUSERList(ilt):
    with open("D://doctor_ups.txt", "a", encoding='utf-8') as f:
        f.write("视频标题"+"\t"+"视频链接"+"\t"+ "up主"+"\t"+ "up主主页链接" + "\t" + "播放量"+"\t"+ "弹幕量"+"\t"+ "上传时间"+"\t"+"\n")
        for i in ilt:
            for j in i:
                f.write(j +"\t")
            f.write("\n")
        f.close()

def main():
    kw = "博士"
    depth = 50
    start_url = "https://search.bilibili.com/all?keyword=" + str(kw) + "&from_source=nav_search_new&page="
    doctorList = []
    for i in range(depth):
        try:
           url = start_url + str(i+1)
           html = getHTMLText(url)
           parsePage(doctorList, html)
        except:
            continue
    printUSERList(doctorList)
    saveUSERList(doctorList)

main()
