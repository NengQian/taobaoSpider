# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common import keys
import time
import requests
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os.path 


itemKeys = "洗发水"
outputDir = './test'
chromeDirverPath = r'D:\project\chromedriver/chromedriver.exe'
# 创建输出目录
if not os.path.isdir(outputDir):
    os.mkdir(outputDir)



# 模拟向下滑动浏览
def swipe_down(browser,second):
    for i in range(int(second/0.1)):
        js = "var q=document.documentElement.scrollTop=" + str(300+200*i)
        browser.execute_script(js)
        time.sleep(0.1)
    js = "var q=document.documentElement.scrollTop=100000"
    browser.execute_script(js)
    time.sleep(0.2)


# 创建浏览器
def functions():

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium 
    browser = webdriver.Chrome(chromeDirverPath, options=options)
    wait = WebDriverWait(browser, 10) # 最大等待时间

    # 让浏览器打开淘宝
    browser.get("https://www.taobao.com/")

    # 找到搜索框输入内容并搜索
    # browser.find_element_by_xpath('//*[@id="q"]').send_keys("便携果汁杯", keys.Keys.ENTER)
    browser.find_element("xpath",'//*[@id="q"]').send_keys(itemKeys, keys.Keys.ENTER)

    time.sleep(1)
    # 切换成二维码登录
    # browser.find_element_by_xpath('//*[@id="login"]/div[1]/i').click()
    

    browser.find_element("xpath",'//*[@id="login"]/div[1]/i').click()

    # 判断当前页面是否为登录页面
    while browser.current_url.startswith("https://login.taobao.com/"):
        print("等待用户输入")
        time.sleep(1)
        # maybe use  WebDriverWait 
    print("登录成功!!!")
    n = 1
    count = 1
    
    # 等待直到页面刷新出
    itemsTotal = wait.until(EC.presence_of_element_located(( By.CSS_SELECTOR, '.m-itemlist .items > div')))
    print("页面成功出现!!!")
    print(itemsTotal)
    while True:
        #items = browser.find_elements_by_css_selector('.m-itemlist .items > div')
        items = browser.find_elements( By.CSS_SELECTOR, '.m-itemlist .items > div')
        print(len(items))
        for item in items:
            # 获取这张图片的下载地址
            # img = item.find_element_by_css_selector(".pic-box .pic img").get_attribute("data-src")
            img = item.find_element( By.CSS_SELECTOR ,".pic-box .pic img").get_attribute("data-src")
            
            # 拼接完成的下载地址
            img_url = "http:" + img
            # print(img_url)
            # 通过requests下载这张图片
            sleep_time = random.random()*10
            time.sleep(sleep_time)
            # 文件夹需要手动创建好
            file = open(f"./test\\{n}.jpg", "wb")
            try:
                file.write(requests.get(img_url).content)  
            except:
                print("无法下载该图片，跳过")
            print("下载图片" + str(n))
            n += 1

            # 精髓之处，大部分人被检测为机器人就是因为进一步模拟人工操作
            # 模拟人工向下浏览商品，即进行模拟下滑操作，防止被识别出是机器人
            swipe_down(browser, 0.5)  # 这里可以稍微快一点，把下面那个sleep删掉吧。
            # time.sleep(1)

        # 翻页操作
        # browser.find_element_by_css_selector('.wraper:nth-last-child(1) .next > a').click()
        browser.find_element(By.CSS_SELECTOR, '.wraper:nth-last-child(1) .next > a').click()

        time.sleep(2)
        count += 1
        # 爬取 4 页内容
        if count == 6:
            file.close()
            break

    # 关闭浏览器
    browser.quit()


if __name__ == '__main__':
    functions()