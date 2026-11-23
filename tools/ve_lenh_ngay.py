#!/usr/bin/env python3
"""Vẽ BƯỚC vào lệnh – dừng lỗ – chốt lời (khai thác pha đẩy, M15/M15) cho ngày 22/10/2026."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import smc_engine as eng
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "DejaVu Sans"
CSV = sys.argv[1]
bars = [eng.Bar(b.t[:16], b.o, b.h, b.l, b.c) for b in eng.load_csv(CSV)]
a0 = next(i for i, b in enumerate(bars) if b.t == "2026-10-22 13:15"); a1 = next(i for i, b in enumerate(bars) if b.t == "2026-10-22 22:30")
seg = bars[a0:a1 + 1]; X = lambda t: next(i for i, b in enumerate(seg) if b.t.endswith(t))
fig, ax = plt.subplots(figsize=(24, 12))
def zone(x0, x1, col, lab):
    ax.axvspan(x0 - .5, x1 + .5, color=col, zorder=0); ax.text((x0 + x1) / 2, 4129, lab, ha="center", fontsize=11, fontweight="bold", color="#333")
zone(0, X("13:45"), "#e8f5e9", "pha đẩy 1"); zone(X("13:45") + 1, X("14:15"), "#e3f2fd", "pha hồi 1"); zone(X("14:15") + 1, X("19:45"), "#e8f5e9", "pha đẩy 2")
zone(X("19:45") + 1, X("20:45"), "#e3f2fd", "pha hồi 2"); zone(X("20:45") + 1, len(seg) - 1, "#e8f5e9", "pha đẩy 3")
hl = {X(t) for t in ("14:15", "14:30", "15:00", "17:45", "19:15", "20:00", "20:45", "21:00")}
for i, x in enumerate(seg):
    c = "#26a69a" if x.c >= x.o else "#ef5350"
    ax.plot([i, i], [x.l, x.h], color=c, lw=1.4, zorder=3)
    ax.add_patch(plt.Rectangle((i - .32, min(x.o, x.c)), .64, max(abs(x.c - x.o), .02), color=c, zorder=4, ec="#000" if i in hl else c, lw=1.5 if i in hl else 0))
def hline(y, x0, x1, col, ls, lab, va="center", lw=1.6):
    ax.plot([x0, x1], [y, y], color=col, ls=ls, lw=lw, zorder=5); ax.text(x1 + .2, y, lab, color=col, fontsize=9.5, fontweight="bold", va=va)
# ---- LỆNH 1 (pha hồi 1)
t, cf, fill, be, tp1, tp2 = X("14:15"), X("14:30"), X("15:00"), X("17:45"), X("19:15"), X("20:00")
top = seg[t].h; body = max(seg[t].o, seg[t].c); entry = (top + body) / 2
hline(4095.19, 0, X("19:45"), "#6a1b9a", "--", "50% pha đẩy 1 = 4095.19")
hline(top, t, tp2, "#c62828", "--", f"điểm cao nhất {top:.2f} (mốc dừng lỗ)", "center")
hline(top + 3, t, tp2, "#6a1b9a", ":", f"SL cứng {top+3:.2f} (+3 giá)", "center")
hline(entry, t, tp2, "#1565c0", "-", f"SELL {entry:.2f} (1/2 râu trên nến 14:15)", "top", 2.2)
hline(4066.575, X("13:45"), tp2, "#f57f17", "--", "đáy cũ 4066.57 = TP1", "top")
def note(x, y, txt, dx, dy, col="#333"):
    ax.annotate(txt, xy=(x, y), xytext=(x + dx, y + dy), fontsize=9.5, fontweight="bold", color=col, ha="center",
                arrowprops=dict(arrowstyle="->", color=col), bbox=dict(facecolor="white", alpha=.85, edgecolor=col, boxstyle="round,pad=0.25"), zorder=8)
note(t, top, "① 14:15: pha hồi 1 chạm 50%,\nnến có điểm CAO NHẤT", -3, 8, "#c62828")
note(cf, seg[cf].c, "② 14:30: nến xác nhận ĐỈNH\n(thân đóng dưới low nến trước)\n→ đặt lệnh chờ SELL", 2.5, -14, "#333")
note(fill, entry, "③ 15:00: giá hồi lên chạm\n1/2 râu → KHỚP SELL", 3.5, 10, "#1565c0")
note(be, seg[be].c, "④ 17:45: giá tạo ĐÁY CAO HƠN đáy cũ\n(chưa chạm đáy cũ) → dời SL về điểm vào", -2, -14, "#6a1b9a")
note(tp1, 4066.575, "⑤ 19:15: chạm đáy cũ\n→ CHỐT 1/2", -3, -9, "#f57f17")
note(tp2, seg[tp2].c, "⑥ 20:00: phá đáy cũ, nến xác nhận\nĐÁY MỚI 4057.30 → CHỐT 1/2 còn lại\n(tổng +5.43R)", 0, 13, "#2e7d32")
# ---- LỆNH 2 (pha hồi 2) – không khớp
t2, cf2 = X("20:45"), X("21:00"); top2 = seg[t2].h; e2 = (top2 + max(seg[t2].o, seg[t2].c)) / 2
hline(4079.94, X("19:45"), len(seg) - 1, "#6a1b9a", "--", "50% pha đẩy 2 = 4079.94")
hline(e2, t2, len(seg) - 1, "#1565c0", "-", f"SELL chờ {e2:.2f}", "bottom", 2)
note(t2, top2, "⑦ 20:45: pha hồi 2 chạm 50%,\nnến có điểm cao nhất 4091.55", 5, 24, "#c62828")
note(cf2, seg[cf2].c, "⑧ 21:00: xác nhận đỉnh → đặt SELL chờ 4089.73\n⑨ giá KHÔNG hồi về điểm vào, chạm đáy 4057.30\n→ BỎ LỆNH", 2.5, -24, "#555")
ticks = list(range(0, len(seg), 2)); ax.set_xticks(ticks); ax.set_xticklabels([seg[i].t[11:] for i in ticks], fontsize=9)
ax.set_xlim(-1, len(seg) + 10); ax.set_ylim(4040, 4132)
ax.set_title("XAUUSD M15 – 22/10/2026: khai thác PHA ĐẨY (SELL, xu hướng giảm) – vào lệnh, dừng lỗ, chốt lời (M15 vừa xác định vừa vào lệnh)", loc="left", fontsize=13, fontweight="bold")
plt.tight_layout(); plt.savefig("backtest/lenh-2026-10-22.png", dpi=85); print("ok", entry, e2)
