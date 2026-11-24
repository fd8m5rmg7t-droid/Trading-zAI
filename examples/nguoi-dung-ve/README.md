# Các trường hợp người dùng tự vẽ (đợt 1, 24/11/2026) – CHỜ người dùng tổng hợp đủ rồi mới phân tích

1. `truong-hop-1.png`: Đáy 1 → Đỉnh 1 → Đáy 2 (hồi không đủ → thanh khoản) → Đỉnh 2 → hồi đủ → Đỉnh 3 xác nhận xu hướng tăng tiếp diễn. PnD vẽ trên từng pha đẩy.
2. `truong-hop-2.png`: hồi đủ về vùng thanh khoản (đáy 2 hồi không đủ) → vào lệnh theo khai thác thanh khoản.
3. `truong-hop-3.png`: hồi đủ, quét qua thanh khoản xuống POI trong discount → vào lệnh theo khai thác POI.
4. `truong-hop-4.png`: hồi xuyên qua thanh khoản, POI, phá Đáy 1 → có thể đảo chiều xu hướng.
5. `truong-hop-5.png`: phá Đáy 1 (có thể đảo chiều) → Đáy 3 → Đỉnh 3 (hồi đủ) → Đáy 4 xác nhận xu hướng giảm.
6. `truong-hop-6.png`: phá Đáy 1 (có thể đảo chiều) → Đáy 3 → Đỉnh 3; giá không phá Đỉnh 2 và Đáy 3 → đi sideway (hộp tím: vùng từ Đỉnh 2 đến Đáy 3, có đường 50%).
7. `truong-hop-7.png`: Đỉnh 3 hồi không đủ (dưới 50% của Đỉnh 2→Đáy 3) → thanh khoản; Đáy 4 xác nhận xu hướng giảm; khai thác theo kiểu thanh khoản tại Đỉnh 3.
8. `truong-hop-8.png`: Đỉnh 3 hồi đủ; Đáy 4 xác nhận giảm; sau đó Đỉnh 3 bị phá → có thể thay đổi xu hướng.
9. `truong-hop-9.png`: Đỉnh 3 hồi không đủ; Đáy 4 xác nhận giảm; sau đó Đỉnh 2 bị phá → có thể thay đổi xu hướng.

## Phân tích của Claude (chờ người dùng xác nhận)
- Quy tắc mới rút ra: đỉnh/đáy của **pha hồi KHÔNG đủ** chỉ là **thanh khoản**, KHÔNG phải mốc cấu trúc. Mốc xét
  "dấu hiệu đảo chiều" là đỉnh/đáy của **pha hồi ĐỦ gần nhất** (TH4: phá Đáy 1 mới có thể đảo chiều, không phải Đáy 2;
  TH8: Đỉnh 3 hồi đủ → phá Đỉnh 3; TH9: Đỉnh 3 hồi không đủ → phải phá Đỉnh 2).
  → Bộ máy hiện tại đang coi đáy nông là mốc đảo chiều (khác với hình).
- Xác nhận xu hướng không cần pha hồi đủ (TH7: Đỉnh 3 hồi không đủ, Đáy 4 vẫn xác nhận giảm) – khớp quy tắc hiện có.
- Vào lệnh: hồi đủ chạm thanh khoản → khai thác thanh khoản (TH2); đi qua thanh khoản xuống POI → khai thác POI (TH3).
- Câu hỏi: POI ở TH3 phải nằm trong discount của sóng nào; khi nào chọn TH2 hay chờ TH3; hộp TH6 có phải PnD để xét Đỉnh 3 hồi đủ.
