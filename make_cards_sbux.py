#!/usr/bin/env python3
"""프린트용 '미스터리' 스타벅스 마니또 선물 카드 (A6, 300dpi).
스벅 그린 테마 + Pretendard. 스캔하면 페이지에서 리빌됨.
사용법: python make_cards_sbux.py "쿠폰코드"
출력: card_sbux_1_green.png, card_sbux_2_cream.png, card_sbux_3_gold.png
"""
import sys, urllib.parse
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont

CODE = sys.argv[1].strip() if len(sys.argv) > 1 else "TEST-1234-DEMO"
BASE = "https://robin0214.github.io/qr-gift/starbucks/"
URL = BASE + "#" + urllib.parse.quote(CODE)
OUTDIR = "/Users/robin.lee/app/"
W, H = 1240, 1748

PRE = "/Users/robin.lee/Library/Fonts/"
def fb(size):  return ImageFont.truetype(PRE+"Pretendard-Black.otf", size)     # 굵게
def fbd(size): return ImageFont.truetype(PRE+"Pretendard-Bold.otf", size)
def fm(size):  return ImageFont.truetype(PRE+"Pretendard-Medium.otf", size)    # 본문
def fsb(size): return ImageFont.truetype(PRE+"Pretendard-SemiBold.otf", size)

GREEN="#00704A"; HOUSE="#1e3932"; CREAM="#f4efe4"; GOLD="#c8a96a"

def qr_img(px):
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=2)
    qr.add_data(URL); qr.make(fit=True)
    im = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return im.resize((px, px), Image.NEAREST)

def center(d, y, text, font, fill, w=W, spacing=0):
    bb = d.textbbox((0,0), text, font=font); tw = bb[2]-bb[0]
    d.text(((w-tw)//2 - bb[0], y), text, font=font, fill=fill)

def spaced(d, y, text, font, fill, gap=18, w=W):
    # 글자 사이 간격(트래킹) 넣어 라틴 라벨용
    widths=[d.textbbox((0,0),c,font=font)[2] for c in text]
    total=sum(widths)+gap*(len(text)-1)
    x=(w-total)//2
    for c,wd in zip(text,widths):
        d.text((x,y),c,font=font,fill=fill); x+=wd+gap

def cup(d, cx, cy, s, color, lw=8):
    # 간단한 테이크아웃 컵 라인아트
    top_w=int(150*s); bot_w=int(110*s); h=int(180*s)
    tl=(cx-top_w//2, cy-h//2); tr=(cx+top_w//2, cy-h//2)
    bl=(cx-bot_w//2, cy+h//2); br=(cx+bot_w//2, cy+h//2)
    d.line([tl,bl], fill=color, width=lw); d.line([tr,br], fill=color, width=lw)
    d.line([bl,br], fill=color, width=lw)
    # 뚜껑
    lidy=cy-h//2
    d.line([(cx-top_w//2-int(14*s),lidy),(cx+top_w//2+int(14*s),lidy)], fill=color, width=lw)
    d.rounded_rectangle([cx-top_w//2-int(14*s),lidy-int(34*s),cx+top_w//2+int(14*s),lidy],
                        radius=int(10*s), outline=color, width=lw)
    # 김(steam)
    for dx in (-int(28*s),0,int(28*s)):
        d.line([(cx+dx,lidy-int(60*s)),(cx+dx,lidy-int(110*s))], fill=color, width=max(4,lw-3))

# ---------- 1) 딥그린 프리미엄 ----------
def card_green():
    img=Image.new("RGB",(W,H),HOUSE); d=ImageDraw.Draw(img)
    d.rounded_rectangle([34,34,W-34,H-34], radius=42, outline=GOLD, width=3)
    spaced(d,118,"A GIFT FOR YOU", fbd(34), GOLD, gap=14)
    cup(d, W//2, 280, 1.05, "#e9e1cf")
    center(d,400,"누군가 당신에게", fm(40), "#cfe0d7")
    center(d,470,"선물을 보냈어요", fb(64), "#ffffff")
    d.rounded_rectangle([(W-700)//2,580,(W+700)//2,1280], radius=28, fill="#ffffff")
    q=qr_img(600); img.paste(q,((W-600)//2,630))
    center(d,1350,"스캔하면 정체가 공개돼요", fbd(46), GOLD)
    center(d,1430,"과연 무엇일까요?", fm(38), "#cfe0d7")
    center(d,1600,"From. 당신의 마니또", fsb(36), GOLD)
    p=OUTDIR+"card_sbux_1_green.png"; img.save(p); return p

# ---------- 2) 크림 미니멀 ----------
def card_cream():
    img=Image.new("RGB",(W,H),CREAM); d=ImageDraw.Draw(img)
    d.rounded_rectangle([40,40,W-40,H-40], radius=44, fill="#fffdf8", outline=GREEN, width=4)
    spaced(d,120,"STARBUCKS", fb(40), GREEN, gap=16)
    cup(d, W//2, 280, 0.95, GREEN)
    center(d,400,"열어보기 전엔", fb(56), HOUSE)
    center(d,484,"아무도 몰라요", fb(56), HOUSE)
    d.rounded_rectangle([(W-660)//2,600,(W+660)//2,1260], radius=24, fill="#ffffff", outline="#e7dcc3", width=3)
    q=qr_img(560); img.paste(q,((W-560)//2,650))
    center(d,1330,"QR을 스캔해서", fbd(46), GREEN)
    center(d,1400,"선물을 확인하세요!", fbd(46), GREEN)
    center(d,1520,"카메라로 비추기만 하면 끝", fm(34), "#8a7f66")
    center(d,1610,"For. 나의 마니또", fsb(36), GOLD)
    p=OUTDIR+"card_sbux_2_cream.png"; img.save(p); return p

# ---------- 3) 그린+골드 티켓 ----------
def card_gold():
    bg=HOUSE; img=Image.new("RGB",(W,H),bg); d=ImageDraw.Draw(img); card=CREAM
    d.rounded_rectangle([60,60,W-60,H-60], radius=36, fill=card, outline=GOLD, width=4)
    cy=H//2
    for cx in (60, W-60): d.ellipse([cx-46,cy-46,cx+46,cy+46], fill=bg)
    x=130
    while x<W-130: d.line([x,cy,x+22,cy], fill=GOLD, width=3); x+=44
    spaced(d,140,"MYSTERY GIFT", fbd(36), GREEN, gap=12)
    center(d,215,"무엇이 들어", fb(58), HOUSE)
    center(d,300,"있을까요?", fb(58), HOUSE)
    q=qr_img(540); img.paste(q,((W-540)//2,450))
    cup(d, W//2, 1130, 0.8, GREEN)
    center(d,1280,"스캔하면 바로 받을 수 있어요", fbd(42), GREEN)
    center(d,1360,"카메라로 QR을 비춰보세요", fm(34), "#8a7f66")
    center(d,1580,"For. 나의 마니또", fsb(38), GOLD)
    p=OUTDIR+"card_sbux_3_gold.png"; img.save(p); return p

paths=[card_green(), card_cream(), card_gold()]
print("CODE:", CODE)
for p in paths: print("saved:", p)
