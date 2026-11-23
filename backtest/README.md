# Backtest lần 1 – XAUUSD, 03/08 → 14/11/2026 (giờ VN)

Dữ liệu: HistData M1 (người dùng tải lên Google Drive), M15 gộp từ M1. Công cụ: `tools/backtest.py`.

Phạm vi: chỉ khai thác **phase 4 tại POI** (BUY xu hướng tăng / SELL xu hướng giảm). CHƯA có: vào lệnh kiểu quét
thanh khoản, khai thác phase 3, tránh tin tức. Spread trừ 0.30/lệnh. Kết quả tính bằng R.

## Kết quả
- Phễu lọc: 245 sóng → 56 POI hợp lệ → 16 lần giá chạm POI trong phase 3 → 13 lệnh chờ → **6 lệnh khớp**.
- **6 lệnh, thua cả 6, tổng −3.34R** (mỗi lệnh −0.27 đến −0.91R; đều thoát do nến M1 đóng cửa qua điểm thấp/cao nhất).
- Mẫu quá nhỏ để kết luận về phương pháp.

## Nhận xét (Claude)
- Trên M1, "nến xác nhận đáy" (đóng cửa trên high nến trước) xảy ra gần như ngay khi giá vừa chạm mép POI → điểm vào
  thường nằm ở mép POI, giá đi tiếp xuyên qua POI và lệnh bị dừng lỗ theo giá đóng cửa M1 sau vài phút.
- Bộ lọc POI rất chặt (nằm trọn trong discount + FVG ngay sau + chưa bị chạm) → rất ít cơ hội.
- Cần người dùng quyết định trước khi chỉnh: xem câu hỏi trong cuộc trò chuyện.

Hình từng lệnh: `xauusd-2026-08-11-lenh.png`. Danh sách lệnh: `xauusd-2026-08-11-lenh.csv`.
