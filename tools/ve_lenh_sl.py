#!/usr/bin/env python3
"""Vẽ các lệnh dừng lỗ (M15/M15) từ file CSV kết quả backtest.
Cách dùng: python3 tools/ve_lenh_sl.py XAUUSD_M15.csv trades.csv [số_lệnh]"""
import os, sys, csv
sys.path.insert(0, os.path.dirname(__file__))
import smc_engine as eng
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "DejaVu Sans"
bars = [eng.Bar(b.t[:16], b.o, b.h, b.l, b.c) for b in eng.load_csv(sys.argv[1])]
idx = {b.t: i for i, b in enumerate(bars)}
rows = [r for r in csv.DictReader(open(sys.argv[2])) if r["exit"].startswith("SL")]
N = int(sys.argv[3]) if len(sys.argv) > 3 else 4
step = max(1, len(rows) // N); pick = rows[::step][:N]
fig, axs = plt.subplots(N, 1, figsize=(20, 6.3 * N))
for ax, r in zip(axs, pick):
    f = lambda k: float(r[k]); sell = r["side"] == "SELL"
    ws, wt = int(r["song_bat_dau_i"]), int(r["dinh_cu_i"]); ji, jo = idx[r["t_in"]], idx[r["t_out"]]
    a, b = max(0, ws - 4), min(len(bars), jo + 10)
    for i in range(a, b):
        x = bars[i]; c = "#26a69a" if x.c >= x.o else "#ef5350"; mk = i in (ji, jo)
        ax.plot([i, i], [x.l, x.h], color=c, lw=1.3, zorder=3)
        ax.add_patch(plt.Rectangle((i - .32, min(x.o, x.c)), .64, max(abs(x.c - x.o), .02), color=c, zorder=4, ec="#000" if mk else c, lw=1.5 if mk else 0))
    st, T, mid = f("song_bat_dau"), f("T"), f("mid")
    lo, hi = (mid, st) if sell else (st, mid)
    ax.add_patch(plt.Rectangle((wt, lo), b - wt, hi - lo, color="#ffcdd2" if sell else "#c8e6c9", alpha=.45, zorder=1))
    ax.annotate("", xy=(wt, T), xytext=(ws, st), arrowprops=dict(arrowstyle="-|>", color="#6a1b9a", lw=2))
    lines = [(T, "#f57f17", "--", "đáy cũ T (TP1)" if sell else "đỉnh cũ T (TP1)"), (mid, "#6a1b9a", "--", "50% pha đẩy"),
             (f("entry"), "#1565c0", "-", ("SELL " if sell else "BUY ") + f"{f('entry'):.2f} (1/2 râu)"),
             (f("low"), "#c62828", "--", ("điểm cao nhất " if sell else "điểm thấp nhất ") + f"{f('low'):.2f}"), (f("hard_sl"), "#6a1b9a", ":", f"SL cứng {f('hard_sl'):.2f}")]
    for y, c, ls, lab in lines:
        ax.plot([wt, b], [y, y], color=c, ls=ls, lw=1.4, zorder=2); ax.text(b + .3, y, lab, color=c, fontsize=9, va="center", fontweight="bold")
    ax.axvline(ji, color="#1565c0", ls=":", lw=1.2); ax.axvline(jo, color="#c62828", ls=":", lw=1.2)
    yl = ax.get_ylim()
    ax.text(ji, yl[1], " vào", color="#1565c0", fontsize=9.5, va="top", fontweight="bold"); ax.text(jo, yl[1], " ra", color="#c62828", fontsize=9.5, va="top", fontweight="bold")
    ax.set_title(f"{r['side']}  vào {r['t_in']}  ra {r['t_out']}  →  {r['exit']}  ({float(r['R']):+.2f}R)", loc="left", fontsize=12, fontweight="bold", color="#c62828")
    ticks = list(range(a, b, 2)); ax.set_xticks(ticks); ax.set_xticklabels([bars[i].t[5:] if i == a else bars[i].t[11:] for i in ticks], fontsize=8)
    ax.set_xlim(a - 1, b + 9)
fig.suptitle("Các lệnh DỪNG LỖ – XAUUSD M15/M15 (tìm xu hướng lại mỗi ngày, khai thác pha đẩy). Mũi tên tím: pha đẩy; vùng màu: premium (SELL) / discount (BUY)",
             fontsize=13.5, fontweight="bold")
plt.tight_layout(rect=(0, 0, 1, .975)); plt.savefig("backtest/lenh-sl-m15.png", dpi=80)
for r in pick: print(r["side"], r["t_in"], r["t_out"], r["exit"], round(float(r["R"]), 2))
print(len(rows), "lệnh SL tổng cộng")
