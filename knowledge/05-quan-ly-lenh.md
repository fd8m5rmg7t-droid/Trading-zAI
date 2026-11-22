# Quản lý lệnh

## Nguyên tắc chung (người dùng đã giảng, chờ duyệt hình `examples/29-quan-ly-lenh-phase.png`)
- **Chỉ giao dịch thuận xu hướng:** BUY khi xu hướng tăng, SELL khi xu hướng giảm.
- **Khai thác theo order flow = khai thác PHASE 2 hoặc PHASE 4.** Các phase này **kỳ vọng sẽ phá đỉnh (BUY) hoặc đáy (SELL) trước đó**.
- Cách hiểu của Claude: lệnh khai thác phase 2 vào ở cuối phase 1 (vùng đáy thấp nhất của tích lũy), kỳ vọng phá đỉnh gần nhất; lệnh khai thác phase 4 vào ở cuối phase 3 (đáy tạm thời), kỳ vọng phá đỉnh mới của phase 2.

**Chưa chốt:**
- Chốt lời đặt ở đâu: ngay tại đỉnh/đáy trước đó (mức kỳ vọng bị phá), hay giữ đến khi tạo đỉnh/đáy mới?

## Đã biết từ các bài trước (chi tiết trong `03-setup.md` mục 7)
- **Vào lệnh:** đặt lệnh chờ tại 1/2 râu của nến có điểm thấp nhất (BUY) / cao nhất (SELL), sau khi có nến xác nhận đáy/đỉnh trong vùng POI.
- **Dừng lỗ:** khi có nến (khung vào lệnh) đóng thân qua điểm thấp nhất (BUY) / cao nhất (SELL).
- **Vào lệnh khi quét thanh khoản (chỉ thuận xu hướng):** sau khi nến quét đóng cửa, đặt limit tại 1/2 râu của nến quét nếu mức đó nằm bên kia giá thanh khoản; ngược lại đặt tại chính giá thanh khoản. Dừng lỗ khi có nến đóng thân qua điểm thấp/cao nhất của nến quét. Giá không hồi về điểm vào → bỏ lệnh.
- **Chưa học:** chốt lời, dời SL, SL cứng bảo hiểm (người dùng sẽ nghiên cứu).
