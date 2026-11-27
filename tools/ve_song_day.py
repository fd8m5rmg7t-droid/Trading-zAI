#!/usr/bin/env python3
"""Vẽ lại SÓNG ĐẨY thật rõ (mỗi ảnh 1 sóng, nến đánh số) để người dùng chỉ ra các POI quan trọng.
Lấy các sóng bị khoá rồi giá về discount (cùng số thứ tự với backtest/song-khoa-m15/NĂM/danh-sach.md).
Không vẽ POI/FVG/thanh khoản của bộ máy – chỉ có nến, sóng đẩy, 50% và đáy/đỉnh nông.

Cách dùng: python3 tools/ve_song_day.py nen_M1.csv thu_muc_ra NHAN --so 1-6
"""
import os, sys, argparse, bisect
sys.path.insert(0, os.path.dirname(__file__))
import smc_engine as eng
import backtest as bt
import vao_lenh_uu_tien as vl
from ve_song_khoa import phan_loai
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "DejaVu Sans"


def ve(bars, so, r, q_end, path, nhan):
    sg = 1 if r["side"] == "BUY" else -1
    P = lambda x: sg * x
    a = max(0, r["Bi"] - 3); b = min(len(bars), q_end + 6)
    fig, ax = plt.subplots(figsize=(max(14, (b - a) * 0.32 + 4), 8.5))
    for i in range(a, b):
        x = bars[i]; c = "#26a69a" if x.c >= x.o else "#ef5350"
        ax.plot([i, i], [x.l, x.h], color="#333", lw=1.0, zorder=3)
        ax.add_patch(plt.Rectangle((i - .35, min(x.o, x.c)), .7, max(abs(x.c - x.o), .01), facecolor=c, edgecolor="#333", lw=.5, zorder=4))
    lo_all = min(bars[i].l for i in range(a, b)); hi_all = max(bars[i].h for i in range(a, b)); rg = hi_all - lo_all
    for i in range(a, b):                              # số nến, đếm từ điểm bắt đầu sóng đẩy
        n = i - r["Bi"] + 1
        ax.text(i, lo_all - rg * .035, str(n), fontsize=8.5, ha="center", va="top", fontweight="bold", color="#1565c0" if n >= 1 else "#999",
                rotation=90 if b - a > 45 else 0)
    Bp, Tp, mid, lo = P(r["Bp"]), P(r["Tp"]), P(r["mid"]), P(r["lo"])
    x0 = r["Bi"]
    hi_, lo_ = max(Bp, Tp), min(Bp, Tp)
    ax.add_patch(plt.Rectangle((x0, mid), b - x0, hi_ - mid, color="#ffcdd2", alpha=.25, zorder=0))
    ax.add_patch(plt.Rectangle((x0, lo_), b - x0, mid - lo_, color="#c8e6c9", alpha=.3, zorder=0))
    ax.annotate("", xy=(r["Ti"], Tp), xytext=(r["Bi"], Bp), arrowprops=dict(arrowstyle="-|>", color="#6a1b9a", lw=2, alpha=.6), zorder=2)
    for y, c, ls, lab in [(Tp, "#f57f17", "--", "ĐỈNH" if sg > 0 else "ĐÁY"), (mid, "#6a1b9a", "--", f"50%  {mid:.2f}"),
                          (Bp, "#6a1b9a", "-", "MỐC CẤU TRÚC"), (lo, "#ef6c00", ":", "đáy nông" if sg > 0 else "đỉnh nông")]:
        ax.plot([x0, b], [y, y], color=c, ls=ls, lw=1.2, zorder=5)
        ax.text(b + .3, y, f"{lab}" if "50%" in lab else f"{lab}  {y:.2f}", color=c, fontsize=9, va="center", fontweight="bold")
    ax.axvline(r["j"], color="#ef6c00", ls=":", lw=1.2); ax.text(r["j"], hi_all + rg * .02, "khoá", color="#ef6c00", fontsize=9, ha="center", fontweight="bold")
    ax.axvline(q_end, color="#333", ls=":", lw=1.2); ax.text(q_end, hi_all + rg * .02, "chạm 50%", color="#333", fontsize=9, ha="center", fontweight="bold")
    step = max(1, (b - a) // 12); ticks = list(range(a, b, step))
    ax.set_xticks(ticks); ax.set_xticklabels([bars[i].t[5:] for i in ticks], fontsize=8)
    ax.set_ylim(lo_all - rg * .12, hi_all + rg * .07); ax.set_xlim(a - 1, b + 6)
    ax.grid(axis="y", alpha=.25)
    ax.set_title(f"{nhan} #{so} – {r['side']} – sóng đẩy {bars[r['Bi']].t} → {bars[r['Ti']].t}   "
                 f"(số xanh dưới nến = số thứ tự nến, nến 1 = điểm bắt đầu sóng)", loc="left", fontsize=11.5, fontweight="bold")
    plt.tight_layout(); plt.savefig(path, dpi=100); plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nen"); ap.add_argument("out"); ap.add_argument("nhan")
    ap.add_argument("--so", default="1-6", help="số thứ tự sóng (theo danh-sach.md của song-khoa), ví dụ 1-6 hoặc 1,4,9")
    a = ap.parse_args()
    chon = set()
    for p in a.so.split(","):
        x, _, y = p.partition("-"); chon.update(range(int(x), int(y or x) + 1))
    os.makedirs(a.out, exist_ok=True)
    bars = bt.resample([eng.Bar(b.t[:16], b.o, b.h, b.l, b.c) for b in eng.load_csv(a.nen)], 15)
    st = bt.day_starts(bars) + [len(bars)]
    het_ngay = lambda j: st[bisect.bisect_right(st, j)]
    ds = []
    for side, D in (("BUY", bars), ("SELL", bt.neg(bars))):
        kh = []
        vl.run(D, side, khoa=kh)
        for r in kh:
            kq, q = phan_loai(D, r, het_ngay); ds.append((r, kq, q))
    ds.sort(key=lambda x: x[0]["j"])
    A = [x for x in ds if x[1] == "A"]
    for so, (r, kq, q) in enumerate(A, 1):
        if so in chon:
            p = os.path.join(a.out, f"song-{so:03d}.png"); ve(bars, so, r, q, p, a.nhan); print(p)


if __name__ == "__main__":
    main()
