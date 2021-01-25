#워드 클라우드
from konlpy.tag import Okt
from collections import Counter
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
import cv2

#크롤링
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import sys
import os
import math
import time
from datetime import datetime
import xlwt
import urllib.request

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

# =========================== 크롤링 ===========================
# 입력 받기
input_title = input('1. 크롤링할 영화 제목을 입력하세요: ')

'''
input_path = input('3. 파일을 저장할 폴더명만 쓰세요: ')

if(input_path == '0'):
    input_path = os.getcwd()
else:
    createFolder(f'./code/ReviewCrowling&WordCloud/data/{input_path}')
'''

# 웹드라이버 실행
#print(os.getcwd())
driver = webdriver.Chrome(os.getcwd() + "/chromedriver.exe")
url = 'https://movie.naver.com'
driver.get(url)

# 검색어 입력
search_box =  driver.find_element_by_id('ipt_tx_srch')
search_box.send_keys(input_title)
time.sleep(2)

#검색어 클릭
driver.find_element_by_xpath('//*[@class="auto_tx_area"]/div[1]/ul/li[1]/a').click()
time.sleep(2)

# 전체 소스 가져오기
full_html = driver.page_source
soup = BeautifulSoup(full_html, 'html.parser')

#장르, 개봉일, 출연, 감독, 줄거리 가져오기
genre=driver.find_element_by_xpath('//*[@class="info_spec"]/dd[1]/p/span[3]').text #장르

year=driver.find_element_by_xpath('//*[@class="info_spec"]/dd[1]/p/span[4]/a[1]').text 
month=driver.find_element_by_xpath('//*[@class="info_spec"]/dd[1]/p/span[4]/a[2]').text
date=(year + month) #개봉일

director=driver.find_element_by_xpath('//*[@class="info_spec"]/dd[2]/p/a').text #감독

#dd태그 찾아서 저장
list1_p=soup.find('dt',class_='step3').find_next_sibling('dd').find('p')
#dd태그 속에서 a태그 리스트 저장
list2_p=list1_p.find_all('a')
perfomer=[] #출연진
for i in list2_p:
    #가져온 a태그 리스트에서 text만 perfomer에 저장
    perfomer.append(i.get_text())

try:
    summary_title=driver.find_element_by_xpath('//*[@class="h_tx_story"]').text #줄거리 제목
except:
    pass
summary=driver.find_element_by_xpath('//*[@class="con_tx"]').text #줄거리

'''
print(genre)
print(date)
print(director)
print(perfomer)
print(summary_title)
print(summary)
'''

# 평점가져오기
list_score=soup.find('div',class_='score score_left').find('div',class_='star_score').find_all('em')
score=""
for i in list_score:
    score+=(i.get_text())
#print(score)

#포스터 클릭
sample = driver.find_element_by_xpath('//*[@class="poster"]/a')
driver.execute_script("arguments[0].click();", sample)
    
#새 창으로 핸들 변경
driver.window_handles
driver.switch_to.window(driver.window_handles[1])
    
#사진 저장하기
src = driver.find_element_by_xpath('//*[@id="page_content"]/a/img').get_attribute('src')
urllib.request.urlretrieve(src,'./data/image.jpg')
    
#탭 종료
driver.close()
    
#다시 원래대로 핸들 변경
driver.window_handles
driver.switch_to.window(driver.window_handles[0])

# 평점 클릭
driver.find_element_by_xpath('//*[@id="movieEndTabMenu"]/li[5]/a').click()
time.sleep(2)

# 칼럼 리스트 준비
score = []
text = []
user = []
date = []
good = []
bad = []

# iframe 이동
driver.switch_to_default_content()
driver.switch_to_frame('pointAfterListIframe')

# 전체 소스 가져오기
full_html = driver.page_source
soup = BeautifulSoup(full_html, 'html.parser')

# 전체 글 수를 가져와서 입력받은 건수와 비교
total_comment = soup.find('div', class_='score_total').find('strong',class_='total').em.string
total_comment = int(total_comment.replace(",",""))
input_num = total_comment

# 크롤링한 글 수 카운트
count = 0

while(True):

    # 리뷰 리스트 가져오기
    content_list =  soup.find('div',class_='ifr_area basic_ifr').find('div', class_ = 'score_result').find('ul').find_all('li')

    for li in content_list:

        count += 1

        # 각 요소 가져오기
        tmp_score = li.find('div', class_='star_score').find('em').text
        tmp_text = li.find('div', class_='score_reple').find('p').text
        tmp_user = li.find('div', class_='score_reple').find('dl').find('span').text
        tmp_date = li.find('div', class_='score_reple').find_all('em')[1].text
        tmp_good = li.find('div', class_='btn_area').find_all('strong')[0].text
        tmp_bad = li.find('div', class_='btn_area').find_all('strong')[1].text

        # 칼럼 리스트에 추가
        score.append(tmp_score)
        text.append(tmp_text)
        user.append(tmp_user)
        date.append(tmp_date)
        good.append(tmp_good)
        bad.append(tmp_bad)

        

        # 만약 현재 글 수가 입력건수에 도달하면 루프 종료
        if(count == 100):#input_num
            break
    
    if(count == 100):#input_num
        break
    
    # 아직 입력건수에 도달하지 않았다면 다음 페이지를 열고 루프 계속
    else:
        driver.find_element_by_class_name('pg_next').click()
        time.sleep(1)
                
        driver.switch_to_default_content()
        driver.switch_to_frame('pointAfterListIframe')

        full_html = driver.page_source
        soup = BeautifulSoup(full_html, 'html.parser')

'''
        # 확인용 프린트
        print("총 %s 건 중 %s 번째 리뷰 데이터를 수집합니다===================================="%(input_num, count))
        print('1) 별점:', tmp_score)
        print('2) 리뷰내용:', tmp_text)
        print('3) 작성자:', tmp_user)
        print('4) 작성일자:', tmp_date)
        print('5) 공감:', tmp_good)
        print('6) 비공감:',tmp_bad)
        print('\n')
'''

# 데이터프레임 생성, 각 칼럼 리스트 넣기   
df = pd.DataFrame()
df['별점'] = score
df['리뷰내용'] = text
df['작성자'] = user
df['작성일자'] = date
df['공감'] = good
df['비공감'] = bad

for i in range(len(df)):
    df['리뷰내용'][i] = df['리뷰내용'][i].replace("\t","")
    df['리뷰내용'][i] = df['리뷰내용'][i].replace("\n","")

# ===========================워드클라우드 ===========================
data=df
dic = {}
okt=Okt()

for string in data['리뷰내용']:
    string=string.replace("\t","")
    string=string.replace("\n","")
    words = okt.nouns(string) 
    for word in words:
        try: dic[word] += 1
        except: dic[word] = 1

icon=cv2.imread("./data/image.jpg")#이미지 불러오기
icon_gray=cv2.imread("./data/image.jpg",cv2.IMREAD_GRAYSCALE)

ret, dst = cv2.threshold(icon_gray, 0, 255, cv2.THRESH_OTSU)
#THRESH_OTSU
#cv2.THRESH_BINARY_INV
plt.imshow(dst,cmap='gray')
plt.xticks([])
plt.yticks([])
plt.show()

wc = WordCloud(font_path= r'C:\Users\yangb\AppData\Local\Microsoft\Windows\Fonts\NanumGothic.ttf', background_color='black',
              width=dst.shape[0],height=dst.shape[1],max_words=300,max_font_size=250, mask=dst)

#C:\Users\yangb\AppData\Local\Microsoft\Windows\Fonts\NanumGothic.ttf

wc.generate_from_frequencies(dic)
plt.figure(figsize=(50,50)) #이미지 사이즈 지정
plt.imshow(wc) #이미지의 부드럽기 정도
plt.axis('off') #x y 축 숫자 제거
plt.show() 
plt.savefig(f"./data/image_wordcloud.png")#저장 형식

img2 = wc.to_array()
a = 0.3
b = 1.0 - a
result = cv2.addWeighted(img2, a,icon, b, 0)
cv2.imshow('dst',result)
cv2.waitKey(0)

cv2.destroyAllWindows()
