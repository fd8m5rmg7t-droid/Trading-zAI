#!/usr/bin/env python3
"""Vẽ pha ĐẨY / pha HỒI, PnD của từng pha đẩy và tính hợp lệ của pha hồi cho một ngày (M15).
Cách dùng: python3 tools/ve_pha_ngay.py 2026-10-22 duong/dan/XAUUSD_M15.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import smc_engine as eng, backtest as bt
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "DejaVu Sans"
DAY, CSV = sys.argv[1], sys.argv[2]
bars = [eng.Bar(b.t[:16], b.o, b.h, b.l, b.c) for b in eng.load_csv(CSV)]
st = bt.day_starts(bars); k = next(i for i, x in enumerate(st) if bars[x].t >= DAY + " 05:00")
s = st[k] - 1; e = st[k + 1] if k + 1 < len(st) else len(bars)
seg = bars[s:e]; n = len(seg); r = eng.analyze(seg, start_rule="prev_close")
CONF = next(i for i, t in r.events if t.startswith("Xác nhận"))
mode, T, B, _ = r.ctx[CONF]; up = mode == "UP"
# chuỗi cực trị xen kẽ sau khi xác nhận: [điểm bắt đầu pha đẩy, cực trị pha đẩy, cực trị pha hồi, ...]
pts = [(T.i, T.price), (B.i, B.price)] if not up else [(B.i, B.price), (T.i, T.price)]
for i in range(CONF + 1, n):
    m2, T2, B2, _ = r.ctx[i]
    if m2 != mode:
        break
    a, b = ((B2, T2) if up else (T2, B2))
    if b.i != pts[-1][0]:
        pts.append((a.i, a.price)); pts.append((b.i, b.price))
last = pts[-1][0]
scan_end = r.ctx[n - 1][3]           # đang phá đỉnh/đáy nhưng chưa xác nhận đỉnh/đáy mới
rng = range(last + 1, scan_end if scan_end is not None else n)
open_end = False; tail_push = None
if len(rng):
    j = min(rng, key=lambda q: seg[q].l) if up else max(rng, key=lambda q: seg[q].h)
    pts.append((j, seg[j].l if up else seg[j].h)); open_end = scan_end is None
    if scan_end is not None:
        tail_push = (j, scan_end)
fig, ax = plt.subplots(figsize=(24, 11))
for i, x in enumerate(seg):
    c = "#26a69a" if x.c >= x.o else "#ef5350"
    ax.plot([i, i], [x.l, x.h], color=c, lw=1.2, zorder=3)
    ax.add_patch(plt.Rectangle((i - .32, min(x.o, x.c)), .64, max(abs(x.c - x.o), .02), color=c, zorder=4))
ax.axvspan(-.5, CONF - .5, color="#eeeeee", zorder=0)
ax.text(CONF / 2, max(x.h for x in seg) + 4, "Chưa rõ xu hướng (bước 1)", ha="center", fontsize=11, fontweight="bold", color="#777")
start_i, start_p = pts[0]
rows = []; liq = []
for q in range(0, len(pts) - 1, 2):
    a_i, a_p = (start_i, start_p)
    b_i, b_p = pts[q + 1]
    hi_end = pts[q + 2] if q + 2 < len(pts) else None
    mid = (a_p + b_p) / 2
    ax.axvspan(pts[q][0], b_i, color="#e8f5e9", alpha=.8, zorder=0)
    ax.annotate("", xy=(b_i, b_p), xytext=(a_i, a_p), arrowprops=dict(arrowstyle="-|>", color="#6a1b9a", lw=2.2))
    x1 = hi_end[0] + 1 if hi_end else n
    ax.plot([b_i, x1], [mid, mid], color="#6a1b9a", ls="--", lw=1.4, zorder=5)
    ax.text(b_i + .3, mid + (1 if up else -1) * 0, f"50% = {mid:.2f} ", fontsize=8.5, color="#6a1b9a", va="bottom" if not up else "top", ha="left", fontweight="bold")
    nr = q // 2 + 1
    ax.text((pts[q][0] + b_i) / 2, max(x.h for x in seg) + (6.5 if nr % 2 else 1), f"PHA ĐẨY {nr}", ha="center", fontsize=11, fontweight="bold", color="#2e7d32")
    if hi_end:
        h_i, h_p = hi_end
        ax.axvspan(b_i, h_i, color="#e3f2fd", alpha=.8, zorder=0)
        touched = (h_p >= mid) if not up else (h_p <= mid)
        lab = "hợp lệ (chạm 50%)" if touched else "KHÔNG chạm 50% → order flow THIẾU"
        col = "#2e7d32" if touched else "#c62828"
        fin = (q + 2 == len(pts) - 1) and open_end
        ax.text((b_i + h_i) / 2, max(x.h for x in seg) + (1 if nr % 2 else 6.5), f"PHA HỒI {nr}" + (" (chưa kết thúc)" if fin else ""), ha="center", fontsize=11, fontweight="bold", color="#1565c0")
        ax.scatter([h_i], [h_p], s=90, color="#1565c0" if up else "#f57f17", marker="^" if up else "v", zorder=6)
        ax.text(h_i, h_p + (-2 if up else 2), f"{h_p:.2f}\n{lab}", ha="center", va="top" if up else "bottom", fontsize=9, fontweight="bold", color=col)
        rows.append((nr, seg[a_i].t[11:], a_p, seg[b_i].t[11:], b_p, mid, seg[h_i].t[11:], h_p, touched))
        if touched:
            start_i, start_p = h_i, h_p
        else:
            liq.append((h_i, h_p))
    ax.scatter([b_i], [b_p], s=90, color="#f57f17" if up else "#1565c0", marker="v" if up else "^", zorder=6)
    ax.text(b_i, b_p + (2 if up else -2), f"{b_p:.2f}", ha="center", va="bottom" if up else "top", fontsize=9, fontweight="bold", color="#0d47a1")
ax.scatter([pts[0][0]], [pts[0][1]], s=110, color="#6a1b9a", zorder=6)
# đường zigzag nối tất cả đỉnh/đáy (kể cả đỉnh/đáy của pha hồi không đủ)
ax.plot([p[0] for p in pts], [p[1] for p in pts], color="#111", lw=2.6, zorder=5, alpha=.85)
for h_i, h_p in liq:
    ax.plot([h_i, n + .5], [h_p, h_p], color="#ef6c00", lw=2, ls="--", zorder=5)
    ax.text(n + .6, h_p, f"THANH KHOẢN {h_p:.2f}\n({'đỉnh' if not up else 'đáy'} của pha hồi không đủ)", fontsize=9, fontweight="bold", color="#ef6c00", va="center")
if tail_push:
    j, sc = tail_push
    ax.axvspan(j, n - .5, color="#e8f5e9", alpha=.8, zorder=0)
    ax.text((j + n) / 2, max(x.h for x in seg) + 1, "PHA ĐẨY tiếp theo\n(đã phá đáy, chưa xác nhận đáy mới)", ha="center", fontsize=10, fontweight="bold", color="#2e7d32", va="bottom")
    ax.annotate("thân nến phá đáy", xy=(sc, seg[sc].c), xytext=(sc + 2, seg[sc].c - 6), fontsize=9, color="#c62828", fontweight="bold", arrowprops=dict(arrowstyle="->", color="#c62828"))
ticks = list(range(0, n, 4)); ax.set_xticks(ticks); ax.set_xticklabels([seg[i].t[11:] for i in ticks], fontsize=8.5)
ax.set_xlim(-1, n + 14); ax.set_ylim(min(x.l for x in seg) - 10, max(x.h for x in seg) + 12)
ax.set_title(f"XAUUSD M15 – ngày {seg[1].t[8:10]}/{seg[1].t[5:7]}/{seg[1].t[:4]}: xu hướng {'TĂNG' if up else 'GIẢM'} (xác nhận {seg[CONF].t[11:]}) – PHA ĐẨY (xanh lá) / PHA HỒI (xanh dương), "
             "PnD đo trên pha đẩy gần nhất", loc="left", fontsize=12.5, fontweight="bold")
ax.text(.01, -.05, "Đường đen: đường đi của giá qua các đỉnh/đáy. Mũi tên tím: pha đẩy dùng để đo PnD. Nét đứt tím: 50%. Pha hồi hợp lệ khi chạm 50%; "
        "pha hồi không đủ (order flow thiếu): đỉnh của nó (xu hướng giảm) / đáy của nó (xu hướng tăng) là THANH KHOẢN (nét đứt cam).", transform=ax.transAxes, va="top", fontsize=10)
plt.tight_layout(); out = f"backtest/pha-day-hoi-{DAY}.png"; plt.savefig(out, dpi=85)
print(out)
for row in rows: print(row)
