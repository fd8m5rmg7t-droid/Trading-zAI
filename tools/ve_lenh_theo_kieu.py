#!/usr/bin/env python3
"""Vẽ lệnh mẫu theo từng KIỂU vào lệnh (fvg / poi / quét thanh khoản / quét+POI / bình thường) từ kết quả vao_lenh_uu_tien.py.
Cách dùng: python3 tools/ve_lenh_theo_kieu.py nen.csv ket_qua.csv"""
import os, sys, csv
sys.path.insert(0, os.path.dirname(__file__))
import smc_engine as eng
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "DejaVu Sans"
bars = [eng.Bar(b.t[:16], b.o, b.h, b.l, b.c) for b in eng.load_csv(sys.argv[1])]
idx = {b.t: i for i, b in enumerate(bars)}
rows = list(csv.DictReader(open(sys.argv[2])))
TEN = {"fvg": "FVG (khai thác độc lập)", "poi": "POI", "quet-liq": "QUÉT THANH KHOẢN", "quet-liq+poi": "QUÉT THANH KHOẢN + râu chạm POI",
       "normal": "BÌNH THƯỜNG (không có vùng, chạm 50%)"}
out = []
for kieu in TEN:
    rs = [r for r in rows if r["kieu"] == kieu]
    if not rs:
        continue
    win = max(rs, key=lambda r: float(r["R"])); loss = min(rs, key=lambda r: float(r["R"]))
    pick = [win] if win is loss else [win, loss]
    fig, axs = plt.subplots(len(pick), 1, figsize=(20, 7.2 * len(pick)), squeeze=False)
    for ax, r in zip(axs[:, 0], pick):
        f = lambda k: float(r[k]); sell = r["side"] == "SELL"
        ws, wt = int(r["song_bat_dau_i"]), int(r["dinh_cu_i"]); ji, jo = idx[r["t_in"]], idx[r["t_out"]]
        a = max(ws - 5, ji - 260); b = min(len(bars), jo + 25)
        for i in range(a, b):
            x = bars[i]; c = "#26a69a" if x.c >= x.o else "#ef5350"
            ax.plot([i, i], [x.l, x.h], color=c, lw=.9, zorder=3)
            ax.add_patch(plt.Rectangle((i - .32, min(x.o, x.c)), .64, max(abs(x.c - x.o), .01), color=c, zorder=4))
        st, T, mid = f("song_bat_dau"), f("T"), f("mid")
        hi, lo = max(st, T), min(st, T); x0 = max(a, min(ws, wt))
        ax.add_patch(plt.Rectangle((x0, mid), b - x0, hi - mid, color="#ffcdd2", alpha=.35, zorder=1))
        ax.add_patch(plt.Rectangle((x0, lo), b - x0, mid - lo, color="#c8e6c9", alpha=.4, zorder=1))
        if ws >= a:
            ax.annotate("", xy=(wt, T), xytext=(ws, st), arrowprops=dict(arrowstyle="-|>", color="#6a1b9a", lw=2))
        if r.get("vung_tren"):
            zt, zb = float(r["vung_tren"]), float(r["vung_duoi"])
            ax.add_patch(plt.Rectangle((a, zb), b - a, zt - zb, color="#9575cd", alpha=.35, zorder=2))
            ax.text(b + .5, (zt + zb) / 2, "FVG" if kieu == "fvg" else "POI", color="#4527a0", fontsize=10, fontweight="bold", va="center")
        if r.get("tk"):
            y = float(r["tk"])
            ax.plot([a, b], [y, y], color="#ef6c00", lw=2.2, ls="--", zorder=5); ax.text(b + .5, y, "THANH KHOẢN", color="#ef6c00", fontsize=9.5, fontweight="bold", va="center")
        for y, c, ls, lab in [(T, "#f57f17", "--", ("đáy" if sell else "đỉnh") + " T (TP1)"), (mid, "#6a1b9a", "--", "50% (sóng từ mốc cấu trúc)"),
                              (f("entry"), "#1565c0", "-", ("SELL " if sell else "BUY ") + f"{f('entry'):.2f}"),
                              (f("low"), "#c62828", "--", "điểm cao nhất" if sell else "điểm thấp nhất"), (f("hard_sl"), "#6a1b9a", ":", "SL cứng")]:
            ax.plot([a, b], [y, y], color=c, ls=ls, lw=1.3, zorder=5); ax.text(b + .5, y, lab, color=c, fontsize=9, va="center", fontweight="bold")
        ax.axvline(ji, color="#1565c0", ls=":", lw=1.2); ax.axvline(jo, color="#333", ls=":", lw=1.2)
        R = f("R"); col = "#2e7d32" if R > .05 else "#c62828"
        ax.set_title(f"{r['side']}  vào {r['t_in']}  ra {r['t_out']}  →  {r['exit']}  ({R:+.2f}R)   [mốc cấu trúc {abs(st):.2f} → {abs(T):.2f}]",
                     loc="left", fontsize=11.5, fontweight="bold", color=col)
        ticks = list(range(a, b, max(1, (b - a) // 10))); ax.set_xticks(ticks); ax.set_xticklabels([bars[i].t[5:] for i in ticks], fontsize=8)
        ax.set_xlim(a - 1, b + 22)
    fig.suptitle(f"Kiểu vào lệnh: {TEN[kieu]}  –  lệnh LÃI lớn nhất và LỖ lớn nhất (XAUUSD M1, 2026)", fontsize=14, fontweight="bold")
    plt.tight_layout(rect=(0, 0, 1, .96)); p = f"backtest/kieu-{kieu}.png"; plt.savefig(p, dpi=80); out.append(p); plt.close(fig)
    for r in pick: print(kieu, r["side"], r["t_in"], r["exit"], round(float(r["R"]), 2))
print(out)
