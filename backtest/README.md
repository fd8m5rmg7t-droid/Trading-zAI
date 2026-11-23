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

## Lần 4 – chỉ dùng M15 cho cả xác định xu hướng/POI lẫn vào lệnh (`--khung M15/M15`)
- Tìm xu hướng liên tục: 6 lệnh, thắng 0, **−5.34R** (5 lệnh dính SL cứng, 1 hòa vốn).
- Tìm xu hướng lại mỗi ngày: 3 lệnh, thắng 1 (+4.0R, chốt TP2), thua 1 (−1.06R), hòa 1 → **+2.88R**.
- Giới hạn: trong một nến M15 không biết giá chạm điểm vào hay SL trước → mô phỏng giả định SL trước (thận trọng);
  2 lệnh "vào và dính SL trong cùng 1 nến" có thể bị đánh giá xấu hơn thực tế. Có thể dùng dữ liệu M1 để biết thứ tự chính xác.
- Mẫu 3–6 lệnh: chưa đủ để kết luận. Hình 7 lệnh (gộp cả hai cách): `xauusd-m15m15-lenh.png`.

## Lần 5 – chỉ khai thác PHASE 4, KHÔNG cần POI (`--vung discount`)
Thay vì chờ giá về POI hợp lệ: chỉ cần phase 3 hợp lệ (giá hồi chạm đường 50% sóng đẩy, vào discount/premium),
sau đó chờ tạo đáy/đỉnh trên khung vào lệnh rồi vào lệnh ở 1/2 râu như cũ. Tối đa 1 lệnh mỗi sóng.

| Khung | Tìm xu hướng | Lệnh | Thắng/Thua/Hòa | Tổng | TB thắng / TB thua | Sụt giảm lớn nhất |
|---|---|---|---|---|---|---|
| M15/M15 | lại mỗi ngày | 32 | 7/21/4 | **+9.42R** | +3.38R / −0.67R | −7.4R |
| M15/M15 | liên tục | 30 | 2/24/4 | −14.45R | +1.54R / −0.72R | −14.5R |
| M15/M1 | lại mỗi ngày | 106 | 11/95/0 | +1.22R | +4.31R / −0.49R | −19.4R |
| M15/M1 | liên tục | 90 | 4/86/0 | −31.29R | +3.37R / −0.52R | −33.0R |

Đường lợi nhuận: `xauusd-phase4-equity.png`. Lưu ý: đã thử nhiều biến thể trên cùng 3,5 tháng dữ liệu → dễ "khớp dữ liệu";
cần kiểm tra lại trên dữ liệu khác (năm khác, cặp khác) trước khi tin.
