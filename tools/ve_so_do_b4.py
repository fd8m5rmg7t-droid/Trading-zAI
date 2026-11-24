#!/usr/bin/env python3
"""Sơ đồ các trường hợp xảy ra SAU trường hợp B4 (xác nhận TĂNG nhưng Đáy B hồi không tới 50% → Đáy B là thanh khoản).
Đúng như bộ máy đang làm (smc_engine.py + vao_lenh_uu_tien.py). Ra examples/44-sau-truong-hop-b4.png"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ve_so_do_xu_huong import frame, path, pt, level, candle, note, result, pnd, OR, GR, RD, PU, BL

BASE = [(0, 108), (3, 98), (6, 116), (8.5, 109), (9.5, 112)]


def base(ax, title):
    frame(ax, title); path(ax, BASE)
    pt(ax, 0, 108, "Đỉnh A"); pt(ax, 3, 98, "Đáy A = MỐC CẤU TRÚC", up=False, col=PU); pt(ax, 6, 116, "Đỉnh mới")
    pt(ax, 8.5, 109, "Đáy B", up=False, col="#ef6c00")
    pnd(ax, 98, 116, 3, 15)
    level(ax, 109, 8.5, 15, "TK (Đáy B)", col="#ef6c00"); level(ax, 98, 3, 15, "mốc cấu trúc", col=PU)
    ax.axvline(9.5, color="#999", ls=":", lw=1); ax.text(9.5, 87, "xác nhận\nTĂNG", fontsize=8, color="#666", ha="center", va="bottom")


fig, axs = plt.subplots(2, 3, figsize=(27, 15)); A = axs.flat
ax = next(A); base(ax, "1. Đi tiếp lên: thân đóng trên Đỉnh mới")
path(ax, [(9.5, 112), (11, 117.5), (12.5, 121), (13.2, 119.5)]); pt(ax, 12.5, 121, "đỉnh mới 2")
note(ax, 11, 117, "thân đóng trên Đỉnh mới\n→ tiếp diễn (như C1/C2)", dx=-8.5, dy=4)
note(ax, 8.5, 109, "đáy giữa 2 đỉnh vẫn là Đáy B,\nvẫn không tới 50% → vẫn là TK;\nmốc cấu trúc vẫn là Đáy A", dx=.8, dy=-13, col="#ef6c00")
result(ax, "Vẫn TĂNG – KHÔNG vào lệnh (giá chưa về discount)", GR)

ax = next(A); base(ax, "2. Quét Đáy B nhưng vẫn ở PREMIUM")
path(ax, [(9.5, 112), (10.6, 110)]); candle(ax, 11, 110, 110.6, 111, 107.8); path(ax, [(11.4, 110.6), (13, 114)])
note(ax, 11, 107.8, "râu quét Đáy B, thân đóng lại trên\n(vẫn trên 50%)", dx=-1.5, dy=-11, col="#ef6c00")
result(ax, "KHÔNG vào lệnh: thanh khoản ở premium", "#757575")

ax = next(A); base(ax, "3. Về DISCOUNT (chạm 50%) → tìm vùng vào lệnh")
path(ax, [(9.5, 112), (12, 103.5), (13, 108)])
ax.add_patch(plt.Rectangle((3.5, 102.5), 11.5, 1.8, color="#9575cd", alpha=.35, zorder=1)); ax.text(5, 103.4, "POI / FVG / TK trong discount", fontsize=8.5, color="#4527a0", fontweight="bold", va="center")
ax.scatter([12], [103.5], marker="^", s=130, color=BL, zorder=8)
note(ax, 12, 103.5, "vào lệnh theo 9 trường hợp\n(ảnh 42); không có vùng →\nchạm 50%, tạo đáy, BUY 1/2 râu", dx=-1.5, dy=-14)
result(ax, "VÀO LỆNH – sóng đo từ Đáy A → Đỉnh mới", GR)

ax = next(A); base(ax, "4. Thân đóng dưới Đáy B (chưa tới mốc cấu trúc)")
path(ax, [(9.5, 112), (10.8, 108.5)]); candle(ax, 11.2, 109.6, 106.8, 110, 106.4); path(ax, [(11.6, 106.8), (12.5, 105.5), (13.5, 109)])
note(ax, 11.2, 106.8, "thân đóng dưới Đáy B\n= KHÔNG phải đảo chiều\n(Đáy B chỉ là thanh khoản)", dx=-9, dy=-12, col="#ef6c00")
result(ax, "Vẫn TĂNG – tiếp tục chờ giá về discount", GR)

ax = next(A); base(ax, "5. Thân đóng dưới Đáy A (mốc cấu trúc)")
path(ax, [(9.5, 112), (12, 99.5)]); candle(ax, 12.4, 99.5, 96.5, 100, 96); path(ax, [(12.8, 96.5), (13.5, 95), (14.2, 97)])
note(ax, 12.4, 96.5, "thân đóng dưới mốc cấu trúc\n→ dấu hiệu đảo chiều", dx=-9.5, dy=-7, col=RD)
result(ax, "CHƯA RÕ xu hướng → xét lại theo B1–B5", "#757575")

ax = next(A); base(ax, "6. Đi ngang giữa Đáy B và Đỉnh mới")
path(ax, [(9.5, 112), (10.5, 114.5), (11.5, 110), (12.5, 115), (13.5, 111)])
note(ax, 12.5, 115, "không đóng thân qua Đỉnh mới,\nkhông xuống discount", dx=-6, dy=4, col="#757575")
result(ax, "Vẫn TĂNG – KHÔNG vào lệnh (chờ)", GR)

fig.suptitle("SAU TRƯỜNG HỢP B4: đã xác nhận TĂNG nhưng Đáy B hồi không tới 50% (Đáy B = thanh khoản, mốc cấu trúc = Đáy A)",
             fontsize=15, fontweight="bold")
plt.tight_layout(rect=(0, 0, 1, .95)); plt.savefig("examples/44-sau-truong-hop-b4.png", dpi=75); print("ok")
