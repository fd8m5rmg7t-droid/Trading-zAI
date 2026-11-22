# Thị trường & khung thời gian

- **Thị trường:** Forex
- **Phong cách:** Scalping
- **Cặp tiền (đã xác nhận):** các cặp tiền CHÍNH có USD (EURUSD, GBPUSD, AUDUSD, NZDUSD, USDJPY, USDCHF, USDCAD) và **vàng XAUUSD**.
- Phiên giao dịch: tránh giờ giao phiên (xem bên dưới).
- Khung thời gian (khung xác định xu hướng & order flow / khung vào lệnh): _người dùng nhờ Claude tư vấn, chưa chốt_.

## Thời điểm KHÔNG giao dịch (đã xác nhận)
- **Không giao dịch 30 phút trước và 30 phút sau mỗi lần giao phiên.**
- **Không giao dịch khi thị trường có tin tức mạnh ảnh hưởng.**

**Chưa chốt:**
- **Thời gian tin tức: người dùng sẽ thông báo cho Claude** khi có tin. Khi được báo, Claude không đề xuất vào lệnh trong khoảng thời gian đó.

**Mốc giao phiên (đã xác nhận: cả 3 mốc, theo giờ mở phiên FOREX, giờ Việt Nam):**

| Mốc | Mùa đông (đầu tháng 11 → giữa tháng 3) | Mùa hè (giữa tháng 3 → đầu tháng 11) |
|---|---|---|
| Phiên Á (Tokyo) mở 09:00 giờ Tokyo | 07:00 → **không GD 06:30–07:30** | 07:00 → **06:30–07:30** (Nhật không đổi giờ) |
| Phiên Âu (London) mở 08:00 giờ London | 15:00 → **14:30–15:30** | 14:00 → **13:30–14:30** |
| Phiên Mỹ (New York) mở 08:00 giờ New York | 20:00 → **19:30–20:30** | 19:00 → **18:30–19:30** |

(Claude tự tính quy đổi; ngày chuyển giờ: Mỹ đổi giờ Chủ nhật thứ 2 của tháng 3 và Chủ nhật đầu tiên của tháng 11; châu Âu đổi giờ Chủ nhật cuối tháng 3 và cuối tháng 10 – có vài tuần lệch nhau.)

## Công cụ không dùng
- **Không dùng BOS / CHoCH** (đã xác nhận).
