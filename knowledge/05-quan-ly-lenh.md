# Quản lý lệnh

## Nguyên tắc chung
- **Chỉ giao dịch thuận xu hướng:** BUY khi xu hướng tăng, SELL khi xu hướng giảm (đã xác nhận).
- Phase 2 và phase 4 của order flow đều kỳ vọng phá đỉnh/đáy trước đó, nhưng **CHỈ KHAI THÁC PHASE 4**, **không khai thác phase 2** (người dùng sửa lại; Claude hiểu câu "không khai thác phase mà chỉ khai thác phase 4" là "không khai thác phase 2").
- Lệnh khai thác phase 4 vào ở **cuối phase 3** (đáy tạm thời khi BUY / đỉnh tạm thời khi SELL), theo cách vào lệnh tại POI hoặc quét thanh khoản (`03-setup.md` mục 6–7).

## Chốt lời (người dùng đã giảng, chờ duyệt hình `examples/30-chot-loi-phase4.png`)
- **Chốt 1/2 lệnh** khi giá **chạm đỉnh cũ** (BUY) / **đáy cũ** (SELL) – tức đỉnh/đáy tạo ra ở cuối phase 2.
- **Chốt phần còn lại** khi giá **phá đỉnh cũ và tạo đỉnh mới** (BUY) / phá đáy cũ và tạo đáy mới (SELL).

**Chưa chốt:**
- "Chạm" đỉnh cũ = râu nến chạm là đủ?
- "Tạo đỉnh mới" = nến xác nhận đỉnh (quy tắc mục 1) đóng cửa → chốt phần còn lại tại giá đóng cửa đó?
- Sau khi chốt 1/2: có dời dừng lỗ (ví dụ về điểm vào) không?

## Đã biết từ các bài trước (chi tiết trong `03-setup.md` mục 7)
- **Vào lệnh:** đặt lệnh chờ tại 1/2 râu của nến có điểm thấp nhất (BUY) / cao nhất (SELL), sau khi có nến xác nhận đáy/đỉnh trong vùng POI.
- **Dừng lỗ:** khi có nến (khung vào lệnh) đóng thân qua điểm thấp nhất (BUY) / cao nhất (SELL).
- **Vào lệnh khi quét thanh khoản (chỉ thuận xu hướng):** sau khi nến quét đóng cửa, đặt limit tại 1/2 râu của nến quét nếu mức đó nằm bên kia giá thanh khoản; ngược lại đặt tại chính giá thanh khoản. Dừng lỗ khi có nến đóng thân qua điểm thấp/cao nhất của nến quét. Giá không hồi về điểm vào → bỏ lệnh.
- **Chưa học:** chốt lời, dời SL, SL cứng bảo hiểm (người dùng sẽ nghiên cứu).
