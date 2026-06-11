#!/usr/bin/env python3
"""최종 카드 2장(스벅 그린 + 배민 핑크)을 11x16.5cm(2:3)로 그려 단일 PDF로 저장.
사용법: python make_final_pdf.py ["스벅번호"] ["배민코드"]
출력: 최종_카드.pdf  (2페이지, 각 11x16.5cm @ ~300dpi)
      + 미리보기 PNG 2장
"""
import sys, urllib.parse
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont

# 실제 코드 (기본값)
CODE_SBUX   = sys.argv[1].strip() if len(sys.argv) > 1 else "9007 6970 0755"
CODE_BAEMIN = sys.argv[2].strip() if len(sys.argv) > 2 else "K9PA ANGK WX"
BASE_SBUX   = "https://robin0214.github.io/qr-gift/starbucks/"
BASE_BAEMIN = "https://robin0214.github.io/qr-gift/"
OUTDIR = "/Users/robin.lee/app/"

# 11 x 16.5 cm @ 300dpi
W, H = 1300, 1950
DPI = 1300 / (11/2.54)   # ≈300.18 → 인쇄 100%시 정확히 11x16.5cm

PRE = "/Users/robin.lee/Library/Fonts/"
DOHYEON = "/Users/robin.lee/Library/Fonts/BMDOHYEON_otf.otf"
def pB(s):  return ImageFont.truetype(PRE+"Pretendard-Black.otf", s)
def pBd(s): return ImageFont.truetype(PRE+"Pretendard-Bold.otf", s)
def pM(s):  return ImageFont.truetype(PRE+"Pretendard-Medium.otf", s)
def pSb(s): return ImageFont.truetype(PRE+"Pretendard-SemiBold.otf", s)
def DH(s):  return ImageFont.truetype(DOHYEON, s)

GREEN="#00704A"; HOUSE="#1e3932"; GOLD="#c8a96a"

def qr_img(base, code, px):
    url = base + "#" + urllib.parse.quote(code)
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=2)
    qr.add_data(url); qr.make(fit=True)
    im = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    return im.resize((px, px), Image.NEAREST)

def center(d, y, text, font, fill):
    bb = d.textbbox((0,0), text, font=font); tw = bb[2]-bb[0]
    d.text(((W-tw)//2 - bb[0], y), text, font=font, fill=fill)

def spaced(d, y, text, font, fill, gap=16):
    widths=[d.textbbox((0,0),c,font=font)[2] for c in text]
    total=sum(widths)+gap*(len(text)-1); x=(W-total)//2
    for c,wd in zip(text,widths):
        d.text((x,y),c,font=font,fill=fill); x+=wd+gap

def qmark(d, cx, cy, r, color, lw=9):
    d.ellipse([cx-r,cy-r,cx+r,cy+r], outline=color, width=lw)
    fnt=pB(int(r*1.25)); bb=d.textbbox((0,0),"?",font=fnt)
    tw=bb[2]-bb[0]; th=bb[3]-bb[1]
    d.text((cx-tw//2-bb[0], cy-th//2-bb[1]), "?", font=fnt, fill=color)

# ---------- 스타벅스: 딥그린 (Pretendard) ----------
def card_sbux():
    img=Image.new("RGB",(W,H),HOUSE); d=ImageDraw.Draw(img)
    d.rounded_rectangle([38,38,W-38,H-38], radius=46, outline=GOLD, width=3)
    spaced(d,130,"A GIFT FOR YOU", pBd(36), GOLD, gap=16)
    qmark(d, W//2, 350, 86, "#e9e1cf")
    center(d,490,"누군가 당신에게", pM(42), "#cfe0d7")
    center(d,566,"선물을 보냈어요", pB(64), "#ffffff")
    d.rounded_rectangle([(W-740)//2,700,(W+740)//2,1400], radius=30, fill="#ffffff")
    img.paste(qr_img(BASE_SBUX, CODE_SBUX, 600), ((W-600)//2,740))
    center(d,1465,"스캔하면 정체가 공개돼요", pBd(46), GOLD)
    center(d,1543,"과연 무엇일까요?", pM(40), "#cfe0d7")
    center(d,1800,"From. 당신의 마니또", pSb(38), GOLD)
    return img

# ---------- 배민: 핑크 (도현체) ----------
def card_baemin():
    pink="#ff7a90"
    img=Image.new("RGB",(W,H),"#fff3f5"); d=ImageDraw.Draw(img)
    d.rounded_rectangle([44,44,W-44,H-44], radius=50, outline=pink, width=5)
    center(d,140,"To.  나의 마니또", DH(46), pink)
    center(d,250,"깜짝 선물!", DH(86), "#3a2630")
    center(d,400,"무엇이 들어있을까요?", DH(42), "#9b6b76")
    d.rounded_rectangle([(W-760)//2,520,(W+760)//2,1340], radius=38, fill="#ffffff", outline="#ffd6dd", width=4)
    img.paste(qr_img(BASE_BAEMIN, CODE_BAEMIN, 620), ((W-620)//2,580))
    center(d,1420,"여기를 스캔하면 공개!", DH(48), pink)
    center(d,1525,"카메라로 QR을 비춰보세요", DH(38), "#9b6b76")
    center(d,1770,"Happy 마니또", DH(46), pink)
    return img

sbux = card_sbux()
baemin = card_baemin()

# 미리보기 PNG
sbux.save(OUTDIR+"최종_스타벅스_11x16.5.png")
baemin.save(OUTDIR+"최종_배민_11x16.5.png")

# 단일 PDF (2페이지)
pdf = OUTDIR+"최종_카드.pdf"
sbux.save(pdf, "PDF", resolution=DPI, save_all=True, append_images=[baemin])

print(f"스벅 코드 : {CODE_SBUX}")
print(f"배민 코드 : {CODE_BAEMIN}")
print(f"캔버스    : {W}x{H}px  (≈11x16.5cm @ {DPI:.1f}dpi)")
print(f"PDF 저장  : {pdf}  (2페이지)")
