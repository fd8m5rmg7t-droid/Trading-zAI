#!/usr/bin/env python3
"""Backtest phương pháp đã học: khai thác PHASE 4 tại POI (M15 xác định, M1 vào lệnh).

Quy tắc dùng (knowledge/03-setup.md, 05-quan-ly-lenh.md, 04-quan-ly-von.md, 02-thi-truong.md):
  * Xu hướng/đỉnh/đáy trên M15: tools/smc_engine.py. Chỉ BUY khi xu hướng tăng, SELL khi giảm
    (lệnh SELL chạy bằng cách đảo dấu giá rồi dùng lại đúng logic BUY).
  * Sóng đẩy phase 2 = từ đáy tạo ra đỉnh (B) đến đỉnh mới (T). Order flow thiếu (phase 3 chưa chạm
    đường 50% mà đã phá đỉnh) → sóng tiếp theo vẫn đo từ đáy bắt đầu phase 2 cũ.
  * POI (M15): nến có ít nhất 1 râu dài hơn thân, nến sau đóng cửa trong high–low của nó; nằm TRỌN trong
    discount; có FVG tăng bắt đầu trong vòng 2 nến sau; chưa bị giá quay lại chạm; dùng 1 lần.
  * Lần đầu giá chạm POI mà nến M15 đó đóng cửa dưới low POI → POI hết hiệu lực.
  * M1: sau khi chạm POI, chờ nến xác nhận đáy (đóng cửa > high nến trước); điểm thấp nhất = low thấp nhất
    từ lúc chạm đến nến xác nhận; đặt BUY limit tại 1/2 râu dưới của nến có điểm thấp nhất.
    Huỷ lệnh chờ nếu: giá chạm đỉnh cũ T trước khi khớp, hoặc nến M1 đóng cửa dưới điểm thấp nhất,
    hoặc giá chạm điểm vào trong khung giờ cấm.
  * Dừng lỗ: nến M1 đóng cửa dưới điểm thấp nhất (thoát tại giá đóng cửa); SL cứng = điểm thấp nhất − 3.0.
  * Chốt 1/2 khi chạm T, dời SL về điểm vào (chạm là thoát). Giá tạo đỉnh thấp hơn T trước khi chạm T
    → dời SL về điểm vào. Phần còn lại chốt khi M15 phá T rồi có nến M15 xác nhận đỉnh mới (giá đóng cửa).
  * Không vào lệnh 30' trước/sau giờ mở phiên Á/Âu/Mỹ (giờ VN, có tính đổi giờ mùa hè).
  * Kết quả tính bằng R (1R = khoảng cách điểm vào → SL cứng); trừ spread cố định.
Chưa có: vào lệnh kiểu quét thanh khoản, khai thác phase 3 ngược xu hướng, tránh tin tức.
"""
import argparse
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import smc_engine as eng  # noqa: E402


# ----------------------------------------------------------------------------- giờ giao phiên (VN)
def _last_sunday(y, m):
    d = dt.date(y, m + 1, 1) - dt.timedelta(days=1) if m < 12 else dt.date(y, 12, 31)
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)


def _nth_sunday(y, m, n):
    d = dt.date(y, m, 1)
    d += dt.timedelta(days=(6 - d.weekday()) % 7)
    return d + dt.timedelta(weeks=n - 1)


def session_opens_vn(day):
    y = day.year
    eu_summer = _last_sunday(y, 3) <= day < _last_sunday(y, 10)
    us_summer = _nth_sunday(y, 3, 2) <= day < _nth_sunday(y, 11, 1)
    return [7 * 60, (14 if eu_summer else 15) * 60, (19 if us_summer else 20) * 60]


def blocked(tstr):
    t = dt.datetime.strptime(tstr, "%Y-%m-%d %H:%M")
    m = t.hour * 60 + t.minute
    return any(abs(m - o) <= 30 for o in session_opens_vn(t.date()))


# ----------------------------------------------------------------------------- tiện ích nến
def neg(bars):
    return [eng.Bar(b.t, -b.o, -b.l, -b.h, -b.c) for b in bars]


def is_poi(B, i):
    b = B[i]
    if i + 1 >= len(B):
        return False
    body = abs(b.c - b.o)
    wick = max(b.h - max(b.o, b.c), min(b.o, b.c) - b.l)
    return wick > body and b.l <= B[i + 1].c <= b.h


def bull_fvg(B, k):
    return k + 2 < len(B) and B[k + 2].l > B[k].h


# ----------------------------------------------------------------------------- gộp nến khung lớn
def resample(bars, minutes, anchor="ny17"):
    """Gộp nến. anchor="ny17": mốc ngày = 17:00 New York (giờ máy chủ MT5 phổ biến GMT+2/+3),
    tức 04:00 VN khi Mỹ giờ mùa hè, 05:00 VN mùa đông. Nến H4 bắt đầu tại mốc ngày + bội số 4 giờ."""
    out = []; key = None
    for b in bars:
        t = dt.datetime.strptime(b.t, "%Y-%m-%d %H:%M")
        us_summer = _nth_sunday(t.year, 3, 2) <= t.date() < _nth_sunday(t.year, 11, 1)
        off = 4 if us_summer else 5
        m = ((t.hour - off) % 24) * 60 + t.minute
        start = t - dt.timedelta(minutes=m % minutes)
        k = start.strftime("%Y-%m-%d %H:%M")
        if k != key:
            out.append(eng.Bar(k, b.o, b.h, b.l, b.c)); key = k
        else:
            o = out[-1]; out[-1] = eng.Bar(o.t, o.o, max(o.h, b.h), min(o.l, b.l), b.c)
    return out


# ----------------------------------------------------------------------------- tìm xu hướng lại mỗi ngày
def day_starts(bars, gap_min=30):
    """Chỉ số nến đầu tiên của mỗi ngày giao dịch (sau khoảng nghỉ cuối ngày ≥ gap_min phút)."""
    out = [0]
    for i in range(1, len(bars)):
        t0 = dt.datetime.strptime(bars[i - 1].t, "%Y-%m-%d %H:%M"); t1 = dt.datetime.strptime(bars[i].t, "%Y-%m-%d %H:%M")
        if (t1 - t0).total_seconds() / 60 >= gap_min:
            out.append(i)
    return out


def analyze_daily(bars):
    """Mỗi ngày giao dịch bắt đầu tìm xu hướng lại từ NẾN ĐÓNG CỬA CỦA NGÀY LIỀN TRƯỚC (nến cuối ngày hôm trước)."""
    n = len(bars); ctx = [("UNKNOWN", None, None, None)] * n
    starts = day_starts(bars) + [n]
    for a, b in zip(starts, starts[1:]):
        s = max(0, a - 1)                                   # nến cuối của ngày trước
        r = eng.analyze(bars[s:b])
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
    return ctx


# ----------------------------------------------------------------------------- backtest một chiều (BUY)
def run_long(m15, m1, ctx, side, spread, hard_buf, be_tf="M15", log=None, diag=None):
    D = diag if diag is not None else {}
    inc = lambda key: D.__setitem__(key, D.get(key, 0) + 1)
    import bisect
    t1 = [b.t for b in m1]
    trades = []
    wave = None          # dict: T, start (Swing), mid, pois, mid_touched
    prev_wave = None
    setup = None         # setup đang chạy
    trade = None
    for k in range(1, len(m15) - 1):
        mode, T, B, scan = ctx[k]
        # ---- cập nhật sóng khi có đỉnh mới
        if mode == "UP" and T is not None:
            if wave is None or wave["T"].i != T.i:
                start = B
                if wave is not None and wave["T"].i < T.i and not wave["mid_touched"] and wave["start"].i < T.i:
                    start = wave["start"]           # order flow thiếu
                mid = (start.price + T.price) / 2
                pois = []
                for i in range(start.i, T.i + 1):
                    if not is_poi(m15, i) or m15[i].h > mid:
                        continue
                    if not any(bull_fvg(m15, q) for q in range(i, i + 3)):
                        continue
                    used = any(m15[j].l <= m15[i].h for j in range(i + 3, k + 1))
                    if not used:
                        pois.append(i)
                prev_wave = wave
                inc("1_song"); D["2_poi_hop_le"] = D.get("2_poi_hop_le", 0) + len(pois)
                wave = {"T": T, "start": start, "mid": mid, "pois": sorted(pois, key=lambda i: -m15[i].h),
                        "mid_touched": False}
                if setup and setup["state"] != "open":
                    setup = None
        else:
            if setup and setup["state"] != "open":
                setup = None
            if mode != "UP":
                wave = None
        # ---- duyệt các nến M1 trong nến M15 tiếp theo (k+1)
        j0 = bisect.bisect_left(t1, m15[k + 1].t)
        if j0 is None:
            continue
        j1 = bisect.bisect_left(t1, m15[k + 2].t) if k + 2 < len(m15) else len(m1)
        if j0 >= j1:
            continue
        in_phase3 = wave is not None and mode == "UP" and scan is None
        for j in range(j0, j1):
            b = m1[j]
            if wave is not None and b.l <= wave["mid"]:
                wave["mid_touched"] = True
            # --- quản lý lệnh đang mở
            if trade is not None:
                _manage(trade, m1, j, trades, log)
                if trade["done"]:
                    trade = None; setup = None
                continue
            if not in_phase3:
                continue
            # --- chọn POI để theo dõi
            if setup is None:
                touched = [p for p in wave["pois"] if b.l <= m15[p].h]
                if touched:
                    for p in touched:                    # POI bị chạm = đã dùng
                        wave["pois"].remove(p)
                    p = min(touched, key=lambda q: m15[q].h)   # POI sâu nhất giá đang ở trong
                    setup = {"state": "bottom", "poi": p, "touch_k": k + 1, "low_j": j, "T": wave["T"].price}
                    inc("3_cham_poi")
            if setup is None:
                continue
            if setup["state"] == "bottom":
                if b.h >= setup["T"]:
                    inc("x_huy_cho_day_gia_ve_T"); setup = None; continue
                if b.l < m1[setup["low_j"]].l:
                    setup["low_j"] = j
                if j > 0 and b.c > m1[j - 1].h and j >= setup["low_j"]:
                    lo = m1[setup["low_j"]]
                    entry = (min(lo.o, lo.c) + lo.l) / 2
                    if entry > lo.l:
                        setup.update(state="pending", entry=entry, low=lo.l, hard=lo.l - hard_buf, conf_j=j)
                        inc("4_dat_lenh_cho")
                continue
            if setup["state"] == "pending":
                if b.h >= setup["T"] or b.c < setup["low"]:
                    inc("x_huy_lenh_cho_" + ("gia_ve_T" if b.h >= setup["T"] else "dong_duoi_day")); setup = None; continue
                if b.l <= setup["entry"]:
                    if blocked(b.t):
                        inc("x_huy_gio_cam"); setup = None; continue
                    inc("5_khop_lenh")
                    trade = {"k_in": k + 1, "side": side, "entry": setup["entry"], "low": setup["low"], "hard": setup["hard"],
                             "T": setup["T"], "poi": m15[setup["poi"]], "t_in": b.t, "j_in": j, "size": 1.0,
                             "be": False, "tp1": False, "pnl": 0.0, "done": False, "broke": False,
                             "maxh": b.h, "spread": spread, "be_tf": be_tf, "notes": []}
                    setup["state"] = "open"
                    _manage(trade, m1, j, trades, log, first=True)
                    if trade["done"]:
                        trade = None; setup = None
        # ---- POI hết hiệu lực (nến M15 chạm lần đầu đóng cửa dưới low POI)
        if setup and setup["state"] in ("bottom", "pending") and setup["touch_k"] == k + 1:
            if m15[k + 1].c < m15[setup["poi"]].l:
                inc("x_poi_bi_pha"); setup = None
        # ---- quản lý theo M15: đỉnh thấp hơn / phá T và xác nhận đỉnh mới
        if trade is not None:
            c15 = m15[k + 1]; p15 = m15[k]
            if not trade["broke"] and c15.c > trade["T"]:
                trade["broke"] = True
            elif trade["broke"] and c15.c < p15.l and trade["tp1"]:
                _close(trade, c15.c, c15.t, "TP2 (đỉnh mới M15)", trades, log)
                trade = None; setup = None
            elif (not trade["tp1"] and trade["be_tf"] == "M15" and k > trade["k_in"] and c15.c < p15.l
                  and not trade["be"]):
                trade["be"] = True; trade["notes"].append(f"{c15.t} đỉnh thấp hơn → SL về điểm vào")
    return trades


def _manage(tr, m1, j, trades, log, first=False):
    b = m1[j]
    tr["maxh"] = max(tr["maxh"], b.h)
    # dừng lỗ trước (thận trọng)
    if not tr["be"] and not tr["tp1"]:
        if b.l <= tr["hard"]:
            _close(tr, tr["hard"], b.t, "SL cứng", trades, log); return
        if b.c < tr["low"]:
            _close(tr, b.c, b.t, "SL (đóng cửa dưới điểm thấp nhất)", trades, log); return
    elif b.l <= tr["entry"] and not first:
        _close(tr, tr["entry"], b.t, "Hòa vốn (chạm điểm vào)", trades, log); return
    if not tr["tp1"] and b.h >= tr["T"]:
        tr["pnl"] += 0.5 * (tr["T"] - tr["entry"]); tr["size"] = 0.5; tr["tp1"] = True; tr["be"] = True
        tr["notes"].append(f"{b.t} TP1 chạm đỉnh cũ")
    if tr["be_tf"] == "M1" and not tr["tp1"] and not tr["be"] and j > tr["j_in"] and b.c < m1[j - 1].l:
        tr["be"] = True


def _close(tr, price, t, why, trades, log):
    tr["pnl"] += tr["size"] * (price - tr["entry"])
    risk = tr["entry"] - tr["hard"]
    r = tr["pnl"] / risk - tr["spread"] / risk
    sgn = 1 if tr["side"] == "BUY" else -1
    rec = {"side": tr["side"], "t_in": tr["t_in"], "t_out": t, "entry": sgn * tr["entry"], "hard_sl": sgn * tr["hard"],
           "T": sgn * tr["T"], "risk": risk, "R": r, "R_gross": tr["pnl"] / risk, "exit": why, "tp1": tr["tp1"],
           "notes": "; ".join(tr["notes"]), "low": sgn * tr["low"],
           "poi_h": sgn * (tr["poi"].h if sgn > 0 else tr["poi"].l), "poi_l": sgn * (tr["poi"].l if sgn > 0 else tr["poi"].h),
           "poi_t": tr["poi"].t}
    trades.append(rec); tr["done"] = True
    if log:
        log.append(rec)


# ----------------------------------------------------------------------------- tổng hợp
def stats(trades):
    if not trades:
        return "Không có lệnh nào."
    Rs = [t["R"] for t in trades]
    wins = [r for r in Rs if r > 0.05]; loss = [r for r in Rs if r < -0.05]
    eq = 0; peak = 0; dd = 0
    for r in Rs:
        eq += r; peak = max(peak, eq); dd = min(dd, eq - peak)
    lines = [f"Số lệnh: {len(Rs)}  |  thắng {len(wins)}  thua {len(loss)}  hòa {len(Rs) - len(wins) - len(loss)}",
             f"Tỷ lệ thắng (trên lệnh có kết quả): {len(wins) / max(1, len(wins) + len(loss)) * 100:.1f}%",
             f"Tổng: {sum(Rs):+.2f} R  |  TB mỗi lệnh: {sum(Rs) / len(Rs):+.3f} R",
             f"Lãi TB lệnh thắng: {sum(wins) / max(1, len(wins)):+.2f} R  |  Lỗ TB lệnh thua: {sum(loss) / max(1, len(loss)):+.2f} R",
             f"Sụt giảm lớn nhất: {dd:.2f} R"]
    by = {}
    for t in trades:
        by.setdefault(t["exit"], []).append(t["R"])
    lines.append("Cách thoát lệnh: " + ", ".join(f"{k}: {len(v)} ({sum(v):+.1f}R)" for k, v in sorted(by.items())))
    mon = {}
    for t in trades:
        mon.setdefault(t["t_in"][:7], []).append(t["R"])
    lines.append("Theo tháng: " + ", ".join(f"{k}: {len(v)} lệnh {sum(v):+.1f}R" for k, v in sorted(mon.items())))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--m15", required=True); ap.add_argument("--m1", required=True)
    ap.add_argument("--spread", type=float, default=0.30, help="spread trừ mỗi lệnh (đơn vị giá)")
    ap.add_argument("--hard", type=float, default=3.0, help="SL cứng cách điểm thấp/cao nhất (vàng: 3.0)")
    ap.add_argument("--be-tf", default="M15", choices=["M15", "M1", "none"], help="khung xét 'đỉnh thấp hơn' để dời SL")
    ap.add_argument("--csv", help="ghi danh sách lệnh ra file CSV")
    ap.add_argument("--khung", default="M15/M1", choices=["M15/M1", "H4/M15", "H1/M5"],
                    help="khung xác định xu hướng/POI / khung vào lệnh")
    ap.add_argument("--xu-huong", default="lien-tuc", choices=["lien-tuc", "moi-ngay"],
                    help="moi-ngay: mỗi ngày tìm xu hướng lại từ giá đóng cửa ngày liền trước")
    a = ap.parse_args()
    m15 = eng.load_csv(a.m15); m1 = eng.load_csv(a.m1)
    m15 = [eng.Bar(b.t[:16], b.o, b.h, b.l, b.c) for b in m15]; m1 = [eng.Bar(b.t[:16], b.o, b.h, b.l, b.c) for b in m1]
    if a.khung == "H4/M15":
        m15, m1 = resample(m15, 240), m15
    elif a.khung == "H1/M5":
        m15, m1 = resample(m15, 60), resample(m1, 5)
    print(f"Khung: {a.khung}  ({len(m15)} nến khung lớn, {len(m1)} nến khung vào lệnh)")
    trades = []; diag = {}
    for side, A, Bm in (("BUY", m15, m1), ("SELL", neg(m15), neg(m1))):
        ctx = analyze_daily(A) if a.xu_huong == "moi-ngay" else eng.analyze(A).ctx
        trades += run_long(A, Bm, ctx, side, a.spread, a.hard, a.be_tf, diag=diag)
    print("Phễu lọc:", ", ".join(f"{k}={v}" for k, v in sorted(diag.items())))
    trades.sort(key=lambda t: t["t_in"])
    print(stats(trades))
    if a.csv and trades:
        import csv
        with open(a.csv, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(trades[0].keys())); w.writeheader(); w.writerows(trades)
    return trades


if __name__ == "__main__":
    main()
