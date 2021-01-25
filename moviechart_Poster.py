import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import sys
import os
import math
import time
from datetime import datetime
import xlwt
import urllib
import urllib.request as ul
import requests
import json
import time

#한국영화 진흥원 api key
key = '7181efd7556aa2d121f744395312d5c5'

date = '20210120'
url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key={key}&targetDt={date}'

request = ul.Request(url)
response = ul.urlopen(request)
rescode = response.getcode()

if(rescode == 200):
    responseData = response.read()

result = json.loads(responseData)

names = []
for i in range(10):
    names.append(result['boxOfficeResult']['weeklyBoxOfficeList'][i]['movieNm'])

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

#폴더 만들기
today=time.strftime('%Y-%m-%d', time.localtime(time.time()))
createFolder(f'./movie_chart/{today}')

# 웹드라이버 실행
driver = webdriver.Chrome(os.getcwd() + "/chromedriver.exe")
url = 'https://movie.naver.com/'
driver.get(url)

# 전체 소스 가져오기
full_html = driver.page_source
soup = BeautifulSoup(full_html, 'html.parser')

for i in range(10):
    #포스터 가져오기
    search_box =  driver.find_element_by_id('ipt_tx_srch')
    search_box.send_keys(names[i])
    time.sleep(2)

    #검색어 클릭
    driver.find_element_by_xpath('//*[@class="auto_tx_area"]/div[1]/ul/li[1]/a').click()
    time.sleep(2)
    
    #포스터 클릭
    sample = driver.find_element_by_xpath('//*[@class="poster"]/a')
    driver.execute_script("arguments[0].click();", sample)
    
    #새 창으로 핸들 변경
    driver.window_handles
    driver.switch_to.window(driver.window_handles[1])
    
    #사진 저장하기
    src = driver.find_element_by_xpath('//*[@id="page_content"]/a/img').get_attribute('src')
    urllib.request.urlretrieve(src,f'./movie_chart/{i}.jpg')
    
    #탭 종료
    driver.close()
    
    #다시 원래대로 핸들 변경
    driver.window_handles
    driver.switch_to.window(driver.window_handles[0])

#탭 종료 및 드라이버 종료
driver.close()
driver.quit()