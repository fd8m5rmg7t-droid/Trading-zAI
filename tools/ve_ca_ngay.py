#!/usr/bin/env python3
"""Vẽ TOÀN BỘ một ngày giao dịch (M15): xu hướng (có thể đổi trong ngày), pha đẩy / pha hồi, 50%, thanh khoản,
POI hợp lệ và các lệnh backtest của ngày đó.
Cách dùng: python3 tools/ve_ca_ngay.py 2026-09-16 XAUUSD_M15.csv [trades.csv]"""
import os, sys, csv
sys.path.insert(0, os.path.dirname(__file__))
import smc_engine as eng, backtest as bt
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "DejaVu Sans"
DAY, CSV = sys.argv[1], sys.argv[2]; TR = sys.argv[3] if len(sys.argv) > 3 else None
bars = [eng.Bar(b.t[:16], b.o, b.h, b.l, b.c) for b in eng.load_csv(CSV)]
st = bt.day_starts(bars); k = next(i for i, x in enumerate(st) if bars[x].t >= DAY + " 05:00")
s = st[k] - 1; e = st[k + 1] if k + 1 < len(st) else len(bars)
seg = bars[s:e]; n = len(seg); r = eng.analyze(seg, start_rule="prev_close")
HI = max(x.h for x in seg); LO = min(x.l for x in seg); RG = HI - LO
fig, ax = plt.subplots(figsize=(26, 12))
BG = {"UP": "#e8f5e9", "SIDE_UP": "#f1f8e9", "DOWN": "#ffebee", "SIDE_DOWN": "#fff3f3", "UNCLEAR": "#eeeeee"}
for i in range(n):
    ax.axvspan(i - .5, i + .5, color=BG[r.state[i]], lw=0, zorder=0)
for i, x in enumerate(seg):
    c = "#26a69a" if x.c >= x.o else "#ef5350"
    ax.plot([i, i], [x.l, x.h], color=c, lw=1.2, zorder=3)
    ax.add_patch(plt.Rectangle((i - .32, min(x.o, x.c)), .64, max(abs(x.c - x.o), .02), color=c, zorder=4))
# --- các đoạn xu hướng
segs = []; cur = None
for i in range(n):
    m = r.ctx[i][0]
    if m in ("UP", "DOWN"):
        if cur is None or cur["mode"] != m:
            cur = {"mode": m, "a": i, "b": i}; segs.append(cur)
        cur["b"] = i
    else:
        cur = None
for sg in segs:
    up = sg["mode"] == "UP"; a, b = sg["a"], sg["b"]
    _, T, B, _ = r.ctx[a]
    pts = [(B.i, B.price), (T.i, T.price)] if up else [(T.i, T.price), (B.i, B.price)]
    # xác nhận kiểu "phá đỉnh rồi đáy cao hơn": pha hồi (B sau T) đã xong → thêm pha đẩy trước đó
    ext, cnt = (T, B) if up else (B, T)
    if cnt.i > ext.i and getattr(ext, "src", None) is not None:
        pv = ext.src
        pts = [(pv.i, pv.price), (ext.i, ext.price), (cnt.i, cnt.price)]
    for i in range(a + 1, b + 1):
        _, T2, B2, _ = r.ctx[i]
        p, q = ((B2, T2) if up else (T2, B2))
        if q.i != pts[-1][0] and q.i not in [x[0] for x in pts]:
            if p.i != pts[-1][0]:
                pts.append((p.i, p.price))
            pts.append((q.i, q.price))
    endi = min(n - 1, b + 1)
    rng = range(pts[-1][0] + 1, endi + 1)
    sc = r.ctx[b][3]
    if sc is not None:
        rng = range(pts[-1][0] + 1, sc)
    if len(rng) and len(pts) % 2 == 0:          # chỉ thêm điểm cuối pha hồi khi đang kết thúc ở một đỉnh/đáy của pha đẩy
        j = min(rng, key=lambda q: seg[q].l) if up else max(rng, key=lambda q: seg[q].h)
        pts.append((j, seg[j].l if up else seg[j].h))
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color="#111", lw=2.4, zorder=5, alpha=.85)
    for q in range(0, len(pts) - 1, 2):
        (ai, ap), (bi, bp) = pts[q], pts[q + 1]; mid = (ap + bp) / 2
        ax.annotate("", xy=(bi, bp), xytext=(ai, ap), arrowprops=dict(arrowstyle="-|>", color="#6a1b9a", lw=1.8), zorder=6)
        nxt = pts[q + 2] if q + 2 < len(pts) else None
        xe = nxt[0] if nxt else n
        ax.plot([bi, xe], [mid, mid], color="#6a1b9a", ls="--", lw=1.2, zorder=5)
        ax.text(bi + .2, mid, f"50% {mid:.1f}", fontsize=8, color="#6a1b9a", va="bottom" if up else "top", fontweight="bold")
        # POI hợp lệ trong pha đẩy
        A = seg if up else bt.neg(seg); sgn = 1 if up else -1
        for i in range(min(ai, bi), max(ai, bi) + 1):
            if bt.is_poi(A, i) and A[i].h <= sgn * mid and any(bt.bull_fvg(A, z) for z in range(i, i + 3)):
                ax.add_patch(plt.Rectangle((i - .45, seg[i].l), xe - i + .4, seg[i].h - seg[i].l, color="#ce93d8", alpha=.45, zorder=2))
                ax.text(i, seg[i].l if up else seg[i].h, "POI", fontsize=8, color="#6a1b9a", fontweight="bold", va="top" if up else "bottom")
        rev_end = sg["b"] < n - 1 and r.ctx[sg["b"] + 1][0] == "UNKNOWN" and q + 2 == len(pts) - 1
        if nxt and rev_end:
            ax.scatter([nxt[0]], [nxt[1]], s=70, color="#555", zorder=7)
            ax.text(nxt[0], nxt[1] + (-RG * .02 if up else RG * .02), "phá " + ("đáy" if up else "đỉnh") + " tạo ra " + ("đỉnh" if up else "đáy") +
                    "\n→ dấu hiệu đảo chiều", ha="center", va="top" if up else "bottom", fontsize=8.5, fontweight="bold", color="#555")
        elif nxt:
            hp = nxt[1]; ok = (hp <= mid) if up else (hp >= mid)
            col = "#2e7d32" if ok else "#ef6c00"
            ax.scatter([nxt[0]], [hp], s=70, color=col, zorder=7)
            ax.text(nxt[0], hp + (-RG * .02 if up else RG * .02), "hồi đủ" if ok else "hồi KHÔNG đủ\n→ thanh khoản", ha="center",
                    va="top" if up else "bottom", fontsize=8.5, fontweight="bold", color=col)
            if not ok:
                ax.plot([nxt[0], n], [hp, hp], color="#ef6c00", ls="--", lw=1.6, zorder=5)
for i, t in r.events:
    if t.startswith("Xác nhận") or t.startswith("Dấu hiệu") or t.startswith("Vượt"):
        col = "#2e7d32" if "TĂNG" in t else ("#c62828" if "GIẢM" in t else "#555")
        ax.axvline(i, color=col, lw=1.1, ls=":")
        ax.text(i + .2, HI + RG * .13, f"{seg[i].t[11:]} {t.replace('→ chưa rõ xu hướng', '')}", rotation=90, fontsize=8.5, va="top", color=col, fontweight="bold")
# --- lệnh
if TR:
    for t in csv.DictReader(open(TR)):
        if not (seg[1].t <= t["t_in"] <= seg[-1].t):
            continue
        ti = next(i for i, x in enumerate(seg) if x.t == t["t_in"]); to = next((i for i, x in enumerate(seg) if x.t == t["t_out"]), n - 1)
        ent = float(t["entry"]); R = float(t["R"]); col = "#2e7d32" if R > .05 else ("#c62828" if R < -.05 else "#555")
        ax.plot([ti, to], [ent, ent], color="#1565c0", lw=2.6, zorder=8)
        ax.plot([ti, to], [float(t["hard_sl"])] * 2, color="#6a1b9a", lw=1.2, ls=":", zorder=8)
        ax.scatter([ti], [ent], s=120, marker="v" if t["side"] == "SELL" else "^", color="#1565c0", zorder=9)
        ax.text(ti, ent + (RG * .03 if t["side"] == "SELL" else -RG * .03), f"{t['side']} {t['t_in'][11:]}\n{t['exit'][:24]}\n{R:+.2f}R",
                fontsize=9, fontweight="bold", color=col, ha="center", va="bottom" if t["side"] == "SELL" else "top",
                bbox=dict(facecolor="white", alpha=.85, edgecolor=col, boxstyle="round,pad=0.2"), zorder=10)
for i, x in enumerate(seg):
    if bt.blocked(x.t):
        ax.add_patch(plt.Rectangle((i - .5, LO - RG * .1), 1, RG * .025, color="#757575", zorder=2))
ticks = list(range(0, n, 4)); ax.set_xticks(ticks); ax.set_xticklabels([seg[i].t[11:] for i in ticks], fontsize=8.5)
ax.set_xlim(-1, n + 2); ax.set_ylim(LO - RG * .13, HI + RG * .15)
ax.set_title(f"XAUUSD M15 – cả ngày {seg[1].t[8:10]}/{seg[1].t[5:7]}/{seg[1].t[:4]}: xu hướng (nền xanh tăng / đỏ giảm / xám chưa rõ), "
             "đường giá (đen), pha đẩy (tím), 50%, POI hợp lệ (tím nhạt), thanh khoản (cam), lệnh (xanh dương)", loc="left", fontsize=12, fontweight="bold")
ax.text(.01, -.05, "Nền đậm: đang phá đỉnh/đáy; nền nhạt: đi ngang trong xu hướng. Vạch xám dưới đáy: giờ cấm giao dịch. Nét chấm tím ngang theo lệnh: SL cứng.",
        transform=ax.transAxes, va="top", fontsize=10)
plt.tight_layout(); out = f"backtest/ca-ngay-{DAY}.png"; plt.savefig(out, dpi=80); print(out)
for i, t in r.events: print(seg[i].t[11:], t)
