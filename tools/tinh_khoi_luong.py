#!/usr/bin/env python3
"""Tính khối lượng lệnh (lot) để nếu dính stop loss cứng thì chỉ mất đúng một số tiền cố định.

Quy tắc (xem knowledge/04-quan-ly-von.md):
  - SL cứng = điểm thấp nhất - 3 pip (BUY) / điểm cao nhất + 3 pip (SELL) với cặp tiền;
              vàng XAUUSD dùng 3 giá (3.00).
  - Lot = số tiền rủi ro / (khoảng cách từ điểm vào đến SL cứng x giá trị 1 đơn vị giá của 1 lot).
  - Làm tròn XUỐNG theo bước 0.01 lot để không vượt quá số tiền rủi ro.

Giả định hợp đồng chuẩn (kiểm tra lại với sàn của bạn):
  - Cặp tiền: 1 lot = 100.000 đơn vị đồng tiền cơ sở. 1 pip = 0.0001 (cặp có JPY: 0.01).
  - XAUUSD: 1 lot = 100 oz -> giá di chuyển 1.00 = 100 USD / lot.
Chưa tính spread, phí hoa hồng, trượt giá.

Ví dụ:
  python3 tools/tinh_khoi_luong.py --cap EURUSD --lenh BUY --vao 1.08520 --cuc-tri 1.08440 --rui-ro 50
  python3 tools/tinh_khoi_luong.py --cap XAUUSD --lenh SELL --vao 2650.50 --cuc-tri 2655.20 --rui-ro 50
  python3 tools/tinh_khoi_luong.py --cap EURJPY --lenh BUY --vao 162.40 --cuc-tri 162.15 --rui-ro 50 --ty-gia-quy-doi 0.0064
"""
import argparse
import math
import sys

HARD_SL_PIPS = 3          # cặp tiền
HARD_SL_GOLD = 3.0        # vàng: 3 giá


def spec(symbol):
    s = symbol.upper()
    if s in ("XAUUSD", "GOLD"):
        return {"contract": 100, "unit": 1.0, "unit_name": "giá", "buffer": HARD_SL_GOLD, "base": "XAU", "quote": "USD"}
    if len(s) != 6:
        sys.exit(f"Không nhận diện được cặp tiền: {symbol}")
    base, quote = s[:3], s[3:]
    pip = 0.01 if quote == "JPY" else 0.0001
    return {"contract": 100_000, "unit": pip, "unit_name": "pip", "buffer": HARD_SL_PIPS * pip, "base": base, "quote": quote}


def quote_to_usd(sp, price, rate):
    if sp["quote"] == "USD":
        return 1.0
    if sp["base"] == "USD":
        return 1.0 / price
    if rate is None:
        sys.exit(f"Cặp chéo {sp['base']}{sp['quote']}: cần --ty-gia-quy-doi (1 {sp['quote']} = ? USD).")
    return rate


def calc(symbol, side, entry, extreme, risk, rate=None, lot_step=0.01):
    sp = spec(symbol)
    side = side.upper()
    if side == "BUY":
        if extreme >= entry:
            sys.exit("Lệnh BUY: điểm thấp nhất phải nằm DƯỚI điểm vào.")
        hard_sl = extreme - sp["buffer"]
    elif side == "SELL":
        if extreme <= entry:
            sys.exit("Lệnh SELL: điểm cao nhất phải nằm TRÊN điểm vào.")
        hard_sl = extreme + sp["buffer"]
    else:
        sys.exit("--lenh phải là BUY hoặc SELL")
    dist = abs(entry - hard_sl)
    usd_per_lot = dist * sp["contract"] * quote_to_usd(sp, entry, rate)
    raw = risk / usd_per_lot
    lots = math.floor(raw / lot_step + 1e-9) * lot_step
    return {"sl_cung": hard_sl, "khoang_cach": dist, "don_vi": dist / sp["unit"], "ten_don_vi": sp["unit_name"],
            "lo_moi_lot": usd_per_lot, "lot_chinh_xac": raw, "lot": round(lots, 2), "lo_thuc_te": round(lots, 2) * usd_per_lot}


def main():
    ap = argparse.ArgumentParser(description="Tính lot theo số tiền rủi ro cố định.")
    ap.add_argument("--cap", required=True, help="VD: EURUSD, GBPUSD, USDJPY, XAUUSD")
    ap.add_argument("--lenh", required=True, help="BUY hoặc SELL")
    ap.add_argument("--vao", type=float, required=True, help="Giá vào lệnh (1/2 râu hoặc giá thanh khoản)")
    ap.add_argument("--cuc-tri", type=float, required=True, help="Điểm thấp nhất (BUY) / cao nhất (SELL)")
    ap.add_argument("--rui-ro", type=float, required=True, help="Số tiền chấp nhận mất mỗi lệnh (USD)")
    ap.add_argument("--ty-gia-quy-doi", type=float, default=None, help="Cặp chéo: 1 đồng tiền định giá = ? USD")
    a = ap.parse_args()
    r = calc(a.cap, a.lenh, a.vao, a.cuc_tri, a.rui_ro, a.ty_gia_quy_doi)
    print(f"Cặp: {a.cap.upper()}  Lệnh: {a.lenh.upper()}  Vào: {a.vao}  Cực trị: {a.cuc_tri}")
    print(f"SL cứng: {r['sl_cung']:.5f}  (cách điểm vào {r['don_vi']:.1f} {r['ten_don_vi']})")
    print(f"Lỗ nếu dính SL cứng với 1 lot: {r['lo_moi_lot']:.2f} USD")
    print(f"Khối lượng: {r['lot']:.2f} lot  (chính xác {r['lot_chinh_xac']:.4f})")
    print(f"Lỗ tối đa thực tế (chưa tính spread/phí/trượt giá): {r['lo_thuc_te']:.2f} USD / mục tiêu {a.rui_ro:.2f} USD")
    if r["lot"] <= 0:
        print("CẢNH BÁO: khối lượng nhỏ hơn 0.01 lot – khoảng dừng lỗ quá xa so với số tiền rủi ro.")


if __name__ == "__main__":
    main()
