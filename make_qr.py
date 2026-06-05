#!/usr/bin/env python3
"""배민 쿠폰 QR 생성기.
사용법:
    /Users/robin.lee/app/.qrvenv/bin/python make_qr.py "실제-쿠폰코드"
결과:
    baemin_coupon_qr.png  (스캔 -> robin0214.github.io/qr-gift/ 복사버튼 화면)
"""
import sys, urllib.parse
import qrcode
from qrcode.constants import ERROR_CORRECT_H

BASE = "https://robin0214.github.io/qr-gift/"
OUT = "/Users/robin.lee/app/baemin_coupon_qr.png"

code = sys.argv[1].strip() if len(sys.argv) > 1 else "XXXX-XXXX-XXXX"
url = BASE + "#" + urllib.parse.quote(code)

qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=12, border=4)
qr.add_data(url)
qr.make(fit=True)
qr.make_image(fill_color="black", back_color="white").save(OUT)

print("쿠폰코드 :", code)
print("QR 주소  :", url)
print("저장됨   :", OUT)
