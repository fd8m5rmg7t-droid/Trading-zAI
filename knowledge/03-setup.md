# Định nghĩa SMC & setup vào lệnh

## 1. Đỉnh (swing high)

**Quy tắc:** Đỉnh hình thành (được xác nhận) khi có **một cây nến có THÂN đóng cửa dưới ĐÁY (low) của cây nến LIỀN TRƯỚC**.

**Đã xác nhận (xem `examples/02-cac-truong-hop-dinh.png`):**
- **A. Là đỉnh:** thân nến đóng cửa dưới low của nến trước. Mức giá của đỉnh là high cao nhất của nhịp tăng.
- **B. Chưa phải đỉnh:** chỉ có râu chọc xuống dưới low của nến trước, còn thân đóng cửa phía trên.
- **C. Chưa phải đỉnh:** thân đóng cửa dưới thân nến trước nhưng vẫn trên low của nến đó (còn trong vùng râu dưới).
- **D. Là đỉnh:** chỉ so với nến LIỀN TRƯỚC, không so với nến tạo đỉnh. Nếu sau đỉnh có nến nhỏ đi ngang, nến đóng cửa dưới low của nến nhỏ đó là đủ để xác nhận.
- **E. Là đỉnh:** nhịp điều chỉnh nhỏ trong xu hướng tăng cũng tạo đỉnh, nếu thỏa quy tắc.

**Chưa chốt:**
- F. Giá đóng cửa ĐÚNG BẰNG low của nến trước thì có tính là đỉnh không?
- Đáy (swing low) có áp dụng ngược lại không: thân nến đóng cửa trên high của nến liền trước?
- Phân loại đỉnh lớn và đỉnh nhỏ (có thể sẽ học ở bài cấu trúc thị trường).

Ví dụ chart thật: `examples/01-dinh-day-xauusd-h4.jpg`
