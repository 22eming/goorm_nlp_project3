import os
from urllib import request
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
import argparse
import datetime
from selenium.webdriver.common.keys import Keys

# 설정
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", help="검색 할 주제나 사람 입력", default="")
parser.add_argument("-c", "--channel", help="검색 할 채널 이름" , default="")
parser.add_argument("-t", "--time", help="스크롤 시간",type=int, default=20)
parser.add_argument("--save_path", help="결과 저장 위치", default="./")
args = parser.parse_args()

# URL, search 선언
if args.name != "":
    search = args.name
    url = f'https://www.youtube.com/results?search_query={search}'
else:
    search = args.channel
    url = f'https://www.youtube.com/user/{search}/videos'

# web driver 실행
driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url= url)
driver.implicitly_wait(10)

# 스크롤
body = driver.find_element_by_css_selector('body')

def doScrollDown(whileSeconds):
        start = datetime.datetime.now()
        end = start + datetime.timedelta(seconds=whileSeconds)
        while True:
            body.send_keys(Keys.PAGE_DOWN)
            if datetime.datetime.now() > end:
                break

doScrollDown(args.time)

# 고유 ID 추출
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
a_tag = soup.find_all('a', id='video-title')
id_list = []
id_title = []
for a in a_tag:
    id_list.append(a['href'][9:])
    id_title.append(a.text.strip())


# 이미지 추출 함수

def make_img_url(videoId):
    img_url = "https://img.youtube.com/vi/" + videoId + "/maxresdefault.jpg"
    status = requests.get(img_url)
    if status.status_code == 404:
        print('maxres img를 찾을 수 없어 hqdefault로 반환합니다.')
        img_url = "https://img.youtube.com/vi/" + videoId + "/hqdefault.jpg"
        return img_url
    else:
        return img_url


def save_imgfile(file_name, img_url):
    status = requests.get(img_url)
    if status.status_code == 404:
        print('해당 img를 찾을 수 없습니다 Error_code : 404')
        return
    else:
        with open(os.path.join(args.save_path, file_name), 'wb') as f:
            f.write(request.urlopen(img_url).read())
        return

# 이미지 저장
for idx, (video_title, videoId) in enumerate(zip(id_title, id_list)) :
    print(idx, f'{video_title}영상 저장 중 ...', end = ' ')
    img_url = make_img_url(videoId)
    file_name = search + '_' + str(idx) + ".png"
    save_imgfile(file_name, img_url)
    print('영상 저장 완료.')
print('모든 작업이 끝났습니다.')