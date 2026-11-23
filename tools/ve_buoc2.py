#!/usr/bin/env python3
"""BƯỚC 2: sau khi xác nhận xu hướng – sóng đẩy phase 2 và PnD (premium/discount).
Cách dùng: python3 tools/ve_buoc2.py 2026-10-22 duong/dan/XAUUSD_M15.csv"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import smc_engine as eng, backtest as bt
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "DejaVu Sans"
DAY = sys.argv[1]; CSV = sys.argv[2]
bars = [eng.Bar(b.t[:16], b.o, b.h, b.l, b.c) for b in eng.load_csv(CSV)]
st = bt.day_starts(bars); k = next(i for i, x in enumerate(st) if bars[x].t >= DAY + " 05:00")
s = st[k] - 1; e = st[k + 1] if k + 1 < len(st) else len(bars)
seg = bars[s:e]; r = eng.analyze(seg, start_rule="prev_close")
CONF = next(i for i, t in r.events if t.startswith("Xác nhận"))
mode, T, B, _ = r.ctx[CONF]
up = mode == "UP"
start, end = (B, T) if up else (T, B)          # sóng đẩy: từ cực trị tạo ra đến đỉnh/đáy gần nhất
mid = (start.price + end.price) / 2
a = 0; b = min(len(seg), CONF + 5)
fig, ax = plt.subplots(figsize=(21, 10))
ax.axvspan(-.5, CONF - .5, color="#f5f5f5", zorder=0)
for i in range(a, b):
    x = seg[i]; c = "#26a69a" if x.c >= x.o else "#ef5350"
    ax.plot([i, i], [x.l, x.h], color=c, lw=1.3, zorder=3)
    ax.add_patch(plt.Rectangle((i - .32, min(x.o, x.c)), .64, max(abs(x.c - x.o), .02), color=c, zorder=4))
hi, lo = max(start.price, end.price), min(start.price, end.price)
x0 = start.i - .5
ax.add_patch(plt.Rectangle((x0, mid), b - x0, hi - mid, color="#ffcdd2", alpha=.5, zorder=1))
ax.add_patch(plt.Rectangle((x0, lo), b - x0, mid - lo, color="#c8e6c9", alpha=.55, zorder=1))
for y, ls in ((hi, "-"), (lo, "-"), (mid, "--")):
    ax.plot([x0, b], [y, y], color="#444", lw=1.3, ls=ls, zorder=2)
ax.text(b + .3, (hi + mid) / 2, "PREMIUM", fontsize=12, fontweight="bold", color="#c62828", va="center")
ax.text(b + .3, (lo + mid) / 2, "DISCOUNT", fontsize=12, fontweight="bold", color="#2e7d32", va="center")
ax.text(b + .3, mid, f"50% = {mid:.2f}", fontsize=10, fontweight="bold", color="#333", va="center")
ax.annotate("", xy=(end.i, end.price), xytext=(start.i, start.price), arrowprops=dict(arrowstyle="-|>", color="#6a1b9a", lw=2.6))
rg = hi - lo
nm_s = "Đáy" if up else "Đỉnh"; nm_e = "Đỉnh" if up else "Đáy"
ax.scatter([start.i], [start.price], s=120, color="#6a1b9a", zorder=6)
ax.text(start.i, start.price + (-rg * .04 if up else rg * .04), f"{nm_s} tạo ra {nm_e.lower()} gần nhất\n= ĐIỂM BẮT ĐẦU sóng đẩy\n{start.price:.2f} ({seg[start.i].t[11:]})",
        ha="center", va="top" if up else "bottom", fontsize=10, fontweight="bold", color="#6a1b9a")
ax.scatter([end.i], [end.price], s=120, color="#f57f17", zorder=6)
ax.text(end.i, end.price + (rg * .04 if up else -rg * .04), f"{nm_e} gần nhất = KẾT THÚC sóng đẩy\n{end.price:.2f} ({seg[end.i].t[11:]})",
        ha="center", va="bottom" if up else "top", fontsize=10, fontweight="bold", color="#e65100")
ax.text((start.i + end.i) / 2 + .8, mid, "SÓNG ĐẨY\nPHASE 2", fontsize=12, fontweight="bold", color="#6a1b9a", va="center")
ax.axvline(CONF, color="#2e7d32" if up else "#c62828", lw=1.3, ls="--")
ax.text(CONF + .3, hi + rg * .1, f"{seg[CONF].t[11:]} xác nhận xu hướng {'TĂNG' if up else 'GIẢM'}\n→ đo PnD trên sóng đẩy gần nhất",
        fontsize=11, fontweight="bold", color="#2e7d32" if up else "#c62828", va="top")
ax.text(.01, -.06, f"Xu hướng {'tăng' if up else 'giảm'}: chỉ tìm lệnh {'BUY khi giá hồi về DISCOUNT' if up else 'SELL khi giá hồi lên PREMIUM'} (phase 3 phải chạm ít nhất đường 50%). "
        "Đo theo râu nến. Đo lại mỗi khi có đỉnh/đáy mới.", transform=ax.transAxes, va="top", fontsize=10.5)
ticks = list(range(a, b, 2)); ax.set_xticks(ticks); ax.set_xticklabels([seg[i].t[11:] for i in ticks], fontsize=8.5)
yl = min(x.l for x in seg[a:b]); yh = max(x.h for x in seg[a:b])
ax.set_xlim(a - 1, b + 6); ax.set_ylim(yl - (yh - yl) * .12, yh + (yh - yl) * .15)
ax.set_title(f"BƯỚC 2 – XAUUSD M15, ngày {seg[1].t[8:10]}/{seg[1].t[5:7]}/{seg[1].t[:4]}: xác định SÓNG ĐẨY PHASE 2 và đo PnD (premium / discount)",
             loc="left", fontsize=13, fontweight="bold")
plt.tight_layout(); out = f"backtest/buoc-2-m15-{DAY}.png"; plt.savefig(out, dpi=90); print(out, start.price, end.price, mid)
