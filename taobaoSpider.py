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
import sys

itemKey = "洗发水"
outputDir = './test'
chromeDirverPath = r'D:\project\chromedriver/chromedriver.exe'
pagesNum = 3  # 总共爬取的页数
# 创建输出目录



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

    if not os.path.isdir(outputDir):
        os.mkdir(outputDir)


    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium 
    browser = webdriver.Chrome(chromeDirverPath, options=options)
    wait = WebDriverWait(browser, 10) # 最大等待时间

    # 让浏览器打开淘宝
    browser.get("https://www.taobao.com/")

    # 找到搜索框输入内容并搜索
    # browser.find_element_by_xpath('//*[@id="q"]').send_keys("便携果汁杯", keys.Keys.ENTER)
    browser.find_element("xpath",'//*[@id="q"]').send_keys(itemKey, keys.Keys.ENTER)

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
    
    for i in range(pagesNum):
        # 等待直到页面刷新出
        print("开始爬取：" + str(i+1) + '页')
        goodsTotal = wait.until(EC.presence_of_all_elements_located(( By.CSS_SELECTOR, '.m-itemlist .items > div')))
        print("页面成功出现!!!")
        # print(itemsTotal)
        # items = browser.find_elements( By.CSS_SELECTOR, '.m-itemlist .items > div')
        print(len(goodsTotal))
        for item in goodsTotal:
            
            # [neng] todo: 也许这里可以点击进入这个商品单独的页面，并爬取他相关的六张图片。
            
            # 获取这张图片的下载地址
            # img = item.find_element_by_css_selector(".pic-box .pic img").get_attribute("data-src")
            img = item.find_element( By.CSS_SELECTOR ,".pic-box .pic img").get_attribute("data-src")
            
            # 拼接完成的下载地址
            img_url = "http:" + img
            # print(img_url)
            # 通过requests下载这张图片
            sleep_time = random.random()*3 # [Neng] 通过request下载，是不是最好等待时间设长一些？如果太短则没有接受完就跳过了？
            time.sleep(sleep_time)
            # 文件夹需要手动创建好
            outputImgPath = os.path.join(outputDir,f'{n}.jpg')
            file = open( outputImgPath, "wb")
            
            #file = open( outputDir+f"\\{n}.jpg", "wb")
            try:
                file.write(requests.get(img_url).content)  
            except:
                print("无法下载该图片，跳过")
            print("下载图片" + str(n))
            n += 1

            # 精髓之处，大部分人被检测为机器人就是因为进一步模拟人工操作
            # 模拟人工向下浏览商品，即进行模拟下滑操作，防止被识别出是机器人
            swipe_down(browser, 0.5)  # 这里可以稍微快一点，把下面那个sleep删掉吧。

        # 翻页操作
        # browser.find_element_by_css_selector('.wraper:nth-last-child(1) .next > a').click()
        browser.find_element(By.CSS_SELECTOR, '.wraper:nth-last-child(1) .next > a').click()

        time.sleep(2)

    print('[' + itemKey + ']'+'前'+str(pagesNum)+'页商品图片下载完成,结果保存在：' + str(os.path.abspath(outputDir)))

    file.close()
    # 关闭浏览器
    browser.quit()


if __name__ == '__main__':
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv) )
    # global pagesNum, outputDir, itemKey
    if len(sys.argv) == 4:
        itemKey = sys.argv[1]
        pagesNum = int(sys.argv[2])
        outputDir = sys.argv[3]
    elif len(sys.argv) != 1:
        print('请输入完整指令，例如：')
        print('python taobaoSpider.py 洗发水 3 ./imgDir')
        sys.exit()

    else:
        print("没有输入参数，则使用默认参数")
        print("商品关键词：" + itemKey)
        print("页数：" + str(pagesNum))
        print('图片输出目录：' + str(outputDir))
    functions()