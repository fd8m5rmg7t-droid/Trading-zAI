#!/usr/bin/env python3
"""Sơ đồ dạng đường: tất cả các trường hợp bộ máy VÀO LỆNH (ví dụ xu hướng tăng – BUY; SELL lật ngược)."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "DejaVu Sans"
OR = "#f57f17"
def lab(ax, x, y, t, col="#d32f2f", **kw):
    ax.text(x, y, t, fontsize=9.5, fontweight="bold", color=col, bbox=dict(facecolor="#c5cae9", alpha=.85, edgecolor="none", pad=1.5), **kw)
def frame(ax, title, liq=False):
    ax.add_patch(plt.Rectangle((0, 110), 15, 10, color="#ffcdd2", alpha=.45, zorder=0))
    ax.add_patch(plt.Rectangle((0, 100), 15, 10, color="#c8e6c9", alpha=.5, zorder=0))
    ax.plot([0, 15], [110, 110], color="#e57373", lw=1); ax.text(15.1, 110, "0.5", fontsize=8, color="#e57373", va="center")
    ax.text(15.1, 120, "0", fontsize=8, color="#999", va="center"); ax.text(15.1, 100, "1", fontsize=8, color="#999", va="center")
    lab(ax, -.6, 98.2, "đáy 1"); lab(ax, 5.3, 121.2, "đỉnh")
    ax.set_title(title, loc="left", fontsize=11, fontweight="bold")
    ax.set_xlim(-1.5, 17); ax.set_ylim(95, 124); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_color("#ddd")
def push(ax, liq):
    P = [(0, 100), (2, 108), (3, 105.5), (6, 120)] if liq else [(0, 100), (6, 120)]
    ax.plot([p[0] for p in P], [p[1] for p in P], color=OR, lw=2)
    if liq:
        lab(ax, 3.2, 103.6, "đáy 2 hồi\nkhông đủ", ha="left")
def liqline(ax, y=105.5):
    ax.plot([3, 15], [y, y], color="#ef6c00", ls="--", lw=2); lab(ax, 15.3, y + .4, "thanh khoản", ha="left")
def zone(ax, lo, hi, t, col="#9575cd"):
    ax.add_patch(plt.Rectangle((1, lo), 13.5, hi - lo, color=col, alpha=.35, zorder=1)); ax.text(7.5, (lo + hi) / 2, t, fontsize=9, color="#4527a0", fontweight="bold", ha="center", va="center")
def path(ax, P):
    ax.plot([p[0] for p in P], [p[1] for p in P], color=OR, lw=2)
def entry(ax, x, y, t, dy=-3.2):
    ax.scatter([x], [y], marker="^", s=120, color="#1565c0", zorder=6)
    ax.annotate(t, xy=(x, y), xytext=(x + 1.6, y + dy), fontsize=9.5, fontweight="bold", color="#0d47a1",
                bbox=dict(facecolor="white", edgecolor="#1565c0", boxstyle="round,pad=0.25"), arrowprops=dict(arrowstyle="->", color="#1565c0"))
def bad(ax, x, y, t, dy=3):
    ax.annotate(t, xy=(x, y), xytext=(x + 1.4, y + dy), fontsize=9, fontweight="bold", color="#c62828", arrowprops=dict(arrowstyle="->", color="#c62828"))

fig, axs = plt.subplots(3, 3, figsize=(25, 21)); A = axs.flat
# 1 bình thường
ax = next(A); frame(ax, "1. Không có vùng nào: hồi chạm 50% → tạo đáy"); push(ax, False)
path(ax, [(6, 120), (10, 108.5), (11, 112)]); entry(ax, 10, 108.5, "nến xác nhận đáy\n→ BUY ở 1/2 râu")
# 2 FVG
ax = next(A); frame(ax, "2. FVG trong discount: chạm FVG → tạo đáy"); push(ax, False); zone(ax, 106, 108, "FVG")
path(ax, [(6, 120), (10, 106.8), (11, 111)]); entry(ax, 10, 106.8, "chạm FVG, tạo đáy\n→ BUY ở 1/2 râu")
# 3 POI
ax = next(A); frame(ax, "3. POI (có FVG hỗ trợ) trong discount, không có thanh khoản"); push(ax, False); zone(ax, 103, 104.8, "POI")
path(ax, [(6, 120), (10, 103.6), (11, 109)]); entry(ax, 10, 103.6, "chạm POI, tạo đáy\n→ BUY ở 1/2 râu")
# 4 TK trên POI
ax = next(A); frame(ax, "4. Thanh khoản nằm ngay TRÊN POI"); push(ax, True); liqline(ax); zone(ax, 103, 104.6, "POI")
path(ax, [(6, 120), (10, 104.2), (10.3, 106.3), (11.5, 110)]); entry(ax, 10, 104.2, "nến QUÉT thanh khoản\nvà râu chạm POI → BUY ngay\n(1/2 râu hoặc giá thanh khoản)", dy=-5)
# 5 POI trên TK
ax = next(A); frame(ax, "5. POI nằm TRÊN thanh khoản → bỏ POI"); push(ax, True); liqline(ax); zone(ax, 107, 108.6, "POI (bỏ qua)", col="#bdbdbd")
path(ax, [(6, 120), (9, 107.5), (9.3, 108.5), (10.5, 104.6), (10.8, 106.4), (12, 110)])
bad(ax, 9, 107.5, "chạm POI → không vào", dy=4); entry(ax, 10.5, 104.6, "nến QUÉT thanh khoản\n→ BUY ngay", dy=-4.5)
# 6 TK một mình
ax = next(A); frame(ax, "6. Chỉ có thanh khoản (trong discount)"); push(ax, True); liqline(ax)
path(ax, [(6, 120), (10, 104.6), (10.3, 106.4), (11.5, 110)]); entry(ax, 10, 104.6, "nến QUÉT thanh khoản\n(râu xuyên, thân đóng lại trên,\nrâu dài hơn thân) → BUY ngay", dy=-6.5)
# 7 đóng dưới TK một mình
ax = next(A); frame(ax, "7. Thân nến ĐÓNG CỬA dưới thanh khoản (không có POI)"); push(ax, True); liqline(ax)
path(ax, [(6, 120), (9.6, 104.8), (10.4, 103.2), (11.5, 108)])
bad(ax, 9.6, 104.8, "đóng cửa dưới thanh khoản\n= không phải quét", dy=6); entry(ax, 10.4, 103.2, "khai thác bình thường:\ntạo đáy → BUY ở 1/2 râu", dy=-4.5)
# 8 TK+POI, đóng dưới TK
ax = next(A); frame(ax, "8. Thanh khoản trên POI, thân nến đóng DƯỚI thanh khoản"); push(ax, True); liqline(ax); zone(ax, 101.5, 103.2, "POI")
path(ax, [(6, 120), (9.4, 104.6), (10.4, 102.2), (11.6, 108)])
bad(ax, 9.4, 104.6, "đóng cửa dưới thanh khoản\n→ bỏ kiểu thanh khoản, chờ POI", dy=6.5); entry(ax, 10.4, 102.2, "chạm POI, tạo đáy\n→ BUY ở 1/2 râu", dy=-4.5)
# 9 SL vùng trên → vùng dưới
ax = next(A); frame(ax, "9. Lệnh ở vùng trên bị DỪNG LỖ → vào tiếp vùng dưới"); push(ax, False); zone(ax, 106.5, 108.3, "FVG"); zone(ax, 101.5, 103.2, "POI")
path(ax, [(6, 120), (8.5, 107.2), (9.2, 109), (10.6, 102.3), (11.8, 109)])
entry(ax, 8.5, 107.2, "BUY 1 (FVG)", dy=5); ax.annotate("giá đóng cửa dưới điểm thấp nhất\n→ BUY 1 dừng lỗ", xy=(9.9, 105.5), xytext=(1.3, 113), fontsize=9, fontweight="bold", color="#c62828", arrowprops=dict(arrowstyle="->", color="#c62828"))
entry(ax, 10.6, 102.3, "BUY 2 (POI)", dy=-5)
fig.suptitle("TẤT CẢ các trường hợp bộ máy VÀO LỆNH – ví dụ xu hướng tăng (BUY). Xu hướng giảm (SELL): lật ngược.\n"
             "PnD đo từ mốc cấu trúc (đáy 1) đến đỉnh; mọi vùng phải nằm trong discount; vùng nào giá chạm trước thì ưu tiên.", fontsize=14, fontweight="bold")
plt.tight_layout(rect=(0, 0, 1, .95), h_pad=4, w_pad=2.5)
plt.savefig("examples/42-tat-ca-truong-hop-vao-lenh.png", dpi=80)
