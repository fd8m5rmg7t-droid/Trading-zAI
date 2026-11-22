# Quản lý lệnh

## Nguyên tắc chung
- **Chỉ giao dịch thuận xu hướng:** BUY khi xu hướng tăng, SELL khi xu hướng giảm (đã xác nhận).
- Phase 2 và phase 4 của order flow đều kỳ vọng phá đỉnh/đáy trước đó, nhưng **CHỈ KHAI THÁC PHASE 4**, **không khai thác phase 2** (người dùng sửa lại; Claude hiểu câu "không khai thác phase mà chỉ khai thác phase 4" là "không khai thác phase 2").
- Lệnh khai thác phase 4 vào ở **cuối phase 3** (đáy tạm thời khi BUY / đỉnh tạm thời khi SELL), theo cách vào lệnh tại POI hoặc quét thanh khoản (`03-setup.md` mục 6–7).

## Chốt lời (đã xác nhận, xem `examples/30-chot-loi-phase4.png`)
- **Chốt 1/2 lệnh** khi giá **chạm đỉnh cũ** (BUY) / **đáy cũ** (SELL) – tức đỉnh/đáy tạo ra ở cuối phase 2.
- **Chốt phần còn lại** khi giá **phá đỉnh cũ và tạo đỉnh mới** (BUY) / phá đáy cũ và tạo đáy mới (SELL).

- **"Chạm" đỉnh/đáy cũ** = râu nến chạm là đủ (đã xác nhận).
- **"Tạo đỉnh mới"** = nến xác nhận đỉnh (quy tắc mục 1) đóng cửa → chốt phần còn lại tại giá đóng cửa của nến đó (đã xác nhận).
- **Sau khi chốt 1/2 → dời dừng lỗ về điểm vào lệnh** (hòa vốn) cho phần còn lại (đã xác nhận).

## Dời dừng lỗ khi giá tạo đỉnh thấp hơn (đã xác nhận, xem `examples/31-doi-sl-dinh-thap-hon.png`)
- Sau khi vào lệnh BUY, nếu giá **tạo đỉnh THẤP HƠN đỉnh cũ** (chưa chạm đỉnh cũ) → **dời dừng lỗ về điểm vào lệnh**. SELL ngược lại: giá tạo đáy CAO HƠN đáy cũ → dời dừng lỗ về điểm vào.
- Cách hiểu của Claude: "tạo đỉnh" = có nến xác nhận đỉnh theo quy tắc mục 1. Nếu sau đó giá vẫn lên chạm đỉnh cũ thì quản lý lệnh như bình thường (chốt 1/2, rồi chốt phần còn lại khi tạo đỉnh mới).

- "Tạo đỉnh thấp hơn" xác nhận bằng **quy tắc mục 1** (đã xác nhận).
- **Dừng lỗ tại điểm vào (sau khi dời, ở cả trường hợp này và sau khi chốt 1/2): giá CHẠM điểm vào là thoát lệnh** (không chờ đóng cửa) (đã xác nhận).

## Stop loss cứng và khối lượng
- Xem `04-quan-ly-von.md`: SL cứng 3 pip (cặp tiền) / 3 giá (vàng); khối lượng tính để lỗ đúng một số tiền cố định.

## Đã biết từ các bài trước (chi tiết trong `03-setup.md` mục 7)
- **Vào lệnh:** đặt lệnh chờ tại 1/2 râu của nến có điểm thấp nhất (BUY) / cao nhất (SELL), sau khi có nến xác nhận đáy/đỉnh trong vùng POI.
- **Dừng lỗ:** khi có nến (khung vào lệnh) đóng thân qua điểm thấp nhất (BUY) / cao nhất (SELL).
- **Vào lệnh khi quét thanh khoản (chỉ thuận xu hướng):** sau khi nến quét đóng cửa, đặt limit tại 1/2 râu của nến quét nếu mức đó nằm bên kia giá thanh khoản; ngược lại đặt tại chính giá thanh khoản. Dừng lỗ khi có nến đóng thân qua điểm thấp/cao nhất của nến quét. Giá không hồi về điểm vào → bỏ lệnh.
