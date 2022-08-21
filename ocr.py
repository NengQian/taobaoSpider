# -*- coding: utf-8 -*-
# do ocr here
from email.mime import image
from taobaoSpider import outputDir
import os
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
imageDir = outputDir

if not os.path.isdir(imageDir):
    print(imageDir+" 路径不存在，请指定正确的图片目录路径")

files = [f for f in listdir(imageDir) if isfile(join(imageDir, f))]



