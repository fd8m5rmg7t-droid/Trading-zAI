#!/usr/bin/env python3
"""Vẽ TẤT CẢ lệnh M15 (kết quả của vao_lenh_uu_tien.py --khung M15) để người dùng duyệt từng lệnh.
Mỗi ảnh 6 lệnh (3 hàng x 2 cột), lệnh được đánh số; kèm file danh-sach.md liệt kê từng lệnh.

Cách dùng: python3 tools/ve_lenh_m15.py nen_M1.csv ket_qua_M15.csv thu_muc_ra NHAN
  (nến M1 sẽ được gộp thành M15 đúng như lúc chạy backtest, để chỉ số nến khớp nhau)
"""
import os, sys, csv
sys.path.insert(0, os.path.dirname(__file__))
import smc_engine as eng
import backtest as bt
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "DejaVu Sans"

TEN = {"fvg": "FVG", "poi": "POI", "quet-liq": "Quét thanh khoản", "quet-liq+poi": "Quét TK + râu chạm POI",
       "normal": "Bình thường (chạm 50%)"}
MOI_ANH = 6


def ve_lenh(ax, bars, idx, so, r):
    f = lambda k: float(r[k]); sell = r["side"] == "SELL"
    ws, wt = int(r["song_bat_dau_i"]), int(r["dinh_cu_i"]); ji, jo = idx[r["t_in"]], idx[r["t_out"]]
    a = max(0, min(ws, wt) - 6, ji - 110); b = min(len(bars), jo + 8)
    for i in range(a, b):
        x = bars[i]; c = "#26a69a" if x.c >= x.o else "#ef5350"
        ax.plot([i, i], [x.l, x.h], color=c, lw=.9, zorder=3)
        ax.add_patch(plt.Rectangle((i - .32, min(x.o, x.c)), .64, max(abs(x.c - x.o), .01), color=c, zorder=4))
    st, T, mid = f("song_bat_dau"), f("T"), f("mid")
    hi, lo = max(st, T), min(st, T); x0 = max(a, min(ws, wt))
    # PnD của sóng đẩy: premium đỏ nhạt, discount xanh nhạt
    ax.add_patch(plt.Rectangle((x0, mid), b - x0, hi - mid, color="#ffcdd2", alpha=.35, zorder=1))
    ax.add_patch(plt.Rectangle((x0, lo), b - x0, mid - lo, color="#c8e6c9", alpha=.4, zorder=1))
    if ws >= a:
        ax.annotate("", xy=(wt, T), xytext=(ws, st), arrowprops=dict(arrowstyle="-|>", color="#6a1b9a", lw=1.8))
    kieu = r["kieu"]
    if r.get("vung_tren"):
        zt, zb = float(r["vung_tren"]), float(r["vung_duoi"])
        ax.add_patch(plt.Rectangle((x0, zb), b - x0, max(zt - zb, .05), color="#7e57c2", alpha=.4, zorder=2))
        ax.text(b + .5, (zt + zb) / 2, "FVG" if kieu == "fvg" else "POI", color="#4527a0", fontsize=8, fontweight="bold", va="center")
    if r.get("tk"):
        y = float(r["tk"])
        ax.plot([x0, b], [y, y], color="#ef6c00", lw=1.8, ls="--", zorder=5)
        ax.text(b + .5, y, "TK", color="#ef6c00", fontsize=8, fontweight="bold", va="center")
    for y, c, ls, lab in [(T, "#f57f17", "--", "TP1"), (mid, "#6a1b9a", "--", "50%"),
                          (f("entry"), "#1565c0", "-", "vào"),
                          (f("low"), "#c62828", "--", "đỉnh" if sell else "đáy"), (f("hard_sl"), "#6a1b9a", ":", "SL cứng")]:
        ax.plot([x0, b], [y, y], color=c, ls=ls, lw=1.1, zorder=5); ax.text(b + .5, y, lab, color=c, fontsize=7.5, va="center")
    ax.plot([ji], [f("entry")], marker="v" if sell else "^", color="#1565c0", ms=11, zorder=7, mec="white")
    ax.axvline(ji, color="#1565c0", ls=":", lw=1); ax.axvline(jo, color="#333", ls=":", lw=1)
    R = f("R"); col = "#2e7d32" if R > .05 else ("#c62828" if R < -.05 else "#555")
    ex = r["exit"].replace("đóng cửa dưới điểm thấp nhất", "đóng cửa qua đỉnh" if sell else "đóng cửa dưới đáy")
    ax.set_title(f"#{so}  {r['side']} · {TEN.get(kieu, kieu)} · vào {r['t_in']} → {ex}  ({R:+.2f}R)",
                 loc="left", fontsize=9.5, fontweight="bold", color=col)
    step = max(1, (b - a) // 6); ticks = list(range(a, b, step))
    ax.set_xticks(ticks); ax.set_xticklabels([bars[i].t[5:] for i in ticks], fontsize=7)
    ax.tick_params(axis="y", labelsize=7); ax.set_xlim(a - 1, b + 9)
    return ex, R


def main():
    nen, kq, out, nhan = sys.argv[1:5]
    os.makedirs(out, exist_ok=True)
    bars = bt.resample([eng.Bar(b.t[:16], b.o, b.h, b.l, b.c) for b in eng.load_csv(nen)], 15)
    idx = {b.t: i for i, b in enumerate(bars)}
    rows = list(csv.DictReader(open(kq)))
    ds = [f"# Lệnh M15 {nhan} – danh sách để duyệt\n",
          "Mỗi ảnh 6 lệnh. Chú thích: mũi tên tím = sóng đẩy (từ mốc cấu trúc tới đỉnh/đáy cũ), nền đỏ nhạt = premium,"
          " xanh nhạt = discount, khối tím = POI/FVG, cam đứt = thanh khoản (TK), xanh đậm = điểm vào, đỏ đứt = đáy/đỉnh,"
          " tím chấm = SL cứng, cam = TP1 (đỉnh/đáy cũ). Vạch chấm xanh = lúc vào, vạch chấm đen = lúc ra.\n",
          "| # | Ảnh | Chiều | Kiểu | Vào | Ra | Thoát | R |", "|---|---|---|---|---|---|---|---|"]
    for p in range(0, len(rows), MOI_ANH):
        nhom = rows[p:p + MOI_ANH]
        fig, axs = plt.subplots(3, 2, figsize=(22, 15), squeeze=False)
        ten = f"lenh-{p + 1:03d}-{p + len(nhom):03d}.png"
        for k, ax in enumerate(axs.flat):
            if k >= len(nhom):
                ax.axis("off"); continue
            so = p + k + 1; r = nhom[k]
            ex, R = ve_lenh(ax, bars, idx, so, r)
            ds.append(f"| {so} | {ten} | {r['side']} | {TEN.get(r['kieu'], r['kieu'])} | {r['t_in']} | {r['t_out']} | {ex} | {R:+.2f} |")
        fig.suptitle(f"XAUUSD M15 {nhan} – lệnh #{p + 1}–#{p + len(nhom)}", fontsize=14, fontweight="bold")
        plt.tight_layout(rect=(0, 0, 1, .97)); plt.savefig(os.path.join(out, ten), dpi=70); plt.close(fig)
    Rs = [float(r["R"]) for r in rows]
    ds.append(f"\nTổng: {len(rows)} lệnh, {sum(Rs):+.2f}R.")
    open(os.path.join(out, "danh-sach.md"), "w").write("\n".join(ds) + "\n")
    print(out, len(rows), "lệnh")


if __name__ == "__main__":
    main()
