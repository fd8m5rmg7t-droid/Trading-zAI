#!/usr/bin/env python3
"""Sơ đồ dạng đường: tất cả các trường hợp bộ máy XÁC ĐỊNH XU HƯỚNG (đúng như tools/smc_engine.py đang làm).
Ra 3 ảnh: examples/43a (đầu ngày), 43b (chưa rõ xu hướng), 43c (đã có xu hướng)."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "DejaVu Sans"
OR = "#f57f17"; GR = "#2e7d32"; RD = "#c62828"; PU = "#6a1b9a"; BL = "#1565c0"


def frame(ax, title):
    ax.set_title(title, loc="left", fontsize=11.5, fontweight="bold")
    ax.set_xlim(-1.5, 16.5); ax.set_ylim(86, 124); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#ddd")


def path(ax, P, col=OR, lw=2.2, ls="-"):
    ax.plot([p[0] for p in P], [p[1] for p in P], color=col, lw=lw, ls=ls, zorder=3)


def pt(ax, x, y, t, up=True, col=RD):
    ax.scatter([x], [y], s=28, color=col, zorder=5)
    ax.text(x, y + (1.3 if up else -1.3), t, fontsize=9, fontweight="bold", color=col, ha="center",
            va="bottom" if up else "top", bbox=dict(facecolor="white", alpha=.85, edgecolor="none", pad=1), zorder=6)


def level(ax, y, x0, x1, t="", col="#9e9e9e", ls="--"):
    ax.plot([x0, x1], [y, y], color=col, ls=ls, lw=1.2, zorder=2)
    if t:
        ax.text(x1 + .2, y, t, fontsize=8.5, color=col, va="center", fontweight="bold")


def candle(ax, x, o, c, h, l):
    col = "#26a69a" if c >= o else "#ef5350"
    ax.plot([x, x], [l, h], color=col, lw=1.4, zorder=7)
    ax.add_patch(plt.Rectangle((x - .22, min(o, c)), .44, abs(c - o), color=col, zorder=8))


def note(ax, x, y, t, col=BL, dx=1.2, dy=3.0, ha="left"):
    ax.annotate(t, xy=(x, y), xytext=(x + dx, y + dy), fontsize=8.8, color=col, fontweight="bold", ha=ha,
                arrowprops=dict(arrowstyle="->", color=col), zorder=9,
                bbox=dict(facecolor="white", edgecolor=col, boxstyle="round,pad=0.25", alpha=.95))


def result(ax, t, col):
    ax.text(.5, .03, t, transform=ax.transAxes, ha="center", va="bottom", fontsize=10.5, fontweight="bold", color="white",
            bbox=dict(facecolor=col, edgecolor="none", boxstyle="round,pad=0.4"))


def pnd(ax, lo, hi, x0, x1):
    m = (lo + hi) / 2
    ax.add_patch(plt.Rectangle((x0, m), x1 - x0, hi - m, color="#ffcdd2", alpha=.35, zorder=0))
    ax.add_patch(plt.Rectangle((x0, lo), x1 - x0, m - lo, color="#c8e6c9", alpha=.45, zorder=0))
    level(ax, m, x0, x1, "50%", col="#e57373")


def save(fig, p, sup):
    fig.suptitle(sup, fontsize=15, fontweight="bold")
    plt.tight_layout(rect=(0, 0, 1, .95)); plt.savefig(p, dpi=75); plt.close(fig); print(p)


# ============================================================ A. ĐẦU NGÀY
fig, axs = plt.subplots(2, 2, figsize=(20, 15)); A = axs.flat
ax = next(A); frame(ax, "A1. Giá đi XUỐNG trước")
ax.axvline(0, color="#999", ls=":"); ax.text(0, 123, "nến đóng cửa\nngày hôm trước", fontsize=8.5, color="#666", ha="center", va="top")
path(ax, [(0, 112), (3, 100), (5.5, 107), (8.5, 94), (9.5, 97.5)])
pt(ax, 0, 112, "Đỉnh 1 (râu nến\nđóng cửa hôm trước)"); pt(ax, 3, 100, "Đáy 1 (cách 1)", up=False)
pt(ax, 5.5, 107, "Đỉnh 2 = cao nhất\ngiữa Đáy 1 và Đáy 2"); pt(ax, 8.5, 94, "Đáy 2", up=False)
level(ax, 100, 3, 13, "Đáy 1"); level(ax, 112, 0, 13, "Đỉnh 1")
note(ax, 7.2, 99.5, "thân nến đóng dưới Đáy 1\n→ bắt đầu tìm Đáy 2", dx=2.2, dy=6)
note(ax, 9.5, 97.5, "nến xác nhận Đáy 2 (cách 1)", dx=1.0, dy=-6, col=RD)
result(ax, "Xác nhận GIẢM khi Đáy 2 được xác nhận", RD)

ax = next(A); frame(ax, "A2. Giá đi LÊN trước (ngược lại A1)")
ax.axvline(0, color="#999", ls=":"); ax.text(0, 88, "nến đóng cửa\nngày hôm trước", fontsize=8.5, color="#666", ha="center", va="bottom")
path(ax, [(0, 96), (3, 108), (5.5, 101), (8.5, 114), (9.5, 110.5)])
pt(ax, 0, 96, "Đáy 1 (râu nến\nđóng cửa hôm trước)", up=False); pt(ax, 3, 108, "Đỉnh 1 (cách 1)")
pt(ax, 5.5, 101, "Đáy 2 = thấp nhất\ngiữa Đỉnh 1 và Đỉnh 2", up=False); pt(ax, 8.5, 114, "Đỉnh 2")
level(ax, 108, 3, 13, "Đỉnh 1"); level(ax, 96, 0, 13, "Đáy 1")
note(ax, 7.2, 108.5, "thân nến đóng trên Đỉnh 1\n→ bắt đầu tìm Đỉnh 2", dx=2.2, dy=-8)
result(ax, "Xác nhận TĂNG khi Đỉnh 2 được xác nhận", GR)

ax = next(A); frame(ax, "A3. Râu vượt Đỉnh 1 nhưng THÂN chưa đóng qua (trường hợp 2)")
path(ax, [(0, 110), (3, 100), (5.5, 108.5), (8.5, 94), (9.5, 97.5)])
candle(ax, 5.5, 107, 108.5, 112.5, 106.5)
pt(ax, 0, 110, "Đỉnh 1"); pt(ax, 3, 100, "Đáy 1", up=False); pt(ax, 8.5, 94, "Đáy 2", up=False)
level(ax, 110, 0, 13, "Đỉnh 1"); level(ax, 100, 3, 13, "Đáy 1")
note(ax, 5.5, 112.5, "chỉ râu chọc qua, thân đóng dưới Đỉnh 1\n→ KHÔNG tính là phá", dx=1.5, dy=4, col=PU)
result(ax, "Vẫn xác nhận GIẢM khi Đáy 2 được xác nhận", RD)

ax = next(A); frame(ax, "A4. Quay lên đóng THÂN trên Đỉnh 1 trước khi phá Đáy 1")
path(ax, [(0, 110), (3, 100), (6, 114), (8, 108), (10, 117)])
pt(ax, 0, 110, "Đỉnh 1"); pt(ax, 3, 100, "Đáy 1", up=False)
level(ax, 110, 0, 13, "Đỉnh 1"); level(ax, 100, 3, 13, "Đáy 1")
candle(ax, 5.2, 108.8, 111.5, 112, 108.5)
note(ax, 5.2, 111.5, "thân đóng trên Đỉnh 1\n(chưa phá Đáy 1)", dx=-6.2, dy=4, col=PU)
note(ax, 8, 108, "từ đây tìm đỉnh/đáy theo cách 1,\nĐỉnh 1 và Đáy 1 là 2 điểm đầu\n→ xét theo nhóm B", dx=1.2, dy=-12)
result(ax, "CHƯA RÕ xu hướng → chuyển sang nhóm B", "#757575")
save(fig, "examples/43a-xu-huong-dau-ngay.png", "A. XÁC ĐỊNH XU HƯỚNG ĐẦU NGÀY (bắt đầu từ nến đóng cửa ngày hôm trước)")

# ============================================================ B. CHƯA RÕ XU HƯỚNG (đỉnh/đáy theo cách 1)
fig, axs = plt.subplots(2, 3, figsize=(27, 15)); A = axs.flat
ax = next(A); frame(ax, "B1. Đỉnh thấp hơn → phá đáy → đáy thấp hơn")
path(ax, [(0, 112), (3, 100), (6, 107), (9, 93), (10, 96.5)])
pt(ax, 0, 112, "Đỉnh A"); pt(ax, 3, 100, "Đáy A", up=False); pt(ax, 6, 107, "Đỉnh B\n(thấp hơn)"); pt(ax, 9, 93, "Đáy B\n(thấp hơn)", up=False)
level(ax, 100, 3, 13, "Đáy A"); pnd(ax, 100, 112, 0, 4)
note(ax, 10, 96.5, "nến xác nhận Đáy B (cách 1)", dx=.8, dy=-6, col=RD)
candle(ax, 7.6, 101.5, 98.0, 102, 97.5)
note(ax, 7.6, 98.0, "THÂN nến đóng\ndưới Đáy A", dx=-6.5, dy=-6, col=PU)
note(ax, 6, 107, "Đỉnh B hồi chạm 50%\n→ là MỐC CẤU TRÚC", dx=2.5, dy=6, col=PU)
result(ax, "Xác nhận GIẢM khi Đáy B được xác nhận", RD)

ax = next(A); frame(ax, "B2. Như B1 nhưng Đỉnh B hồi KHÔNG tới 50%")
path(ax, [(0, 112), (3, 100), (5.5, 104), (9, 93), (10, 96.5)])
pt(ax, 0, 112, "Đỉnh A = MỐC CẤU TRÚC", col=PU); pt(ax, 3, 100, "Đáy A", up=False); pt(ax, 9, 93, "Đáy B", up=False)
pnd(ax, 100, 112, 0, 4)
level(ax, 104, 5.5, 13, "THANH KHOẢN", col="#ef6c00")
note(ax, 5.5, 104, "Đỉnh B hồi không đủ 50%\n→ chỉ là thanh khoản", dx=2.0, dy=7, col="#ef6c00")
result(ax, "GIẢM; đảo chiều/PnD tính từ Đỉnh A", RD)

ax = next(A); frame(ax, "B3. Thân phá đỉnh trước → đáy cao hơn (cách B)")
path(ax, [(0, 108), (3, 98), (6, 116), (8.5, 105), (9.5, 108.5)])
pt(ax, 0, 108, "Đỉnh A"); pt(ax, 3, 98, "Đáy A", up=False); pt(ax, 6, 116, "Đỉnh mới = cao nhất\ngiữa Đáy A và Đáy B")
pt(ax, 8.5, 105, "Đáy B (cao hơn)", up=False)
level(ax, 108, 0, 13, "Đỉnh A"); pnd(ax, 98, 116, 3, 7)
note(ax, 4.6, 108.5, "thân nến đóng\ntrên Đỉnh A", dx=-5.5, dy=5, col=PU)
note(ax, 9.5, 108.5, "nến xác nhận Đáy B (cách 1)", dx=.6, dy=6, col=GR)
result(ax, "Xác nhận TĂNG khi Đáy B được xác nhận", GR)

ax = next(A); frame(ax, "B4. Như B3 nhưng Đáy B hồi KHÔNG tới 50%")
path(ax, [(0, 108), (3, 98), (6, 116), (8.5, 109), (9.5, 112)])
pt(ax, 0, 108, "Đỉnh A"); pt(ax, 3, 98, "Đáy A = MỐC CẤU TRÚC", up=False, col=PU); pt(ax, 6, 116, "Đỉnh mới")
pnd(ax, 98, 116, 3, 7)
level(ax, 109, 8.5, 13, "THANH KHOẢN", col="#ef6c00")
note(ax, 8.5, 109, "Đáy B hồi không đủ 50%\n→ chỉ là thanh khoản", dx=1.5, dy=-9, col="#ef6c00")
result(ax, "TĂNG; đảo chiều/PnD tính từ Đáy A", GR)

ax = next(A); frame(ax, "B5. Đỉnh thấp hơn nhưng CHƯA phá đáy (ví dụ 16/09)")
path(ax, [(0, 112), (3, 100), (6, 107), (8.5, 102), (10.5, 106), (12, 101.5)])
pt(ax, 0, 112, "Đỉnh A"); pt(ax, 3, 100, "Đáy A", up=False); pt(ax, 6, 107, "Đỉnh B (thấp hơn)"); pt(ax, 8.5, 102, "đáy cao hơn", up=False)
level(ax, 100, 3, 14, "Đáy A"); level(ax, 112, 0, 14, "Đỉnh A")
note(ax, 10.5, 106, "không phá Đáy A,\nkhông đóng thân trên Đỉnh A", dx=-1, dy=8, col="#757575")
result(ax, "Vẫn CHƯA RÕ → chờ tiếp (đi ngang)", "#757575")

ax = axs.flat[5]; ax.axis("off")
ax.text(0, .95, "Ghi chú nhóm B", fontsize=13, fontweight="bold", va="top")
ax.text(0, .85, "• Đỉnh/đáy luôn tìm theo CÁCH 1 (nến có thân đóng\n   qua low/high của nến liền trước), đỉnh – đáy xen kẽ.\n"
        "• Hai chiều KHÔNG đối xứng (bạn đã chọn):\n"
        "   – GIẢM: đỉnh thấp hơn, thân phá đáy, rồi đáy thấp hơn được xác nhận.\n"
        "   – TĂNG: thân phá đỉnh trước, rồi đáy cao hơn được xác nhận.\n"
        "• Khi xác nhận xu hướng, kiểm tra pha hồi:\n"
        "   hồi chạm 50% → điểm đó là MỐC CẤU TRÚC;\n"
        "   không chạm 50% → điểm đó chỉ là THANH KHOẢN.\n"
        "• Chưa thỏa B1–B4 → vẫn CHƯA RÕ, không vào lệnh.\n\n"
        "• \"Phá\" luôn là THÂN nến đóng qua (râu không tính),\n"
        "   cả chiều tăng lẫn chiều giảm (xác nhận 24/11).",
        fontsize=11, va="top", linespacing=1.5)
save(fig, "examples/43b-xu-huong-chua-ro.png", "B. KHI CHƯA RÕ XU HƯỚNG (sau A4, sau dấu hiệu đảo chiều, hoặc đang đi ngang)")

# ============================================================ C. ĐÃ CÓ XU HƯỚNG (ví dụ TĂNG; GIẢM làm ngược lại)
fig, axs = plt.subplots(2, 2, figsize=(20, 15)); A = axs.flat
ax = next(A); frame(ax, "C1. Tiếp diễn: thân đóng trên đỉnh, hồi đủ 50%")
path(ax, [(0, 98), (3, 110), (5.5, 103.5), (8.5, 118), (9.5, 115)])
pt(ax, 0, 98, "mốc cấu trúc cũ", up=False, col="#757575"); pt(ax, 3, 110, "Đỉnh T"); pt(ax, 8.5, 118, "Đỉnh mới")
pt(ax, 5.5, 103.5, "đáy mới = thấp nhất giữa\nĐỉnh T và Đỉnh mới\n→ MỐC CẤU TRÚC MỚI", up=False, col=PU)
pnd(ax, 98, 110, 0, 4.5); level(ax, 110, 3, 13, "Đỉnh T")
note(ax, 7, 110.5, "thân đóng trên Đỉnh T\n→ quét tìm đỉnh mới", dx=3.0, dy=3.5)
note(ax, 9.5, 115, "nến xác nhận đỉnh (cách 1):\nđỉnh mới = râu cao nhất từ\nnến phá vỡ đến nến xác nhận", dx=.5, dy=-17, col=RD)
result(ax, "Vẫn TĂNG, mốc cấu trúc dời lên", GR)

ax = next(A); frame(ax, "C2. Tiếp diễn nhưng pha hồi KHÔNG tới 50%")
path(ax, [(0, 98), (3, 110), (5.5, 106.5), (8.5, 118), (9.5, 115)])
pt(ax, 0, 98, "MỐC CẤU TRÚC (giữ nguyên)", up=False, col=PU); pt(ax, 3, 110, "Đỉnh T"); pt(ax, 8.5, 118, "Đỉnh mới")
pnd(ax, 98, 110, 0, 4.5); level(ax, 106.5, 5.5, 13, "THANH KHOẢN", col="#ef6c00")
note(ax, 5.5, 106.5, "hồi không đủ 50%\n→ chỉ là thanh khoản", dx=1.5, dy=-11, col="#ef6c00")
ax.annotate("", xy=(8.5, 118), xytext=(0, 98), arrowprops=dict(arrowstyle="-|>", color=PU, lw=1.5, ls="--"))
ax.text(1.5, 115, "sóng đẩy tiếp theo / PnD\nđo từ mốc cấu trúc → đỉnh mới", fontsize=9, color=PU, fontweight="bold")
result(ax, "Vẫn TĂNG, mốc cấu trúc KHÔNG đổi", GR)

ax = next(A); frame(ax, "C3. Đi ngang: không đóng thân qua Đỉnh T, cũng không qua mốc cấu trúc")
path(ax, [(0, 98), (3, 110), (5, 102), (7, 109), (9, 101), (11, 108.5), (12.5, 104)])
pt(ax, 0, 98, "MỐC CẤU TRÚC", up=False, col=PU); pt(ax, 3, 110, "Đỉnh T")
level(ax, 110, 3, 14, "Đỉnh T"); level(ax, 98, 0, 14, "mốc cấu trúc", col=PU)
note(ax, 9, 101, "đỉnh/đáy nhỏ bên trong\nkhông có ý nghĩa", dx=.5, dy=-9, col="#757575")
result(ax, "Vẫn giữ xu hướng TĂNG (đang hồi / đi ngang)", GR)

ax = next(A); frame(ax, "C4. Thân nến đóng DƯỚI mốc cấu trúc → dấu hiệu đảo chiều")
path(ax, [(0, 98), (3, 110), (6.5, 95), (8, 99)])
pt(ax, 0, 98, "MỐC CẤU TRÚC", up=False, col=PU); pt(ax, 3, 110, "Đỉnh T → điểm đầu\ncủa nhóm B")
level(ax, 98, 0, 14, "mốc cấu trúc", col=PU)
candle(ax, 6, 99.5, 96.5, 100, 96)
note(ax, 6, 96.5, "thân đóng dưới mốc cấu trúc\n(đáy nông = thanh khoản thì KHÔNG tính)", dx=1.3, dy=-7, col=RD)
note(ax, 8, 99, "tìm đỉnh/đáy theo cách 1\n→ xác nhận lại theo B1–B5", dx=1.2, dy=7)
result(ax, "CHƯA RÕ xu hướng → chuyển sang nhóm B", "#757575")
save(fig, "examples/43c-xu-huong-dang-co.png", "C. KHI ĐÃ CÓ XU HƯỚNG (ví dụ TĂNG; xu hướng GIẢM làm ngược lại)")
