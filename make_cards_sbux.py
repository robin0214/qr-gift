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
def fb(size):  return ImageFont.truetype(PRE+"Pretendard-Black.otf", size)
def fbd(size): return ImageFont.truetype(PRE+"Pretendard-Bold.otf", size)
def fm(size):  return ImageFont.truetype(PRE+"Pretendard-Medium.otf", size)
def fsb(size): return ImageFont.truetype(PRE+"Pretendard-SemiBold.otf", size)

GREEN="#00704A"; HOUSE="#1e3932"; CREAM="#f4efe4"; GOLD="#c8a96a"

def qr_img(px):
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=2)
    qr.add_data(URL); qr.make(fit=True)
    im = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return im.resize((px, px), Image.NEAREST)

def center(d, y, text, font, fill, w=W):
    bb = d.textbbox((0,0), text, font=font); tw = bb[2]-bb[0]
    d.text(((w-tw)//2 - bb[0], y), text, font=font, fill=fill)

def spaced(d, y, text, font, fill, gap=16, w=W):
    widths=[d.textbbox((0,0),c,font=font)[2] for c in text]
    total=sum(widths)+gap*(len(text)-1)
    x=(w-total)//2
    for c,wd in zip(text,widths):
        d.text((x,y),c,font=font,fill=fill); x+=wd+gap

def cup(d, cx, cy, s, color, lw=8):
    """간단한 테이크아웃 컵 라인아트 (김 짧게)."""
    top_w=int(150*s); bot_w=int(110*s); h=int(180*s)
    body_top=cy-h//2
    tl=(cx-top_w//2, body_top); tr=(cx+top_w//2, body_top)
    bl=(cx-bot_w//2, cy+h//2);  br=(cx+bot_w//2, cy+h//2)
    d.line([tl,bl], fill=color, width=lw); d.line([tr,br], fill=color, width=lw)
    d.line([bl,br], fill=color, width=lw); d.line([tl,tr], fill=color, width=lw)
    # 뚜껑
    lid_top=body_top-int(34*s)
    d.rounded_rectangle([cx-top_w//2-int(14*s),lid_top,cx+top_w//2+int(14*s),body_top],
                        radius=int(9*s), outline=color, width=lw)
    # 김(짧게)
    sy1=lid_top-int(10*s); sy0=sy1-int(46*s)
    for dx in (-int(26*s),0,int(26*s)):
        d.line([(cx+dx,sy1),(cx+dx,sy0)], fill=color, width=max(4,lw-3))

def qmark(d, cx, cy, r, color, lw=8):
    """미스터리용 물음표 배지 (정체 노출 X)."""
    d.ellipse([cx-r,cy-r,cx+r,cy+r], outline=color, width=lw)
    fnt=fb(int(r*1.25))
    bb=d.textbbox((0,0),"?",font=fnt)
    tw=bb[2]-bb[0]; th=bb[3]-bb[1]
    d.text((cx-tw//2-bb[0], cy-th//2-bb[1]), "?", font=fnt, fill=color)

# ---------- 1) 딥그린 프리미엄 ----------
def card_green():
    img=Image.new("RGB",(W,H),HOUSE); d=ImageDraw.Draw(img)
    d.rounded_rectangle([34,34,W-34,H-34], radius=42, outline=GOLD, width=3)
    spaced(d,108,"A GIFT FOR YOU", fbd(34), GOLD, gap=14)
    qmark(d, W//2, 300, 78, "#e9e1cf")
    center(d,420,"누군가 당신에게", fm(40), "#cfe0d7")
    center(d,490,"선물을 보냈어요", fb(60), "#ffffff")
    d.rounded_rectangle([(W-700)//2,615,(W+700)//2,1235], radius=28, fill="#ffffff")
    q=qr_img(560); img.paste(q,((W-560)//2,645))
    center(d,1290,"스캔하면 정체가 공개돼요", fbd(44), GOLD)
    center(d,1362,"과연 무엇일까요?", fm(38), "#cfe0d7")
    center(d,1600,"From. 당신의 마니또", fsb(36), GOLD)
    p=OUTDIR+"card_sbux_1_green.png"; img.save(p); return p

# ---------- 2) 크림 미니멀 ----------
def card_cream():
    img=Image.new("RGB",(W,H),CREAM); d=ImageDraw.Draw(img)
    d.rounded_rectangle([40,40,W-40,H-40], radius=44, fill="#fffdf8", outline=GREEN, width=4)
    spaced(d,108,"MYSTERY GIFT", fbd(38), GREEN, gap=14)
    qmark(d, W//2, 322, 84, GREEN)
    center(d,440,"열어보기 전엔", fb(54), HOUSE)
    center(d,520,"아무도 몰라요", fb(54), HOUSE)
    d.rounded_rectangle([(W-660)//2,640,(W+660)//2,1230], radius=24, fill="#ffffff", outline="#e7dcc3", width=3)
    q=qr_img(540); img.paste(q,((W-540)//2,665))
    center(d,1300,"QR을 스캔해서", fbd(46), GREEN)
    center(d,1372,"선물을 확인하세요!", fbd(46), GREEN)
    center(d,1500,"카메라로 비추기만 하면 끝", fm(34), "#8a7f66")
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
    spaced(d,138,"MYSTERY GIFT", fbd(36), GREEN, gap=12)
    center(d,210,"무엇이 들어", fb(58), HOUSE)
    center(d,292,"있을까요?", fb(58), HOUSE)
    q=qr_img(520); img.paste(q,((W-520)//2,440))
    qmark(d, W//2, 1165, 74, GREEN)
    center(d,1320,"스캔하면 바로 받을 수 있어요", fbd(42), GREEN)
    center(d,1392,"카메라로 QR을 비춰보세요", fm(34), "#8a7f66")
    center(d,1580,"For. 나의 마니또", fsb(38), GOLD)
    p=OUTDIR+"card_sbux_3_gold.png"; img.save(p); return p

paths=[card_green(), card_cream(), card_gold()]
print("CODE:", CODE)
for p in paths: print("saved:", p)
