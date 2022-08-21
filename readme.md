## [淘宝商品图片爬虫][tmall_crawler]
### 使用教程
1. 下载chrome浏览器 （https://www.google.com/chrome/?brand=YTUH&gclid=Cj0KCQjwr4eYBhDrARIsANPywCg6cnnR7qZhs6K63AmNnZTmzs65DVXD1_vU2_R3HZ9iO54XkJAgExEaApokEALw_wcB&gclsrc=aw.ds）
2. 查看chrome浏览器的版本号，下载对应版本号的chromedriver驱动（https://chromedriver.chromium.org/）
3. pip安装下列包
    - [x] pip install selenium


```python
#改成你的chromedriver的完整路径地址
chromeDirverPath = r'D:\project\chromedriver/chromedriver.exe'
#改成想要爬的商品关键词
itemKeys = "洗发水"
#输出图片目录
outputDir = './test'
```

### 运行脚本
``` Bash
python taobaoSpider.py 
```
需要手机淘宝扫码登录网页淘宝。

爬取的图片会保存在上面```outputDir```目录中。


### 参考
https://github.com/shengqiangzhang/examples-of-web-crawlers

selenium安装参考：
https://selenium-python-zh.readthedocs.io/en/latest/






## [TODO]

1. 从淘宝爬商品图片
    1. todo：点入商品页面的6张图片是否也要爬？
    2. 不知道为何，有时候会爬不到，是wait sleep的问题么？

2. 通过ocr将图片中的词识别
    1. todo：清理识别错误的词
    3. todo：寻找更可靠的ocr

3. 清理数据
    1. 使用nlp模型？
    2. 使用别的常规手段清理？

4. 跑数据分析
    1. tdlda？ 那俩？