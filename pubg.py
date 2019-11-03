from PIL import Image, ImageOps
import sys
import pyocr
import pyocr.builders
import re

def ocr(tool, img, lang):
    """"テキスト抽出を実行する"""
    res = tool.image_to_string(
        img,
        lang=lang,
        builder=pyocr.builders.TextBuilder()
    )
    return res

print('[pubg.py] 処理を開始')
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("[pubg.py] OCRが見つかりません")
    sys.exit(1)

tool = tools[0]

score = {
    'rank': [],
    'kill': []
    }

print('[pubg.py] OCRの読み込みが完了')

# 言語の設定
langs = tool.get_available_languages()

img = Image.open('media\\01.png')
print('[pubg.py] ファイル読み込み完了')

img_resize = img.resize((1920, 1080))
img_resize.save('media\\edit\\resize.png')
print('[pubg.py] ファイルリサイズ完了')

print('[pubg.py] トリミングを開始')
img_all = img_resize.crop((70, 293, 480, 357))
img_all.save('media\\edit\\all.png')

img_rank = img_resize.crop((230, 305, 278, 345))
img_rank.save('media\\edit\\rank.png')

img_kill = img_resize.crop((440, 300, 480, 345))
img_kill.save('media\\edit\\kill.png')
print('[pubg.py] トリミング完了')

print('[pubg.py] 前処理なし解析 全体')
str_all = [
    ocr(tool, img_all, langs[0]),
    ocr(tool, img_all, langs[1])
]
print(str_all)

print('[pubg.py] 前処理なし解析 個別')
str_rank = [
    ocr(tool, img_rank, langs[0]),
    ocr(tool, img_rank, langs[1])
]
str_kill = [
    ocr(tool, img_kill, langs[0]),
    ocr(tool, img_kill, langs[1])
]
print('(ランク)', str_rank)
print('(キル)', str_kill)

for item in str_all:
    for str in item.split('\n'):
        r = re.search(r'#[0-9]+', str)
        k = re.search(r'[0-9]+', str)
        if r is not None:
            score['rank'].append(r.group())
        if k is not None:
            score['kill'].append(k.group())

for str in str_rank:
    r = re.search(r'#[0-9]+', str)
    if r is not None:
        score['rank'].append(r.group())

for str in str_kill:
    k = re.search(r'[0-9]+', str)
    if k is not None:
        score['kill'].append(k.group())

print('[pubg.py] グレースケール 開始')
img_all_gray = img_all.convert('L')
img_all_gray.save('media\\edit\\all_gray.png')

img_rank_gray = img_rank.convert('L')
img_rank_gray.save('media\\edit\\rank_gray.png')

img_kill_gray = img_kill.convert('L')
img_kill_gray.save('media\\edit\\kill_gray.png')

print('[pubg.py] グレースケール 全体')
str_all = [
    ocr(tool, img_all_gray, langs[0]),
    ocr(tool, img_all_gray, langs[1])
]
print(str_all)

for item in str_all:
    for str in item.split('\n'):
        r = re.search(r'#[0-9]+', str)
        k = re.search(r'[0-9]+', str)
        if r is not None:
            score['rank'].append(r.group())
        if k is not None:
            score['kill'].append(k.group())

print('[pubg.py] グレースケール 個別')
str_rank = [ocr(tool, img_rank_gray, langs[0]),
            ocr(tool, img_rank_gray, langs[1])]
str_kill = [ocr(tool, img_kill_gray, langs[0]),
            ocr(tool, img_kill_gray, langs[1])]

print('(ランク)', str_rank)
print('(キル)', str_kill)

for str in str_rank:
    r = re.search(r'#[0-9]+', str)
    if r is not None:
        score['rank'].append(r.group())

for str in str_kill:
    k = re.search(r'[0-9]+', str)
    if k is not None:
        score['rank'].append(k.group())

# 2値化
img_all_twoPoint = img_all_gray.point(lambda x: 0 if x < 250 else x)
img_all_twoPoint.save('media\\edit\\all_twoPoint.png')

img_rank_twoPoint = img_rank_gray.point(lambda x: 0 if x < 250 else x)
img_rank_twoPoint.save('media\\edit\\rank_twoPoint.png')

img_kill_twoPoint = img_kill_gray.point(lambda x: 0 if x < 250 else x)
img_kill_twoPoint.save('media\\edit\\kill_twoPoint.png')

print('[pubg.py] 二値化 全体')
str_all = [
    ocr(tool, img_all_twoPoint, langs[0]),
    ocr(tool, img_all_twoPoint, langs[1])
]
print(str_all)

for item in str_all:
    for str in item.split('\n'):
        r = re.search(r'#[0-9]+', str)
        k = re.search(r'[0-9]+', str)
        if r is not None:
            score['rank'].append(r.group())
        if k is not None:
            score['kill'].append(k.group())

print('[pubg.py] 二値化 個別')
str_rank = [
    ocr(tool, img_rank_twoPoint, langs[0]),
    ocr(tool, img_rank_twoPoint, langs[1])
]
str_kill = [
    ocr(tool, img_kill_twoPoint, langs[0]),
    ocr(tool, img_kill_twoPoint, langs[1])
]

print('(ランク)', str_rank)
print('(キル)', str_kill)

for str in str_rank:
    r = re.search(r'#[0-9]+', str)
    if r is not None:
        score['rank'].append(r.group())

for str in str_kill:
    k = re.search(r'[0-9]+', str)
    if k is not None:
        score['rank'].append(k.group())

# 結果JSON
print(score)

pre = 0
for i in score['rank']:
    cnt = score['rank'].count(i)
    if pre < cnt:
        pre = cnt
        rank = i

pre = 0
for i in score['kill']:
    cnt = score['kill'].count(i)
    if pre < cnt:
        pre = cnt
        kill = i

score['rank'] = rank
score['kill'] = kill

print(score)