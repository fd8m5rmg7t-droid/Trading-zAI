# Định nghĩa SMC & setup vào lệnh

> **Mục đích của bài đỉnh/đáy:** chỉ để biết **KHI NÀO** một đỉnh hoặc đáy đã hình thành (thời điểm xác nhận). Việc đỉnh/đáy nào quan trọng và dùng chúng ra sao sẽ học ở các bài sau.

## 1. Đỉnh (swing high)

**Quy tắc:** Đỉnh hình thành (được xác nhận) khi có **một cây nến có THÂN đóng cửa dưới ĐÁY (low) của cây nến LIỀN TRƯỚC**.

**Đã xác nhận (xem `examples/02-cac-truong-hop-dinh.png`):**
- **A. Là đỉnh:** thân nến đóng cửa dưới low của nến trước. Mức giá của đỉnh là high cao nhất của nhịp tăng.
- **B. Chưa phải đỉnh:** chỉ có râu chọc xuống dưới low của nến trước, còn thân đóng cửa phía trên.
- **C. Chưa phải đỉnh:** thân đóng cửa dưới thân nến trước nhưng vẫn trên low của nến đó (còn trong vùng râu dưới).
- **D. Là đỉnh:** chỉ so với nến LIỀN TRƯỚC, không so với nến tạo đỉnh. Nếu sau đỉnh có nến nhỏ đi ngang, nến đóng cửa dưới low của nến nhỏ đó là đủ để xác nhận.
- **E. Là đỉnh:** nhịp điều chỉnh nhỏ trong xu hướng tăng cũng tạo đỉnh, nếu thỏa quy tắc.
- **F. Chưa phải đỉnh:** giá đóng cửa ĐÚNG BẰNG low của nến trước thì KHÔNG tính. Phải đóng cửa thấp hơn hẳn.

**Chưa chốt:**
- Phân loại đỉnh lớn và đỉnh nhỏ (có thể sẽ học ở bài cấu trúc thị trường).

## 2. Đáy (swing low)

**Quy tắc (ngược lại với đỉnh, đã xác nhận):** Đáy hình thành khi có **một cây nến có THÂN đóng cửa trên ĐỈNH (high) của cây nến LIỀN TRƯỚC**. Mức giá của đáy là low thấp nhất của nhịp giảm.

Các trường hợp A–F tương tự đỉnh, chỉ đảo chiều (xem `examples/03-cac-truong-hop-day.png`). Giá đóng cửa ĐÚNG BẰNG high của nến trước thì KHÔNG tính, phải đóng cửa cao hơn hẳn.

Ví dụ chart thật: `examples/01-dinh-day-xauusd-h4.jpg`
