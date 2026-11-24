#!/usr/bin/env python3
"""Cách hiểu quy tắc mới (chờ người dùng duyệt): sau B4 muốn BUY phải đợi thân nến phá Đỉnh mới.
Ra examples/45-b4-doi-pha-dinh-moi.png"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from ve_so_do_xu_huong import frame, path, pt, level, candle, note, result, pnd, GR, RD, PU, BL
from ve_so_do_b4 import BASE

fig, axs = plt.subplots(1, 2, figsize=(24, 9.5)); A = axs.flat
ax = next(A); frame(ax, "TRƯỚC (bộ máy đang làm): về discount là BUY ngay")
path(ax, BASE + [(12, 103.5), (13, 108)])
pt(ax, 3, 98, "Đáy A = MỐC CẤU TRÚC", up=False, col=PU); pt(ax, 6, 116, "Đỉnh mới"); pt(ax, 8.5, 109, "Đáy B (TK)", up=False, col="#ef6c00")
pnd(ax, 98, 116, 3, 15)
ax.scatter([12], [103.5], marker="^", s=140, color=BL, zorder=8)
note(ax, 12, 103.5, "BUY (chưa phá Đỉnh mới)", dx=-1, dy=-9)
result(ax, "SẼ BỎ: không BUY khi chưa phá Đỉnh mới", RD)

ax = next(A); frame(ax, "SAU (cách mình hiểu): đợi thân nến phá Đỉnh mới rồi mới BUY")
P = [(0, 108), (2, 98), (4, 112), (5.5, 107), (6.5, 110), (8, 116.5), (9, 119), (12, 105.5), (13, 110)]
path(ax, P)
pt(ax, 2, 98, "Đáy A = MỐC CẤU TRÚC", up=False, col=PU); pt(ax, 4, 112, "Đỉnh mới"); pt(ax, 5.5, 107, "Đáy B (TK)", up=False, col="#ef6c00")
pt(ax, 9, 119, "Đỉnh mới 2")
level(ax, 112, 4, 15, "Đỉnh mới")
candle(ax, 7.5, 111, 114, 114.5, 110.5)
note(ax, 7.5, 114, "thân nến đóng trên Đỉnh mới\n→ từ đây mới được tìm lệnh BUY", dx=-7.5, dy=5, col=PU)
pnd(ax, 98, 119, 9, 15)
ax.scatter([12], [105.5], marker="^", s=140, color=BL, zorder=8)
note(ax, 12, 105.5, "BUY ở discount của sóng\nĐáy A → Đỉnh mới 2\n(9 trường hợp ở ảnh 42)", dx=-1.5, dy=-13)
result(ax, "Sóng đầu tiên sau B4: không giao dịch", GR)
fig.suptitle("Sau B4 (Đáy B hồi không tới 50%): muốn BUY phải đợi PHÁ ĐỈNH MỚI – cách mình hiểu, chờ bạn duyệt", fontsize=14, fontweight="bold")
plt.tight_layout(rect=(0, 0, 1, .93)); plt.savefig("examples/45-b4-doi-pha-dinh-moi.png", dpi=75); print("ok")
