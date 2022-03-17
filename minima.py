# -*- coding: utf-8 -*-
from contextlib import nullcontext
from dataclasses import dataclass
from pickle import TRUE
from unittest.util import _count_diff_all_purpose
from lxml import etree
from urllib3 import Timeout
import xlrd
import datetime
import xlwt
import time
import sys
import os
from xlutils.copy import copy
from selenium.webdriver import ActionChains
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

""" def save_excle(filename) :
    #1.创建book,sheet对象
    book=xlwt.Workbook('encodeing=utf-8')
    sheet=book.add_sheet('sheet1')
    #2.创建表头
    #sheet.write(行,列,值)
    sheet.write(行,列,值)
    #3.写入
    #sheet.write(行,列, 值)
    sheet.write(行,列,值)
    #4.保存
    book.save(filename) """

def login_minima() :
    #    book=xlwt.Workbook('encodeing=utf-8')
    now = datetime.datetime.now()
    date = '{}-{}-{}'.format(now.year, now.month, now.day)
    #filename = 'Name_of_your_file' + '_' + date
    #print("日期",filename)
    #打开需要操作的excel表
    
    wb=xlrd.open_workbook("../相关文件/minima记录.xls")    
    newbook=copy(wb)
    #sheet=newbook.add_sheet(date)
    #读取datasheet名  
    lens = len(wb.sheet_names())
    #print(lens)
    sheetname = wb.sheet_names()
    if (sheetname[lens-1] == date):
        sheet=newbook.get_sheet(date)
    else:
        #print("sheetname"+sheetname[lens-1]+"没有重复")
        sheet=newbook.add_sheet(date)
    #print(wb.sheet_names())   
    #newbook=xlwt.Workbook('encodeing=utf-8')
     
    #新增sheet,参数是该sheet的名字，可自定义
    
    sheet.write(0, 0, '账号')
    sheet.write(0, 1, 'DAILY_REWARDS')
    sheet.write(0, 2, 'INVITER_REWARDS')

    # myusername = "XXX"#登录账号
    # mypassword = "XXX"#登录密码
    #打开文件
    #name_list = open('d:\\user_pass.txt','r+')
    name_list = open('../相关文件/账号密码.txt','r+')
    #读取该文件行数count
    count=len(open(r"../相关文件/账号密码.txt",'r').readlines())
    print("该文件行数",count)

    # 打开记录用户名密码的文本，文本内格式为：户名:密码
    name_text = dict(line.strip().split(":") for line in name_list if line)
    #print(name_text)
# 将每行分别读取并作为字典
    u = list(name_text.keys())
    p = list(name_text.values())
    #print(u)
    #print(p)
    driver = webdriver.Chrome()  # 模拟浏览器打开网站C:\Users\67042\.wdm\drivers\chromedriver\win32\98.0.4758.102
    # driver = webdriver.Chrome('/path/to/chromedriver')           
    # driver = webdriver.Chrome("C:\Users\67042\.wdm\drivers\chromedriver\win32\98.0.4758.102\chromedriver.exe")
    # driver = webdriver.Chrome(ChromeDriverManager().install()) # 模拟浏览器打开网站   
    for count in range(count):
        print("---------------------------")
        username = u[count]
        password = p[count]
        print("该文件行数",count)
        print(username)
        #print(password)
        count=count+1        
        driver.get("https://incentivecash.minima.global/account/login")       
        #time.sleep(2)
        html = driver.page_source
        e_html = etree.HTML(html)
        try:    
            #确认是否在登录界面
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div/div/div/div[2]/form/div/div[3]/div[1]/button[1]')), '未找到Login按键')
        except:
            #建议刷新页面
            print("try报错未找到Login,刷新页面1")
            driver.refresh()
            time.sleep(10)
            try:  
                #尝试登出  
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/nav/div/a')), '未找到Logout').send_keys(Keys.ENTER)
                driver.get("https://incentivecash.minima.global/account/login")
                html = driver.page_source
                e_html = etree.HTML(html)
            except:
                #建议刷新页面
                print("try报错未找到Logout,刷新页面2")
                driver.refresh()
                time.sleep(10)
                
    # 找到登录框，输入账号密码
        #time.sleep(2)
        #程序每隔xx秒看一眼，如果条件成立了，则执行下一步，否则继续等待，直到超过设置的最长时间，然后抛出TimeoutException。
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')), '未找到email').send_keys(username)
        #driver.find_element_by_xpath("//*[@name='email']").send_keys(username)
        driver.find_element_by_xpath("//*[@name='password']").send_keys(password)
        driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div/div/div[2]/form/div/div[3]/div[1]/button[1]').send_keys(Keys.ENTER)
    # 判断上次是否退出
    # 模拟点击登录
        # print(e_html.xpath('//*[@id="app"]/div[1]/div/div/div/div[2]/form/h3/text()'))
        # if (e_html.xpath('//*[@id="app"]/div[1]/div/div/div/div[2]/form/h3/text()')==['Login']):#是否有Login
        #     driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div/div/div[2]/form/div/div[3]/div[1]/button[1]').send_keys(Keys.ENTER)
        #     print("Logout成功")
        # elif(e_html.xpath('//*[@id="app"]/div[1]/div[1]/nav/div/a/text()')==['Logout']):#是否有Logout
        #     driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/nav/div/a').send_keys(Keys.ENTER)
        #     print("Logout失败")
        # else:
        #     print("页面有问题")
    #登陆完毕后，更新页面源码 
        #登陆后数据可能还没刷新还是0，需要确认是否刷新 #
        # //*[@id="app"]/div/div[2]/div/div/div[1]/p[1]/span[2]   第一个copy
        #//*[@id="app"]/div/div[2]/div/div/div[1]/p[2]/span[2]    share 按键
        #WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[1]/p[1]/span[2]')), '未找到copy').click()
        try:    
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[1]/p[2]/span[2]')), '未找到share').click()
        except:
            #建议刷新页面
            print("try报错未找到share1")
            driver.refresh()
            time.sleep(10)
            try:    
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div/div/div[1]/p[2]/span[2]')), '未找到share').click()            
            except:
                #建议刷新页面
                print("try报错未找到share2")
                driver.refresh()
                time.sleep(10)
        html = driver.page_source
        #print(html)
        #time.sleep(3)
        e_html = etree.HTML(html)
        #print(e_html)
        #time.sleep(3)
        text1 = e_html.xpath('//*[@id="app"]/div/div/div/div/div[1]/div/text()')  #登录是否成功
        text2 = e_html.xpath('//*[@id="app"]/div/div/div/div/div[2]/form/div/div[1]/div/text()')  #登录是否成功
        #print(text2)
        #driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/nav/div/a').click()
        if (text1 == ['Login failed'] ):
            print("Login failed")
            sheet.write(count,0,username)
            sheet.write(count,1,"Login failed")
            sheet.write(count,2,"Login failed")    
                 
        elif (text2 == ['Email is invalid'] ):
            print("Email is invalid")
            sheet.write(count,0,username)
            sheet.write(count,1,"Email is invalid")
            sheet.write(count,2,"Email is invalid")
                       
        else :  
            #time.sleep(5)    
            DAILY_REWARDS = e_html.xpath('//*[@id="app"]/div/div[2]/div/div/div[1]/p[3]/text()')
            INVITER_REWARDS = e_html.xpath('//*[@id="app"]/div/div[2]/div/div/div[1]/p[5]/text()')
            #print(DAILY_REWARDS)
            #print(INVITER_REWARDS)
            sheet.write(count,0,username)
            sheet.write(count,1,DAILY_REWARDS)
            sheet.write(count,2,INVITER_REWARDS)
            #time.sleep(2)
            #程序每隔xx秒看一眼，如果条件成立了，则执行下一步，否则继续等待，直到超过设置的最长时间，然后抛出TimeoutException。
            #element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="su"]')))
            #driver.refresh()
            #time.sleep(2)
            #WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/nav/div/a')), '未找到Logout').send_keys(Keys.ENTER)
            try:    
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/nav/div/a')), '未找到Logout').send_keys(Keys.ENTER)
            except:
            #建议刷新页面
                print("try报错未找到Logout,刷新页面1")
                driver.refresh()
                time.sleep(10)
                try:    
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[1]/nav/div/a')), '未找到Logout').send_keys(Keys.ENTER)
                except:
                    #建议刷新页面
                    print("try报错未找到Logout,刷新页面2")
                    driver.refresh()
                    time.sleep(10)
            
            #driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/nav/div/a').send_keys(Keys.ENTER)
            #time.sleep(5)
    newbook.save("../相关文件/minima记录.xls")
    driver.quit # 退出驱动  
    
    
def main():
    login_minima()


if __name__ == '__main__':
	main()


