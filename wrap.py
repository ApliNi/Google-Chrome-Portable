import os
from datetime import datetime
import shutil

import requests
from requests_html import HTMLSession

if os.path.exists('chrome.exe'):
    os.remove('chrome.exe')
if os.path.exists('chrome.7z'):
    os.remove('chrome.7z')
if os.path.exists('Chrome-bin'):
    os.remove('Chrome-bin')

url = 'https://www.iplaysoft.com/tools/chrome/'

with HTMLSession() as session:
    r = session.get('https://www.iplaysoft.com/tools/chrome/')
    a = r.html.xpath('//*[@id="result_win"]/div[1]/div/div[2]/a[3]')
    href = a[0].attrs['href']

    r = requests.get(href, stream=True)
    with open('chrome.exe', 'wb') as f:
        for ch in r:
            f.write(ch)
        f.close()

os.system('7z.exe x chrome.exe')
os.system('7z.exe x chrome.7z')

if os.path.exists('chrome.exe'):
    os.remove('chrome.exe')
if os.path.exists('chrome.7z'):
    os.remove('chrome.7z')

# 获得Chorme-bin,version.dll,组装到一块就可以分发了
version = '0.0.0.0'
path = 'Chrome-bin'
for i in os.listdir(path):
    if os.path.isdir(os.path.join(path, i)):
        version = i
        break

print(version)

shutil.move(r'build\release\version.dll', 'Chrome-bin')

os.rename('Chrome-bin', 'Chrome')
shutil.move(r'Chrome', 'build/release/Chrome')

# 会自动封装为zip
env = os.getenv('GITHUB_ENV')
with open(env, 'a') as f:
    f.write(f'BUILD_NAME=Win64_{version}_{datetime.now().strftime("%Y-%m-%d")}')

# os.system(f'7z.exe a build/release/Win64_{version}_{datetime.now().strftime("%Y-%m-%d")}.7z Chrome')
