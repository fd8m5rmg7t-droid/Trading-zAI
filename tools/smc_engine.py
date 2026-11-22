#!/usr/bin/env python3
"""Bộ máy nhận diện theo các quy tắc người dùng đã dạy (knowledge/03-setup.md).

Phần 1 (file này): đọc dữ liệu nến, xác định đỉnh/đáy và xu hướng trên khung lớn (M15).
  - Khi CHƯA biết xu hướng: dùng quy tắc mục 1–2 (nến có thân đóng cửa qua low/high của nến
    liền trước) để tìm lần lượt đỉnh/đáy; đủ 2 đỉnh + 2 đáy cùng chiều thì kết luận xu hướng.
  - Khi ĐÃ biết xu hướng tăng (mục 3): theo dõi đỉnh gần nhất T và đáy tạo ra nó B.
      * Có nến đóng cửa > T  -> phá vỡ, quét tìm đỉnh mới từ nến phá vỡ đến nến xác nhận đỉnh
        (tính cả râu nến xác nhận). Đáy mới tạo ra đỉnh mới = điểm thấp nhất giữa T cũ và đỉnh mới.
      * Có nến đóng cửa < B  -> dấu hiệu đảo chiều -> CHƯA RÕ XU HƯỚNG, quay lại chế độ mục 1–2
        (giữ B, T làm 2 điểm đầu) cho đến khi có 2 đỉnh + 2 đáy cùng chiều.
      * Nằm giữa B và T       -> ĐI NGANG.
    Xu hướng giảm: ngược lại.
  - "Vượt qua" luôn phải thấp/cao hơn HẲN (bằng thì không tính).
"""
import csv
from dataclasses import dataclass, field


# ----------------------------------------------------------------------------- dữ liệu
@dataclass
class Bar:
    t: str
    o: float
    h: float
    l: float
    c: float


def load_csv(path):
    """Đọc CSV xuất từ MT5 (<DATE> <TIME> <OPEN> ...) hoặc TradingView (time,open,high,low,close)."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        sample = f.read(4096); f.seek(0)
        delim = "\t" if sample.count("\t") > sample.count(",") else ","
        rows = list(csv.reader(f, delimiter=delim))
    head = [h.strip().strip("<>").lower() for h in rows[0]]
    idx = {k: head.index(k) for k in ("open", "high", "low", "close")}
    if "date" in head and "time" in head:
        tt = lambda r: r[head.index("date")] + " " + r[head.index("time")]
    else:
        k = "time" if "time" in head else head[0]
        tt = lambda r: r[head.index(k)]
    return [Bar(tt(r), float(r[idx["open"]]), float(r[idx["high"]]), float(r[idx["low"]]), float(r[idx["close"]]))
            for r in rows[1:] if r and r[0].strip()]


# ----------------------------------------------------------------------------- kết quả
@dataclass
class Swing:
    kind: str      # "T" (đỉnh) hoặc "B" (đáy)
    i: int         # chỉ số nến tạo đỉnh/đáy (râu cao/thấp nhất)
    price: float
    conf: int      # chỉ số nến xác nhận (hoặc nến mà tại đó đỉnh/đáy được ghi nhận)
    how: str       # "m12" (quy tắc mục 1–2) | "break" (phá vỡ) | "between" (cực trị giữa hai đỉnh/đáy)


@dataclass
class Result:
    swings: list = field(default_factory=list)
    state: list = field(default_factory=list)   # trạng thái theo từng nến: UP / DOWN / SIDE_UP / SIDE_DOWN / UNCLEAR
    events: list = field(default_factory=list)  # (i, text)


# ----------------------------------------------------------------------------- lõi
def analyze(bars):
    n = len(bars)
    H = [b.h for b in bars]; L = [b.l for b in bars]; C = [b.c for b in bars]
    res = Result(state=["UNCLEAR"] * n)

    mode = "UNKNOWN"
    hist = []                 # các đỉnh/đáy dùng để kết luận xu hướng (chế độ mục 1–2)
    look = None               # "T" hoặc "B": đang chờ xác nhận loại nào; None = chưa biết
    start = 0                 # điểm bắt đầu quét
    T = B = None              # khi đã có xu hướng: đỉnh/đáy gần nhất và cực trị tạo ra nó
    scan = None               # chỉ số nến phá vỡ khi đang quét đỉnh/đáy mới

    def add(sw):
        res.swings.append(sw)
        return sw

    def conclude(i):
        nonlocal mode, T, B, scan
        tops = [s for s in hist if s.kind == "T"][-2:]
        bots = [s for s in hist if s.kind == "B"][-2:]
        if len(tops) < 2 or len(bots) < 2:
            return
        if tops[1].price > tops[0].price and bots[1].price > bots[0].price:
            mode = "UP"; T = tops[1]
            # đáy tạo ra đỉnh gần nhất = đáy (mục 1–2) gần nhất nằm TRƯỚC đỉnh đó
            prev = [s for s in hist if s.kind == "B" and s.i < T.i]
            B = prev[-1] if prev else bots[1]
            res.events.append((i, "Xác nhận XU HƯỚNG TĂNG"))
        elif tops[1].price < tops[0].price and bots[1].price < bots[0].price:
            mode = "DOWN"; B = bots[1]
            prev = [s for s in hist if s.kind == "T" and s.i < B.i]
            T = prev[-1] if prev else tops[1]
            res.events.append((i, "Xác nhận XU HƯỚNG GIẢM"))
        scan = None

    for i in range(1, n):
        if mode == "UNKNOWN":
            top_c = C[i] < L[i - 1]          # nến xác nhận đỉnh
            bot_c = C[i] > H[i - 1]          # nến xác nhận đáy
            if look in (None, "T") and top_c:
                j = max(range(start, i + 1), key=lambda k: H[k])
                hist.append(add(Swing("T", j, H[j], i, "m12"))); look = "B"; start = j
                conclude(i)
            elif look in (None, "B") and bot_c:
                j = min(range(start, i + 1), key=lambda k: L[k])
                hist.append(add(Swing("B", j, L[j], i, "m12"))); look = "T"; start = j
                conclude(i)
            res.state[i] = "UNCLEAR" if mode == "UNKNOWN" else mode
            if mode != "UNKNOWN":
                continue
            continue

        up = mode == "UP"
        # --- đang quét đỉnh (đáy) mới sau khi phá vỡ
        if scan is not None:
            confirmed = C[i] < L[i - 1] if up else C[i] > H[i - 1]
            if confirmed:
                rng = range(scan, i + 1)
                j = max(rng, key=lambda k: H[k]) if up else min(rng, key=lambda k: L[k])
                new = add(Swing("T" if up else "B", j, H[j] if up else L[j], i, "break"))
                old = T if up else B
                mid = range(old.i, j + 1)
                k = min(mid, key=lambda q: L[q]) if up else max(mid, key=lambda q: H[q])
                other = add(Swing("B" if up else "T", k, L[k] if up else H[k], i, "between"))
                if up:
                    T, B = new, other
                else:
                    B, T = new, other
                scan = None
                res.events.append((i, ("Đỉnh mới " if up else "Đáy mới ") + f"{new.price}"))
            res.state[i] = mode
            # trong lúc quét vẫn kiểm tra phá vỡ phía ngược lại
        edge_far = B.price if up else T.price           # đáy tạo ra đỉnh (xu hướng tăng)
        edge_near = T.price if up else B.price          # đỉnh gần nhất (xu hướng tăng)
        if (up and C[i] < edge_far) or (not up and C[i] > edge_far):
            res.events.append((i, "Dấu hiệu ĐẢO CHIỀU → chưa rõ xu hướng"))
            mode = "UNKNOWN"
            # Theo quy tắc: Đỉnh 2 (T) đã có; Đáy 2 = đáy mới sau khi phá B; xác nhận giảm khi
            # Đỉnh 3 < Đỉnh 2 VÀ Đáy 3 < Đáy 2  → chỉ giữ T làm điểm đầu (xu hướng giảm: giữ B).
            hist = [T] if up else [B]
            look = "B" if up else "T"                   # đang giảm phá đáy → chờ đáy mới
            start = (T.i if up else B.i)
            scan = None
            res.state[i] = "UNCLEAR"
            continue
        if scan is None and ((up and C[i] > edge_near) or (not up and C[i] < edge_near)):
            scan = i
            res.state[i] = mode
            # nến phá vỡ có thể đồng thời là nến xác nhận? (cần nến sau) → chờ nến sau
            continue
        if scan is None:
            res.state[i] = "SIDE_" + mode
    return res


# ----------------------------------------------------------------------------- vẽ
def plot(bars, res, path, title="", start=0, end=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = "DejaVu Sans"
    end = end or len(bars)
    fig, ax = plt.subplots(figsize=(22, 9))
    colors = {"UP": "#e8f5e9", "DOWN": "#ffebee", "SIDE_UP": "#fffde7", "SIDE_DOWN": "#fffde7", "UNCLEAR": "#eeeeee"}
    for i in range(start, end):
        ax.axvspan(i - .5, i + .5, color=colors[res.state[i]], zorder=0, lw=0)
        b = bars[i]; col = "#26a69a" if b.c >= b.o else "#ef5350"
        ax.plot([i, i], [b.l, b.h], color=col, lw=.8, zorder=3)
        ax.add_patch(plt.Rectangle((i - .3, min(b.o, b.c)), .6, max(abs(b.c - b.o), 1e-9), color=col, zorder=4))
    for s in res.swings:
        if not (start <= s.i < end):
            continue
        mk = "v" if s.kind == "T" else "^"
        col = {"m12": "#6a1b9a", "break": "#f57f17" if s.kind == "T" else "#1565c0", "between": "#1565c0" if s.kind == "B" else "#f57f17"}[s.how]
        y = s.price
        ax.scatter([s.i], [y], marker=mk, s=60, color=col, zorder=6)
    for i, t in res.events:
        if start <= i < end:
            ax.annotate(t, xy=(i, bars[i].c), xytext=(i, bars[i].c), fontsize=7, rotation=90, color="#333", va="bottom")
    ax.set_title(title + "   (nền xanh: tăng, đỏ: giảm, vàng: đi ngang, xám: chưa rõ; ▼ đỉnh, ▲ đáy)", loc="left", fontsize=11)
    ax.set_xlim(start - 1, end)
    plt.tight_layout(); plt.savefig(path, dpi=100); plt.close(fig)


if __name__ == "__main__":
    import sys
    bars = load_csv(sys.argv[1])
    r = analyze(bars)
    print(f"{len(bars)} nến, {len(r.swings)} đỉnh/đáy, {len(r.events)} sự kiện")
    for i, t in r.events[:40]:
        print(bars[i].t, t)
    if len(sys.argv) > 2:
        plot(bars, r, sys.argv[2], title=sys.argv[1])
