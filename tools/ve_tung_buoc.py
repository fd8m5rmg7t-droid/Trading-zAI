import sys
sys.path.insert(0, "/home/user/Trading-zAI/tools")
import smc_engine as eng, backtest as bt
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "DejaVu Sans"
DAY_T = "2026-10-22 15:00"
m1 = [eng.Bar(b.t[:16], b.o, b.h, b.l, b.c) for b in eng.load_csv("data/XAUUSD_M15_VN.csv")]
st = bt.day_starts(m1); k = max(i for i, x in enumerate(st) if m1[x].t <= DAY_T); s = st[k] - 1; e = st[k + 1]
seg = m1[s:e]; r = eng.analyze(seg)
T = lambda hhmm: next(i for i, x in enumerate(seg) if x.t[11:] == hhmm)

def candles(ax, a, b, hl=()):
    for i in range(a, b):
        x = seg[i]; c = "#26a69a" if x.c >= x.o else "#ef5350"
        ax.plot([i, i], [x.l, x.h], color=c, lw=1.3, zorder=3)
        ax.add_patch(plt.Rectangle((i - .32, min(x.o, x.c)), .64, max(abs(x.c - x.o), .02), color=c, zorder=4,
                                   ec="#000" if i in hl else c, lw=1.6 if i in hl else 0))

CONF = next(i for i, t in r.events if t.startswith('Xác nhận'))
HH = seg[CONF].t[11:]

def step1():
    a, b = 0, CONF + 6
    fig, ax = plt.subplots(figsize=(20, 9.5))
    ax.axvspan(-.5, CONF - .5, color="#eeeeee", zorder=0)
    ax.axvspan(CONF - .5, b, color="#ffebee", zorder=0)
    candles(ax, a, b, hl=(0,))
    ax.annotate(f"ĐIỂM BẮT ĐẦU\nnến đóng cửa phiên ngày trước\n(nến {seg[0].t[11:]} sáng {seg[0].t[8:10]}/{seg[0].t[5:7]} giờ VN, đóng {seg[0].c:.2f})", xy=(0, seg[0].c), xytext=(3.5, seg[0].c + 2),
                fontsize=10, fontweight="bold", arrowprops=dict(arrowstyle="->"))
    sw = sorted([w for w in r.swings if w.conf <= CONF], key=lambda w: w.i)
    nt = nb = 0
    for w in sw:
        if w.kind == "T":
            nt += 1; ax.scatter([w.i], [w.price], marker="v", s=110, color="#f57f17", zorder=6)
            ax.text(w.i, w.price + 1.2, f"Đỉnh {nt}\n{w.price:.2f}", ha="center", va="bottom", fontsize=10, color="#e65100", fontweight="bold")
        else:
            nb += 1; ax.scatter([w.i], [w.price], marker="^", s=110, color="#1565c0", zorder=6)
            ax.text(w.i, w.price - 1.2, f"Đáy {nb}\n{w.price:.2f}", ha="center", va="top", fontsize=10, color="#0d47a1", fontweight="bold")
        ax.plot([w.conf, w.conf], [seg[w.conf].c, seg[w.conf].c], marker="o", ms=7, mfc="none", mec="#555", zorder=7)
    ax.plot([w.i for w in sw], [w.price for w in sw], color="#616161", lw=1.2, ls="--", zorder=5)
    tops = [w for w in sw if w.kind == "T"][-2:]; bots = [w for w in sw if w.kind == "B"][-2:]
    ax.plot([w.i for w in tops], [w.price for w in tops], color="#e65100", lw=2.8, ls=(0, (6, 3)), zorder=6)
    ax.plot([w.i for w in bots], [w.price for w in bots], color="#0d47a1", lw=2.8, ls=(0, (6, 3)), zorder=6)
    c = CONF
    ax.axvline(c, color="#c62828", lw=1.2, ls="--")
    nT = {id(w): n + 1 for n, w in enumerate([w for w in sw if w.kind == "T"])}; nB = {id(w): n + 1 for n, w in enumerate([w for w in sw if w.kind == "B"])}
    ax.text(c + .3, max(x.h for x in seg[a:b]) + 1.5, f"{HH} XÁC NHẬN XU HƯỚNG GIẢM\n(Đỉnh {nT[id(tops[1])]} < Đỉnh {nT[id(tops[0])]}, Đáy {nB[id(bots[1])]} < Đáy {nB[id(bots[0])]})", fontsize=10.5,
            fontweight="bold", color="#c62828", va="top")
    ax.text(.01, -.06, "Vòng tròn rỗng = nến xác nhận của từng đỉnh/đáy (quy tắc mục 1–2: thân đóng cửa qua low/high của nến liền trước).\n"
                       "Nét đứt xám: nối các đỉnh/đáy theo thời gian. Nét đứt đậm: 2 đỉnh gần nhất (cam) và 2 đáy gần nhất (xanh) dùng để kết luận.",
            transform=ax.transAxes, va="top", fontsize=10)
    ticks = list(range(a, b, 2)); ax.set_xticks(ticks); ax.set_xticklabels([seg[i].t[11:] for i in ticks], fontsize=8.5)
    ax.set_xlim(a - 1, b + 1); ax.set_ylim(min(x.l for x in seg[a:b]) - 9, max(x.h for x in seg[a:b]) + 6)
    ax.set_title(f"BƯỚC 1 – XAUUSD M15, ngày {seg[1].t[8:10]}/{seg[1].t[5:7]}/{seg[1].t[:4]}: bắt đầu từ giá đóng cửa ngày trước, tìm 2 đỉnh + 2 đáy để xác định xu hướng",
                 loc="left", fontsize=13, fontweight="bold")
    plt.tight_layout(); plt.savefig("/home/user/Trading-zAI/backtest/buoc-1-m15.png", dpi=95)
    for w in sw: print(w.kind, seg[w.i].t[11:], w.price, "conf", seg[w.conf].t[11:])

step1()
