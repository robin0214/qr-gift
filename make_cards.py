#!/usr/bin/env python3
"""프린트용 '미스터리' 마니또 선물 카드 (A6, 300dpi).
배민/쿠폰 정체를 숨기고, 스캔하면 페이지에서 리빌됨.
사용법: python make_cards.py "쿠폰코드"
출력: card_1_mystery.png, card_2_ticket.png, card_3_pink.png
"""
import sys, urllib.parse
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont

CODE = sys.argv[1].strip() if len(sys.argv) > 1 else "TEST-1234-DEMO"
BASE = "https://robin0214.github.io/qr-gift/"
URL = BASE + "#" + urllib.parse.quote(CODE)
OUTDIR = "/Users/robin.lee/app/"
W, H = 1240, 1748
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"

def f(size, idx=0): return ImageFont.truetype(FONT, size, index=idx)

def qr_img(px):
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=2)
    qr.add_data(URL); qr.make(fit=True)
    im = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return im.resize((px, px), Image.NEAREST)

def center(d, y, text, font, fill, w=W):
    bb = d.textbbox((0,0), text, font=font); tw = bb[2]-bb[0]
    d.text(((w-tw)//2 - bb[0], y), text, font=font, fill=fill)

# ---------- 1) 미스터리 (남색/골드, 물음표) ----------
def card_mystery():
    img = Image.new("RGB",(W,H),"#1e2a44"); d=ImageDraw.Draw(img)
    gold="#e8c372"
    d.rounded_rectangle([34,34,W-34,H-34], radius=42, outline=gold, width=4)
    center(d,140,"?  ?  ?", f(70), gold)
    center(d,260,"누군가 당신에게", f(40), "#c7d0e0")
    center(d,330,"선물을 보냈어요", f(64), "#ffffff")
    # QR on white plate
    d.rounded_rectangle([(W-720)//2,470,(W+720)//2,1190], radius=30, fill="#ffffff")
    q=qr_img(620); img.paste(q,((W-620)//2,520))
    center(d,1260,"스캔하면 정체가 공개됩니다", f(44), gold)
    center(d,1345,"과연 무엇일까요?", f(38), "#c7d0e0")
    center(d,1560,"From. 당신의 마니또", f(40), gold)
    p=OUTDIR+"card_1_mystery.png"; img.save(p); return p

# ---------- 2) 미스터리 티켓 (크라프트) ----------
def card_ticket():
    bg="#ece0c8"; img=Image.new("RGB",(W,H),bg); d=ImageDraw.Draw(img); card="#fffdf7"
    d.rounded_rectangle([60,60,W-60,H-60], radius=36, fill=card, outline="#caa24a", width=4)
    cy=H//2
    for cx in (60, W-60): d.ellipse([cx-46,cy-46,cx+46,cy+46], fill=bg)
    x=130
    while x<W-130: d.line([x,cy,x+22,cy], fill="#caa24a", width=3); x+=44
    center(d,150,"MYSTERY  GIFT", f(46), "#caa24a")
    center(d,225,"열어보기 전엔", f(56), "#3a2e16")
    center(d,310,"아무도 몰라요", f(56), "#3a2e16")
    q=qr_img(560); img.paste(q,((W-560)//2,440))
    center(d,1080,"QR을 스캔해서", f(46), "#7a6533")
    center(d,1150,"선물을 확인하세요!", f(46), "#7a6533")
    center(d,1300,"스캔하면 바로 받을 수 있어요", f(34), "#a98b4a")
    center(d,1560,"For. 나의 마니또", f(40), "#caa24a")
    p=OUTDIR+"card_2_ticket.png"; img.save(p); return p

# ---------- 3) 핑크 깜짝 ----------
def card_pink():
    img=Image.new("RGB",(W,H),"#fff3f5"); d=ImageDraw.Draw(img); pink="#ff7a90"
    d.rounded_rectangle([40,40,W-40,H-40], radius=46, outline=pink, width=5)
    center(d,130,"To.  나의 마니또", f(44), pink)
    center(d,235,"깜짝 선물!", f(78), "#3a2630")
    center(d,360,"무엇이 들어있을까요?", f(40), "#9b6b76")
    d.rounded_rectangle([(W-720)//2,450,(W+720)//2,1170], radius=36, fill="#ffffff", outline="#ffd6dd", width=4)
    q=qr_img(600); img.paste(q,((W-600)//2,510))
    center(d,1230,"여기를 스캔하면 공개!", f(44), pink)
    center(d,1340,"카메라로 QR을 비춰보세요", f(36), "#9b6b76")
    center(d,1560,"Happy 마니또", f(40), pink)
    p=OUTDIR+"card_3_pink.png"; img.save(p); return p

paths=[card_mystery(), card_ticket(), card_pink()]
print("CODE:", CODE)
for p in paths: print("saved:", p)
