#!/usr/bin/env python3
"""Vẽ các SÓNG BỊ KHOÁ (quy tắc B4/C2: pha hồi tạo đáy nông chưa tới 50% → sóng đó không BUY, đợi phá đỉnh).

Mỗi sóng bị khoá được phân loại theo diễn biến sau đó (tối đa 200 nến):
  A. giá về DISCOUNT (chạm 50%) trước khi phá đỉnh  → quy tắc thật sự làm bỏ cơ hội vào lệnh (vẽ hết)
  B. thân nến phá đỉnh luôn, không về discount      → quy tắc không ảnh hưởng
  C. thân nến đóng qua mốc cấu trúc trước            → đảo chiều
  D. hết ngày giao dịch mà chưa có gì (xu hướng được tính lại mỗi ngày)
Cách dùng: python3 tools/ve_song_khoa.py nen_M1.csv thu_muc_ra NHAN [--khung M15]
"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(__file__))
import smc_engine as eng
import backtest as bt
import vao_lenh_uu_tien as vl
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "DejaVu Sans"
TEN = {"A": "về discount trước khi phá đỉnh (bỏ lỡ)", "B": "phá đỉnh luôn", "C": "đảo chiều (đóng qua mốc cấu trúc)", "D": "hết ngày, không có gì"}


def phan_loai(D, r, het_ngay):
    for q in range(r["j"] + 1, min(len(D), r["j"] + 200, het_ngay(r["j"]))):
        if D[q].l <= r["mid"]:
            return "A", q
        if D[q].c > r["Tp"]:
            return "B", q
        if D[q].c < r["Bp"]:
            return "C", q
    return "D", min(len(D) - 1, r["j"] + 200, het_ngay(r["j"]) - 1)


def ve(ax, bars, so, r, kq, q_end):
    sg = 1 if r["side"] == "BUY" else -1
    P = lambda x: sg * x
    a = max(0, r["Bi"] - 4); b = min(len(bars), max(q_end, r["j"]) + 12)
    if b - a > 160:
        a = max(0, b - 160)
    for i in range(a, b):
        x = bars[i]; c = "#26a69a" if x.c >= x.o else "#ef5350"
        ax.plot([i, i], [x.l, x.h], color=c, lw=.9, zorder=3)
        ax.add_patch(plt.Rectangle((i - .32, min(x.o, x.c)), .64, max(abs(x.c - x.o), .01), color=c, zorder=4))
    Bp, Tp, mid, lo = P(r["Bp"]), P(r["Tp"]), P(r["mid"]), P(r["lo"])
    x0 = max(a, r["Bi"])
    hi_, lo_ = max(Bp, Tp), min(Bp, Tp)
    prem_lo, prem_hi = mid, hi_          # premium luôn là nửa trên, discount nửa dưới
    disc_lo, disc_hi = lo_, mid
    ax.add_patch(plt.Rectangle((x0, prem_lo), b - x0, prem_hi - prem_lo, color="#ffcdd2", alpha=.35, zorder=1))
    ax.add_patch(plt.Rectangle((x0, disc_lo), b - x0, disc_hi - disc_lo, color="#c8e6c9", alpha=.4, zorder=1))
    if r["Bi"] >= a:
        ax.annotate("", xy=(r["Ti"], Tp), xytext=(r["Bi"], Bp), arrowprops=dict(arrowstyle="-|>", color="#6a1b9a", lw=1.8))
    for y, c, ls, lab in [(Tp, "#f57f17", "--", "đỉnh" if sg > 0 else "đáy"), (mid, "#6a1b9a", "--", "50%"),
                          (Bp, "#6a1b9a", "-", "mốc CT"), (lo, "#ef6c00", "--", "đáy nông" if sg > 0 else "đỉnh nông")]:
        ax.plot([x0, b], [y, y], color=c, ls=ls, lw=1.1, zorder=5); ax.text(b + .5, y, lab, color=c, fontsize=7.5, va="center", fontweight="bold")
    ax.scatter([r["lo_i"]], [lo], s=60, color="#ef6c00", zorder=7, edgecolor="white")
    ax.axvline(r["j"], color="#ef6c00", ls=":", lw=1.3)
    ax.text(r["j"], ax.get_ylim()[1] if False else max(hi_, max(bars[i].h for i in range(a, b))), " khoá", color="#ef6c00",
            fontsize=8, fontweight="bold", va="top")
    if kq in ("A", "B", "C"):
        ax.axvline(q_end, color="#333", ls=":", lw=1.1)
    col = {"A": "#c62828", "B": "#2e7d32", "C": "#757575", "D": "#757575"}[kq]
    ax.set_title(f"#{so}  {r['side']} · khoá {bars[r['j']].t} · {TEN[kq]}", loc="left", fontsize=9.5, fontweight="bold", color=col)
    step = max(1, (b - a) // 6); ticks = list(range(a, b, step))
    ax.set_xticks(ticks); ax.set_xticklabels([bars[i].t[5:] for i in ticks], fontsize=7)
    ax.tick_params(axis="y", labelsize=7); ax.set_xlim(a - 1, b + 8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nen"); ap.add_argument("out"); ap.add_argument("nhan")
    ap.add_argument("--khung", default="M15", choices=["M1", "M5", "M15"])
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    bars = [eng.Bar(b.t[:16], b.o, b.h, b.l, b.c) for b in eng.load_csv(a.nen)]
    if a.khung != "M1":
        bars = bt.resample(bars, 5 if a.khung == "M5" else 15)
    import bisect
    st = bt.day_starts(bars) + [len(bars)]
    het_ngay = lambda j: st[bisect.bisect_right(st, j)]      # nến đầu ngày giao dịch kế tiếp (xu hướng tính lại mỗi ngày)
    ds = []
    for side, D in (("BUY", bars), ("SELL", bt.neg(bars))):
        kh = []
        vl.run(D, side, khoa=kh)
        for r in kh:
            kq, q = phan_loai(D, r, het_ngay); ds.append((r, kq, q))
    ds.sort(key=lambda x: x[0]["j"])
    dem = {k: sum(1 for _, kq, _ in ds if kq == k) for k in TEN}
    print(a.nhan, "sóng bị khoá:", len(ds), dem)
    A = [x for x in ds if x[1] == "A"]
    lines = [f"# Sóng bị khoá {a.nhan} (khung {a.khung})\n",
             f"Tổng {len(ds)} sóng bị khoá: " + ", ".join(f"{TEN[k]}: {v}" for k, v in dem.items()) + ".\n",
             "Chỉ vẽ nhóm A (về discount trước khi phá đỉnh) – đây là các sóng quy tắc mới làm BỎ LỠ cơ hội vào lệnh.\n",
             "Chú thích: mũi tên tím = sóng đẩy (mốc cấu trúc → đỉnh), chấm cam = đáy nông, vạch chấm cam = nến khoá sóng,"
             " vạch chấm đen = lúc giá chạm 50%.\n",
             "| # | Ảnh | Chiều | Khoá lúc | Đáy/đỉnh nông | 50% | Chạm 50% lúc |", "|---|---|---|---|---|---|---|"]
    for p in range(0, len(A), 6):
        nhom = A[p:p + 6]; ten = f"khoa-{p + 1:03d}-{p + len(nhom):03d}.png"
        fig, axs = plt.subplots(3, 2, figsize=(22, 15), squeeze=False)
        for k, ax in enumerate(axs.flat):
            if k >= len(nhom):
                ax.axis("off"); continue
            r, kq, q = nhom[k]; so = p + k + 1
            ve(ax, bars, so, r, kq, q)
            sg = 1 if r["side"] == "BUY" else -1
            lines.append(f"| {so} | {ten} | {r['side']} | {bars[r['j']].t} | {sg * r['lo']:.2f} | {sg * r['mid']:.2f} | {bars[q].t} |")
        fig.suptitle(f"XAUUSD {a.khung} {a.nhan} – sóng bị khoá rồi giá về discount: #{p + 1}–#{p + len(nhom)}", fontsize=14, fontweight="bold")
        plt.tight_layout(rect=(0, 0, 1, .97)); plt.savefig(os.path.join(a.out, ten), dpi=70); plt.close(fig)
    open(os.path.join(a.out, "danh-sach.md"), "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
