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

## Lần 2 – tìm xu hướng lại mỗi ngày từ giá đóng cửa ngày liền trước (`--xu-huong moi-ngay`)
- Ngày giao dịch tách theo khoảng nghỉ cuối ngày của vàng (nến cuối 04:45, mở lại 05:00/06:00 giờ VN).
- Mỗi ngày bộ máy bắt đầu lại từ nến đóng cửa của ngày trước, chưa biết xu hướng cho tới khi đủ 2 đỉnh + 2 đáy.
- Phễu: 289 sóng → 62 POI hợp lệ → 11 lần chạm → 10 lệnh chờ → **3 lệnh khớp, thua cả 3, tổng −1.31R**.
- So với lần 1 (6 lệnh, −3.34R): ít lệnh hơn, lỗ ít hơn nhưng vẫn không có lệnh thắng; mẫu vẫn quá nhỏ.

## Lần 3 – xu hướng/POI trên H4, vào lệnh trên M15 (`--khung H4/M15`)
- H4 gộp từ M15, mốc ngày 17:00 New York (04:00 VN mùa hè / 05:00 mùa đông) như máy chủ MT5 phổ biến.
- Phễu: 18 sóng → 6 POI hợp lệ → **0 lần giá chạm POI trong phase 3 → 0 lệnh**.
- Tìm xu hướng lại mỗi ngày trên H4 (chỉ ~6 nến/ngày) → không đủ 2 đỉnh + 2 đáy → 0 lệnh.
- Tham khảo H1/M5: 52 sóng → 9 POI → 2 lệnh, thua cả 2 (SL cứng), −2.13R.
- Kết luận: 3,5 tháng dữ liệu quá ít cho khung H4; cần dữ liệu nhiều năm.
- Hình đỉnh/đáy/xu hướng H4: `xauusd-h4-xu-huong.png`.
