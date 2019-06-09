# -*- coding:utf-8 -*-
#@Auhor : Agam
#@Time  : 2019-06-01
#@Email : agamgn@163.com
import requests
import lxml
import sys
from bs4 import BeautifulSoup
import xlwt
import time
import urllib


def craw(url, key_word, x):
    User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'
    #    if x == 0:
    #        re = 'http://www.qichacha.com/search?key='+key_word
    #    else:
    #        re = 'https://www.qichacha.com/search?key={}#p:{}&'.format(key_word,x-1)
    re = r'https://www.qichacha.com/search?key=' + key_word
    headers = {
        'Host': 'www.qichacha.com',
        'Connection': 'keep-alive',
        'Accept': r'text/html, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'Referer': re,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': r'xxxxxxxxx这里换成你的cookiexxxxxxxx这里换成你的cookiexxxxxxxxx这里换成你的cookiexxxxxxx',
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            response.encoding = 'utf-8'
            print(response.status_code)
            print('ERROR')
        soup = BeautifulSoup(response.text, 'lxml')
    except Exception:
        print('请求都不让，这企查查是想逆天吗？？？')
    try:
        com_all_info = soup.find_all(class_='m_srchList')[0].tbody
        com_all_info_array = com_all_info.select('tr')
        print('开始爬取数据，请勿打开excel')
        for i in range(0, len(com_all_info_array)):
            #            try:
            temp_g_name = com_all_info_array[i].select('td')[2].select('.ma_h1')[0].text  # 获取公司名
            temp_g_tag = com_all_info_array[i].select('td')[2].select('.search-tags')[0].text  # 获取公司标签
            temp_r_name = com_all_info_array[i].select('td')[2].select('p')[0].a.text  # 获取法人名
            temp_g_money = com_all_info_array[i].select('td')[2].select('p')[0].select('span')[0].text.strip(
                '注册资本：')  # 获取注册资本
            temp_g_date = com_all_info_array[i].select('td')[2].select('p')[0].select('span')[1].text.strip(
                '成立日期：')  # 获取公司注册时间
            temp_r_email = com_all_info_array[i].select('td')[2].select('p')[1].text.split('\n')[1].strip().strip(
                '邮箱：')  # 获取法人Email
            temp_r_phone = com_all_info_array[i].select('td')[2].select('p')[1].select('.m-l')[0].text.strip(
                '电话：')  # 获取法人手机号
            temp_g_addr = com_all_info_array[i].select('td')[2].select('p')[2].text.strip().strip('地址：')  # 获取公司地址
            temp_g_state = com_all_info_array[i].select('td')[3].select('.nstatus.text-success-lt.m-l-xs')[
                0].text.strip()  # 获取公司状态

            g_name_list.append(temp_g_name)
            g_tag_list.append(temp_g_tag)
            r_name_list.append(temp_r_name)
            g_money_list.append(temp_g_money)
            g_date_list.append(temp_g_date)
            r_email_list.append(temp_r_email)
            r_phone_list.append(temp_r_phone)
            g_addr_list.append(temp_g_addr)
            g_state_list.append(temp_g_state)

    #            except Exception:
    #                print('错误！')
    except Exception:
        print('好像被拒绝访问了呢...请稍后再试叭...')


if __name__ == '__main__':
    global g_name_list
    global g_tag_list
    global r_name_list
    global g_money_list
    global g_date_list
    global r_email_list
    global r_phone_list
    global g_addr_list
    global g_state_list

    g_name_list = []
    g_tag_list = []
    r_name_list = []
    g_money_list = []
    g_date_list = []
    r_email_list = []
    r_phone_list = []
    g_addr_list = []
    g_state_list = []

    key_word = input('请输入您想搜索的关键词：')
    num = int(input('请输入您想检索的次数：')) + 1
    sleep_time = int(input('请输入每次检索延时的秒数：'))

    key_word = urllib.parse.quote(key_word)

    print('正在搜索，请稍后')

    for x in range(1, num):
        url = r'https://www.qichacha.com/search_index?key={}&ajaxflag=1&p={}&'.format(key_word, x)
        s1 = craw(url, key_word, x)
        time.sleep(sleep_time)
    workbook = xlwt.Workbook()
    # 创建sheet对象，新建sheet
    sheet1 = workbook.add_sheet('企查查数据', cell_overwrite_ok=True)
    # ---设置excel样式---
    # 初始化样式
    style = xlwt.XFStyle()
    # 创建字体样式
    font = xlwt.Font()
    font.name = '仿宋'
    #    font.bold = True #加粗
    # 设置字体
    style.font = font
    # 使用样式写入数据
    print('正在存储数据，请勿打开excel')
    # 向sheet中写入数据
    name_list = ['公司名字', '公司标签', '法定法人', '注册资本', '成立日期', '法人邮箱', '法人电话', '公司地址', '公司状态']
    for cc in range(0, len(name_list)):
        sheet1.write(0, cc, name_list[cc], style)
    for i in range(0, len(g_name_list)):
        print(g_name_list[i])
        sheet1.write(i + 1, 0, g_name_list[i], style)  # 公司名字
        sheet1.write(i + 1, 1, g_tag_list[i], style)  # 公司标签
        sheet1.write(i + 1, 2, r_name_list[i], style)  # 法定法人
        sheet1.write(i + 1, 3, g_money_list[i], style)  # 注册资本
        sheet1.write(i + 1, 4, g_date_list[i], style)  # 成立日期
        sheet1.write(i + 1, 5, r_email_list[i], style)  # 法人邮箱
        sheet1.write(i + 1, 6, r_phone_list[i], style)  # 法人电话
        sheet1.write(i + 1, 7, g_addr_list[i], style)  # 公司地址
        sheet1.write(i + 1, 8, g_state_list[i], style)  # 公司状态
    # 保存excel文件，有同名的直接覆盖
    workbook.save(r"D:\wyy-qcc-" + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + ".xls")
    print('保存完毕~')
