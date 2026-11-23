#!/usr/bin/env python3
"""Vẽ BƯỚC 1 (xác định xu hướng đầu ngày từ nến đóng cửa ngày trước) cho một ngày bất kỳ trên M15.
Cách dùng: python3 tools/ve_buoc1.py 2026-09-08 duong/dan/XAUUSD_M15.csv"""
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
CONF, EV = next((i, t) for i, t in r.events if t.startswith("Xác nhận"))
up = "TĂNG" in EV
a, b = 0, min(len(seg), CONF + 6)
LAB = {"open": " (điểm bắt đầu)", "m12": " (cách 1)", "between": " (cách 2)", "break": " (phá vỡ)"}
fig, ax = plt.subplots(figsize=(21, 10))
ax.axvspan(-.5, CONF - .5, color="#eeeeee", zorder=0)
ax.axvspan(CONF - .5, b, color="#e8f5e9" if up else "#ffebee", zorder=0)
for i in range(a, b):
    x = seg[i]; c = "#26a69a" if x.c >= x.o else "#ef5350"
    ax.plot([i, i], [x.l, x.h], color=c, lw=1.3, zorder=3)
    ax.add_patch(plt.Rectangle((i - .32, min(x.o, x.c)), .64, max(abs(x.c - x.o), .02), color=c, zorder=4,
                               ec="#000" if i == 0 else c, lw=1.8 if i == 0 else 0))
lo = min(x.l for x in seg[a:b]); hi = max(x.h for x in seg[a:b]); rg = hi - lo
seen = set(); sw = []
for w in sorted([w for w in r.swings if w.conf <= CONF], key=lambda w: w.i):
    if (w.kind, w.i) not in seen:
        seen.add((w.kind, w.i)); sw.append(w)
nt = nb = 0
for w in sw:
    top = w.kind == "T"
    if top: nt += 1; n = nt
    else: nb += 1; n = nb
    ax.scatter([w.i], [w.price], marker="v" if top else "^", s=110, color="#f57f17" if top else "#1565c0", zorder=6)
    ax.text(w.i, w.price + (rg * .025 if top else -rg * .025), f"{'Đỉnh' if top else 'Đáy'} {n}{LAB[w.how]}\n{w.price:.2f}",
            ha="center", va="bottom" if top else "top", fontsize=9.5, fontweight="bold", color="#e65100" if top else "#0d47a1", zorder=7)
    ax.plot([w.conf], [seg[w.conf].c], marker="o", ms=7, mfc="none", mec="#555", zorder=7)
ax.plot([w.i for w in sw], [w.price for w in sw], color="#616161", lw=1.2, ls="--", zorder=5)
tops = [w for w in sw if w.kind == "T"][-2:]; bots = [w for w in sw if w.kind == "B"][-2:]
ax.plot([w.i for w in tops], [w.price for w in tops], color="#e65100", lw=2.8, ls=(0, (6, 3)), zorder=6)
ax.plot([w.i for w in bots], [w.price for w in bots], color="#0d47a1", lw=2.8, ls=(0, (6, 3)), zorder=6)
ax.axvline(CONF, color="#2e7d32" if up else "#c62828", lw=1.3, ls="--")
cmp = ">" if up else "<"
ax.text(CONF + .3, hi + rg * .06, f"{seg[CONF].t[11:]} XÁC NHẬN XU HƯỚNG {'TĂNG' if up else 'GIẢM'}\n"
        f"(Đỉnh {nt} {cmp} Đỉnh {nt-1}, Đáy {nb} {cmp} Đáy {nb-1})", fontsize=11, fontweight="bold",
        color="#2e7d32" if up else "#c62828", va="top")
for i, t in r.events:
    if i < CONF and t.startswith("Vượt"):
        ax.axvline(i, color="#ef6c00", lw=1.2, ls=":")
        ax.text(i - .2, lo - rg * .02, f"{seg[i].t[11:]}: giá vượt điểm bắt đầu\nkhi chưa phá {'Đáy 1' if 'Đáy' in t else 'Đỉnh 1'}\n→ chờ đỉnh mới + đáy mới (cách 1)",
                fontsize=9.5, fontweight="bold", color="#ef6c00", va="top", ha="right")
d0 = "XUỐNG" if sw[0].kind == "T" else "LÊN"
ax.annotate(f"ĐIỂM BẮT ĐẦU: nến đóng cửa ngày trước\n({seg[0].t[11:]} sáng {seg[0].t[8:10]}/{seg[0].t[5:7]}, đóng {seg[0].c:.2f})\n→ giá đi {d0} trước",
            xy=(0, seg[0].c), xytext=(2.5, hi + rg * .06), fontsize=9.5, fontweight="bold", va="top", arrowprops=dict(arrowstyle="->"))
ticks = list(range(a, b, 2)); ax.set_xticks(ticks); ax.set_xticklabels([seg[i].t[11:] for i in ticks], fontsize=8.5)
ax.set_xlim(a - 1, b + 1); ax.set_ylim(lo - rg * .18, hi + rg * .14)
ax.set_title(f"BƯỚC 1 – XAUUSD M15, ngày {seg[1].t[8:10]}/{seg[1].t[5:7]}/{seg[1].t[:4]}: xác định xu hướng từ nến đóng cửa ngày trước",
             loc="left", fontsize=13, fontweight="bold")
ax.text(.01, -.06, "Vòng tròn rỗng = nến xác nhận. Nét đứt xám: nối đỉnh/đáy theo thời gian. Nét đứt đậm: 2 đỉnh (cam) và 2 đáy (xanh) dùng để kết luận.",
        transform=ax.transAxes, va="top", fontsize=10)
plt.tight_layout(); out = f"backtest/buoc-1-m15-{DAY}.png"; plt.savefig(out, dpi=90)
print(out)
for w in sw: print(" ", w.kind, seg[w.i].t[11:], round(w.price, 2), w.how, "xác nhận", seg[w.conf].t[11:])
for i, t in r.events:
    if i <= CONF: print(" ", seg[i].t[11:], t)
