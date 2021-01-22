from konlpy.tag import Okt
from collections import Counter
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

#워드 클라우드를 생성할 데이터 자료
data=pd.read_csv("./아바타/아바타 (Avatar)_2021-01-20_215905.csv")
dic = {}
okt=Okt()

for string in data['리뷰내용']:
    string=string.replace("\t","")
    string=string.replace("\n","")
    words = okt.nouns(string) 
    for word in words:
        try: dic[word] += 1
        except: dic[word] = 1

#워드 클라우드 모양을 결정할 이미지 불러오기
icon=Image.open("video.png")

#RGB type로 icon과 같은 사이즈로 전부 (255,255,255)값으로 만들기
#(255,255,255)는 이미지가 채워지지 않는 부분을 의미
mask=Image.new("RGB", icon.size, (255,255,255))

#mask에 icon의 형상을 붙여넣고 nparray로 만들기
mask.paste(icon,icon)
mask=np.array(mask)

#font_path는 각자의 path 입력
wc = WordCloud(font_path= r'C:\Users\yangb\AppData\Local\Microsoft\Windows\Fonts\NanumGothic.ttf', background_color='white',
              width=1000,height=1000,max_words=300,max_font_size=250, mask=mask, stopwords=stopwords)

#C:\Users\yangb\AppData\Local\Microsoft\Windows\Fonts\NanumGothic.ttf (malangcongdduck)

wc.generate_from_frequencies(dic)
plt.figure(figsize=(50,50)) #이미지 사이즈 지정
plt.imshow(wc) #이미지의 부드럽기 정도
plt.axis('off') #x y 축 숫자 제거
plt.show() 
plt.savefig('아바타.png')#저장 형식과 저장할 파일의 이름