#!/usr/bin/env python3
"""Vẽ xu hướng M15 của một ngày giao dịch, tìm lại từ nến đóng cửa ngày liền trước.
Cách dùng: python3 tools/ve_xu_huong_ngay.py 2026-10-22 duong/dan/XAUUSD_M15.csv"""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
import smc_engine as eng, backtest as bt
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "DejaVu Sans"
DAY = sys.argv[1] if len(sys.argv) > 1 else "2026-10-22"
m15 = [eng.Bar(b.t[:16], b.o, b.h, b.l, b.c) for b in eng.load_csv((sys.argv[2] if len(sys.argv) > 2 else "data/XAUUSD_M15_VN.csv") + "")]
starts = bt.day_starts(m15) + [len(m15)]
a = next(s for s in starts if m15[s].t >= DAY + " 04:00")
b = starts[starts.index(a) + 1]
seg = m15[a - 1:b]; r = eng.analyze(seg); n = len(seg)
fig, ax = plt.subplots(figsize=(24, 10))
col = {"UP": "#c8e6c9", "SIDE_UP": "#e8f5e9", "DOWN": "#ffcdd2", "SIDE_DOWN": "#ffebee", "UNCLEAR": "#eeeeee"}
for i in range(n):
    ax.axvspan(i - .5, i + .5, color=col[r.state[i]], lw=0, zorder=0)
    x = seg[i]; c = "#26a69a" if x.c >= x.o else "#ef5350"
    ax.plot([i, i], [x.l, x.h], color=c, lw=1.3, zorder=3)
    ax.add_patch(plt.Rectangle((i - .3, min(x.o, x.c)), .6, max(abs(x.c - x.o), .02), color=c, zorder=4))
ax.add_patch(plt.Rectangle((-.45, seg[0].l), .9, seg[0].h - seg[0].l, fill=False, ec="#000", lw=2, zorder=5))
ax.axhline(seg[0].c, color="#000", lw=1, ls=":", zorder=2)
ax.annotate(f"ĐIỂM BẮT ĐẦU\nnến đóng cửa ngày trước\n({seg[0].t[5:]}, đóng {seg[0].c:.2f})", xy=(0, seg[0].c), xytext=(3, seg[0].c),
            fontsize=9.5, fontweight="bold", va="center", arrowprops=dict(arrowstyle="->"))
nt = nb = 0
lab = {"m12": "", "break": " (phá vỡ)", "between": " (giữa 2 đỉnh/đáy)"}
for s in sorted(r.swings, key=lambda s: s.i):
    if s.kind == "T":
        nt += 1; ax.scatter([s.i], [s.price], marker="v", s=90, color="#f57f17", zorder=6)
        ax.text(s.i, s.price + 1.2, f"Đỉnh {nt}{lab[s.how]}\n{s.price:.2f}", ha="center", va="bottom", fontsize=8.5, color="#e65100", fontweight="bold")
    else:
        nb += 1; ax.scatter([s.i], [s.price], marker="^", s=90, color="#1565c0", zorder=6)
        ax.text(s.i, s.price - 1.2, f"Đáy {nb}{lab[s.how]}\n{s.price:.2f}", ha="center", va="top", fontsize=8.5, color="#0d47a1", fontweight="bold")
ymin = min(x.l for x in seg); ymax = max(x.h for x in seg)
# đường nét đứt nối các đỉnh/đáy theo thứ tự thời gian (dạng zigzag)
sw = sorted(r.swings, key=lambda s: s.i)
ax.plot([s.i for s in sw], [s.price for s in sw], color="#616161", lw=1.2, ls="--", zorder=5)
# khi xác nhận xu hướng: nối 2 đỉnh và 2 đáy dùng để kết luận
for i, t in r.events:
    if not t.startswith("Xác nhận"):
        continue
    used = [s for s in sw if s.conf <= i]
    tops = [s for s in used if s.kind == "T"][-2:]; bots = [s for s in used if s.kind == "B"][-2:]
    if len(tops) == 2:
        ax.plot([tops[0].i, tops[1].i], [tops[0].price, tops[1].price], color="#e65100", lw=2.6, ls=(0, (6, 3)), zorder=6)
    if len(bots) == 2:
        ax.plot([bots[0].i, bots[1].i], [bots[0].price, bots[1].price], color="#0d47a1", lw=2.6, ls=(0, (6, 3)), zorder=6)
    xs = [s.i for s in tops + bots]
    ax.text((min(xs) + max(xs)) / 2, (tops[-1].price + bots[-1].price) / 2 if tops and bots else ymax,
            t.replace("Xác nhận ", "XÁC NHẬN\n") + "\n(2 đỉnh + 2 đáy)", ha="center", va="center", fontsize=10, fontweight="bold",
            color="#c62828" if "GIẢM" in t else "#2e7d32",
            bbox=dict(facecolor="white", alpha=.85, edgecolor="#999", boxstyle="round,pad=0.3"), zorder=7)
for i, t in r.events:
    ax.axvline(i, color="#555", lw=.8, ls="--", zorder=1)
    ax.text(i + .15, ymax + 6, t, rotation=90, fontsize=8.5, va="top", color="#333")
# session no-trade windows
import datetime as dt
for i, x in enumerate(seg):
    if bt.blocked(x.t):
        ax.add_patch(plt.Rectangle((i - .5, ymin - 9), 1, 2.5, color="#757575", zorder=2))
ax.text(0, ymin - 10.5, "▬ giờ cấm giao dịch (±30' giờ mở phiên)", fontsize=9, color="#555", va="top")
ticks = list(range(0, n, 4)); ax.set_xticks(ticks); ax.set_xticklabels([seg[i].t[11:] for i in ticks], fontsize=8.5)
ax.set_ylim(ymin - 13, ymax + 8); ax.set_xlim(-1, n)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=col[k], label=v) for k, v in [("UP", "tăng – đang phá đỉnh"), ("SIDE_UP", "tăng – đi ngang"),
          ("DOWN", "giảm – đang phá đáy"), ("SIDE_DOWN", "giảm – đi ngang"), ("UNCLEAR", "chưa rõ xu hướng")]],
          loc="upper right", fontsize=9, ncol=5)
ax.set_title(f"XAUUSD M15 – ngày giao dịch {seg[1].t[:10]} (giờ VN): xu hướng tìm lại từ giá đóng cửa ngày liền trước"
             "  (nét đứt xám: nối đỉnh/đáy; nét đứt đậm: 2 đỉnh & 2 đáy dùng để xác nhận)",
             loc="left", fontsize=13, fontweight="bold")
plt.tight_layout(); plt.savefig(f"backtest/xauusd-m15-ngay-{DAY}.png", dpi=95)
print(seg[1].t, "→", seg[-1].t, n, "nến;", len(r.swings), "đỉnh/đáy"); [print(seg[i].t, t) for i, t in r.events]
