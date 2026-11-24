#!/usr/bin/env python3
"""Khai thác PHA ĐẨY với THỨ TỰ ƯU TIÊN VÙNG VÀO LỆNH (người dùng chốt 24/11/2026).

Chỉ dùng một khung (M1/M1 hoặc M15/M15). Ví dụ xu hướng tăng (SELL chạy trên dữ liệu đảo dấu):
  * Sóng = từ mốc cấu trúc B (đáy của pha hồi đủ gần nhất) đến đỉnh T; 50% = (B+T)/2; discount = dưới 50%.
  * Các vùng trong discount (tạo ra trong sóng, chưa bị dùng):
      - THANH KHOẢN: đáy nông của pha hồi không đủ (bộ máy ghi trong Result.liq), chưa bị quét.
      - POI: nến có râu dài hơn thân, nến sau đóng cửa trong high–low; nằm trọn trong discount; có FVG hỗ trợ.
      - FVG: FVG tăng nằm trọn trong discount, chưa bị chạm.
  * Ưu tiên:
      1. Thanh khoản nằm ngay TRÊN POI → vào lệnh khi nến QUÉT thanh khoản và râu chạm vào POI.
      2. POI nằm TRÊN thanh khoản → bỏ POI, vào lệnh khi nến quét thanh khoản.
      3. FVG → khai thác độc lập, giống POI.
      4. Không có vùng nào → khai thác bình thường khi giá chạm 50%.
  * Vào lệnh:
      - Kiểu QUÉT: nến có râu xuống dưới mức thanh khoản, đóng cửa TRÊN mức đó, râu dưới dài hơn thân.
        Lệnh chờ tại 1/2 râu nếu mức đó dưới thanh khoản, ngược lại tại chính giá thanh khoản.
        Thân nến đóng cửa DƯỚI thanh khoản → thanh khoản đó hết; nếu là cặp thanh khoản+POI thì chuyển sang chờ POI;
        nếu thanh khoản đứng một mình (đã ở discount) → khai thác bình thường (chờ tạo đáy).
      - Kiểu POI/FVG/bình thường: chạm vùng → chờ nến xác nhận đáy (cách 1) → lệnh chờ tại 1/2 râu dưới của nến
        có điểm thấp nhất. POI/FVG: nến chạm lần đầu đóng cửa dưới đáy vùng → vùng hết hiệu lực.
      - Huỷ lệnh chờ: giá chạm đỉnh T trước khi khớp; nến đóng cửa dưới điểm thấp nhất; khớp trong giờ cấm.
        (KHÔNG huỷ khi giá tạo đỉnh cách 1 trước khi khớp – đã bỏ 24/11.)
  * Pha hồi từ đỉnh đã tạo đáy (cách 1) mà chưa chạm 50% (đáy nông = thanh khoản, trường hợp B4/C2) → sóng đó
    KHÔNG BUY, phải đợi thân nến phá đỉnh (sóng mới) – người dùng xác nhận 24/11.
  * Mỗi vùng dùng một lần. Lệnh ở vùng trên bị DỪNG LỖ → được vào tiếp ở vùng dưới; lệnh hòa vốn / chốt lời → hết sóng.
  * Quản lý lệnh giống trước (SL theo đóng cửa + SL cứng, TP1 tại T, dời SL về điểm vào, TP2 khi tạo đỉnh mới).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import smc_engine as eng  # noqa: E402
import backtest as bt  # noqa: E402


def analyze_daily_full(bars, inverted=False):
    n = len(bars); ctx = [("UNKNOWN", None, None, None)] * n; liq = []
    starts = bt.day_starts(bars) + [n]
    for a, b in zip(starts, starts[1:]):
        s = max(0, a - 1)
        r = eng.analyze(bars[s:b], start_rule="prev_close", inverted=inverted)
        cache = {}

        def sh(sw):
            if sw is None:
                return None
            if id(sw) not in cache:
                cache[id(sw)] = eng.Swing(sw.kind, sw.i + s, sw.price, sw.conf + s, sw.how)
            return cache[id(sw)]
        for k, c in enumerate(r.ctx):
            if s + k >= a:
                mode, T, B, scan = c
                ctx[s + k] = (mode, sh(T), sh(B), None if scan is None else scan + s)
        liq += [sh(w) for w in r.liq]
    return ctx, liq


class Zone:
    def __init__(self, kind, top, bot, liq=None, poi=None, t=""):
        self.kind, self.top, self.bot, self.liq, self.poi, self.t = kind, top, bot, liq, poi, t
        self.used = False
        self.poi_hi = top if kind in ("poi", "fvg") else None
        self.poi_lo = bot if kind in ("poi", "fvg") else None


def build_zones(B, T, mid, bars, k, liqs):
    L = lambda i: bars[i].l
    H = lambda i: bars[i].h
    lq = []
    for w in liqs:
        if w.kind == "B" and B.i < w.i < T.i and w.conf <= k and w.price <= mid and w.price > B.price:
            if not any(L(q) < w.price for q in range(w.i + 1, k + 1)):
                lq.append(w.price)
    pois = []
    for i in range(B.i, T.i + 1):
        if bt.is_poi(bars, i) and H(i) <= mid and any(bt.bull_fvg(bars, z) for z in range(i, i + 3)):
            if not any(L(q) <= H(i) for q in range(i + 3, k + 1)):
                pois.append(i)
    fvgs = []
    for z in range(B.i, T.i - 1):
        if bt.bull_fvg(bars, z):
            lo, hi = H(z), L(z + 2)
            if hi <= mid and not any(L(q) <= hi for q in range(z + 3, k + 1)):
                fvgs.append((hi, lo, bars[z + 1].t))
    zones = []
    used_liq = set(); skip_poi = set()
    for p in sorted(pois, key=lambda i: -H(i)):
        above = [x for x in lq if x > H(p) and x not in used_liq
                 and not any(H(p) < H(o) < x for o in pois if o != p)]
        below = [x for x in lq if x < bars[p].l]
        if above:
            x = min(above); used_liq.add(x)
            zz = Zone("liq+poi", x, bars[p].l, liq=x, poi=p, t=bars[p].t); zz.poi_hi, zz.poi_lo = H(p), bars[p].l
            zones.append(zz)
        elif below:
            skip_poi.add(p)                        # POI nằm trên thanh khoản → bỏ POI
        else:
            zones.append(Zone("poi", H(p), bars[p].l, poi=p, t=bars[p].t))
    for x in lq:
        if x not in used_liq:
            zones.append(Zone("liq", x, x, liq=x))
    for hi, lo, t in fvgs:
        zones.append(Zone("fvg", hi, lo, t=t))
    if not zones:
        zones.append(Zone("normal", mid, B.price))
    zones.sort(key=lambda z: -z.top)
    return zones


def _info(rec, tr):
    """Ghi thêm mức thanh khoản và khung POI/FVG (giá thật) vào bản ghi lệnh."""
    sg = 1 if tr["side"] == "BUY" else -1
    z = tr["zone"]
    rec["tk"] = sg * z.liq if z.liq is not None else ""
    if z.kind in ("poi", "liq+poi", "fvg"):
        hi, lo = z.poi_hi, z.poi_lo
        rec["vung_tren"], rec["vung_duoi"] = (sg * hi, sg * lo) if sg > 0 else (sg * lo, sg * hi)
    else:
        rec["vung_tren"] = rec["vung_duoi"] = ""


def run(bars, side, spread=0.3, hard_buf=3.0, diag=None, khoa=None):
    D = diag if diag is not None else {}
    inc = lambda key: D.__setitem__(key, D.get(key, 0) + 1)
    ctx, liqs = analyze_daily_full(bars, inverted=(side == "SELL"))
    n = len(bars); trades = []
    wave = None; setup = None; trade = None
    for k in range(1, n - 1):
        mode, T, B, scan = ctx[k]
        j = k + 1; b = bars[j]
        # ---- sóng mới / hết sóng
        if mode == "UP" and T is not None and B is not None and B.i < T.i:
            if wave is None or wave["T"].i != T.i or wave["B"].i != B.i:
                mid = (B.price + T.price) / 2
                wave = {"T": T, "B": B, "mid": mid, "zones": build_zones(B, T, mid, bars, k, liqs), "done": False,
                        "lo": float("inf"), "q": T.i + 1, "khoa": False}
                inc("1_song")
                if setup is not None:
                    setup = None
            # Pha hồi từ đỉnh T đã TẠO ĐÁY (cách 1) mà chưa chạm 50% → đáy nông = thanh khoản; sóng này KHÔNG được BUY,
            # phải đợi thân nến phá đỉnh (sóng mới). Áp dụng cho B4 và C2 (người dùng xác nhận 24/11/2026).
            while wave["q"] <= j and not wave["khoa"]:
                q = wave["q"]
                if bars[q].l < wave["lo"]:
                    wave["lo"], wave["lo_i"] = bars[q].l, q
                if q > T.i and bars[q].c > bars[q - 1].h and wave["lo"] > wave["mid"] and setup is None:
                    wave["khoa"] = True
                    if not wave["done"]:
                        inc("x_khoa_song_day_nong")
                        if khoa is not None:
                            khoa.append({"side": side, "Bi": B.i, "Bp": B.price, "Ti": T.i, "Tp": T.price, "mid": wave["mid"],
                                         "lo_i": wave["lo_i"], "lo": wave["lo"], "j": q})
                wave["q"] += 1
            if wave["khoa"] and trade is None:
                wave["done"] = True
        elif trade is None:
            wave = None; setup = None
        # ---- quản lý lệnh đang mở
        if trade is not None:
            bt._manage(trade, bars, j, trades, None)
            if not trade["done"]:
                if not trade["broke"] and b.c > trade["T"]:
                    trade["broke"] = True
                elif trade["broke"] and trade["tp1"] and b.c < bars[j - 1].l:
                    bt._close(trade, b.c, b.t, "TP2 (đỉnh/đáy mới)", trades, None)
                elif not trade["tp1"] and not trade["be"] and j > trade["j_in"] and b.c < bars[j - 1].l:
                    trade["be"] = True; trade["notes"].append(f"{b.t} đỉnh thấp hơn → SL về điểm vào")
            if trade["done"]:
                trades[-1]["kieu"] = trade["kind"]
                _info(trades[-1], trade)
                if wave is not None and not trades[-1]["exit"].startswith("SL"):
                    wave["done"] = True
                trade = None; setup = None
            continue
        if wave is None or wave["done"] or scan is not None or mode != "UP":
            continue
        # ---- chọn vùng
        if setup is None:
            cand = [z for z in wave["zones"] if not z.used and b.l <= z.top]
            if not cand:
                continue
            z = max(cand, key=lambda z: z.top); z.used = True
            inc("2_cham_" + z.kind)
            setup = {"z": z, "state": "sweep" if z.kind in ("liq", "liq+poi") else "bottom", "low_j": j, "touch_j": j}
        z = setup["z"]
        # ---- kiểu QUÉT thanh khoản (đánh giá trên chính nến chạm)
        if setup["state"] == "sweep":
            x = z.liq; body = abs(b.c - b.o); wick = min(b.o, b.c) - b.l
            if b.l < x and b.c > x and wick > body:
                if z.kind == "liq+poi" and b.l > bars[z.poi].h:
                    inc("x_quet_khong_cham_poi"); setup = None; continue
                half = (min(b.o, b.c) + b.l) / 2
                entry = half if half < x else x
                setup.update(state="pending", entry=entry, low=b.l, hard=b.l - hard_buf, conf_j=j, kind="quet-" + z.kind)
                inc("3_dat_lenh_quet"); continue
            if b.c < x:                              # thân đóng cửa dưới thanh khoản → không phải quét
                if z.kind == "liq+poi":
                    setup = {"z": Zone("poi", bars[z.poi].h, bars[z.poi].l, poi=z.poi, t=z.t), "state": "bottom", "low_j": j, "touch_j": j}
                    if b.l > bars[z.poi].h:
                        setup = None
                        z2 = Zone("poi", bars[z.poi].h, bars[z.poi].l, poi=z.poi, t=z.t); wave["zones"].append(z2)
                        wave["zones"].sort(key=lambda q: -q.top)
                    inc("x_dong_duoi_tk_chuyen_poi")
                else:
                    setup["state"] = "bottom"; setup["z"] = Zone("normal", x, wave["B"].price); inc("x_dong_duoi_tk_binh_thuong")
                if setup is None:
                    continue
            elif b.l < x:
                inc("x_cham_tk_khong_dat_dieu_kien_quet"); setup = None; continue
            else:
                continue                             # chưa chạm tới mức thanh khoản (vùng liq+poi): chờ
            z = setup["z"]
        # ---- kiểu POI / FVG / bình thường: chờ tạo đáy
        if setup["state"] == "bottom":
            if b.h >= wave["T"].price:
                inc("x_huy_ve_T"); setup = None; continue
            if z.kind in ("poi", "fvg") and j == setup["touch_j"] and b.c < z.bot:
                inc("x_vung_bi_pha"); setup = None; continue
            if b.l < bars[setup["low_j"]].l:
                setup["low_j"] = j
            if j > setup["touch_j"] and b.c > bars[j - 1].h:
                lo = bars[setup["low_j"]]
                entry = (min(lo.o, lo.c) + lo.l) / 2
                if entry > lo.l:
                    setup.update(state="pending", entry=entry, low=lo.l, hard=lo.l - hard_buf, conf_j=j, kind=z.kind)
                    inc("3_dat_lenh_" + z.kind)
            continue
        # ---- lệnh chờ
        if setup["state"] == "pending":
            if b.h >= wave["T"].price or b.c < setup["low"]:
                inc("x_huy_lenh_cho"); setup = None; continue
            if b.l <= setup["entry"]:
                if bt.blocked(b.t):
                    inc("x_huy_gio_cam"); setup = None; continue
                inc("4_khop_" + setup["kind"])
                zz = setup["z"]
                trade = {"wstart": wave["B"], "wT": wave["T"], "mid": wave["mid"], "k_in": j, "side": side, "entry": setup["entry"],
                         "low": setup["low"], "hard": setup["hard"], "T": wave["T"].price,
                         "poi": eng.Bar(zz.t or b.t, 0, zz.top, zz.bot, 0), "t_in": b.t, "j_in": j, "size": 1.0, "be": False,
                         "tp1": False, "pnl": 0.0, "done": False, "broke": False, "maxh": b.h, "spread": spread, "be_tf": "M15",
                         "notes": [], "kind": setup["kind"], "zone": zz}
                bt._manage(trade, bars, j, trades, None, first=True)
                if trade["done"]:
                    trades[-1]["kieu"] = trade["kind"]
                    _info(trades[-1], trade)
                    if not trades[-1]["exit"].startswith("SL"):
                        wave["done"] = True
                    trade = None
                setup = None
                continue
            # (Đã bỏ theo yêu cầu người dùng 24/11: KHÔNG huỷ lệnh chờ khi giá tạo đỉnh cách 1 trước khi khớp.)
    return trades


def main():
    import argparse, csv
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv-nen", required=True, help="file nến (M1 hoặc M15), dùng cho cả xu hướng lẫn vào lệnh")
    ap.add_argument("--khung", default="M1", choices=["M1", "M5", "M15"])
    ap.add_argument("--spread", type=float, default=0.3)
    ap.add_argument("--out")
    a = ap.parse_args()
    bars = [eng.Bar(b.t[:16], b.o, b.h, b.l, b.c) for b in eng.load_csv(a.csv_nen)]
    if a.khung != "M1" and len(bars) > 2 and bars[1].t[-2:] != "15" and bars[1].t[-2:] != "00":
        bars = bt.resample(bars, 5 if a.khung == "M5" else 15)
    diag = {}; trades = []
    for side, A in (("BUY", bars), ("SELL", bt.neg(bars))):
        trades += run(A, side, a.spread, diag=diag)
    trades.sort(key=lambda t: t["t_in"])
    print("Phễu:", ", ".join(f"{k}={v}" for k, v in sorted(diag.items())))
    print(bt.stats(trades))
    by = {}
    for t in trades:
        by.setdefault(t.get("kieu", "?"), []).append(t["R"])
    print("Theo kiểu vào lệnh: " + ", ".join(f"{k}: {len(v)} lệnh {sum(v):+.1f}R" for k, v in sorted(by.items())))
    if a.out and trades:
        with open(a.out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(trades[0].keys())); w.writeheader(); w.writerows(trades)
    return trades


if __name__ == "__main__":
    main()
