# Định nghĩa SMC & setup vào lệnh

> **Mục đích của bài đỉnh/đáy:** chỉ để biết **KHI NÀO** một đỉnh hoặc đáy đã hình thành (thời điểm xác nhận). Việc đỉnh/đáy nào quan trọng và dùng chúng ra sao sẽ học ở các bài sau.

## 1. Đỉnh (swing high)

**Quy tắc:** Đỉnh hình thành (được xác nhận) khi có **một cây nến có THÂN đóng cửa dưới ĐÁY (low) của cây nến LIỀN TRƯỚC**.

**Đã xác nhận (xem `examples/02-cac-truong-hop-dinh.png`):**
- **A. Là đỉnh:** thân nến đóng cửa dưới low của nến trước. Mức giá của đỉnh là high cao nhất của nhịp tăng.
- **B. Chưa phải đỉnh:** chỉ có râu chọc xuống dưới low của nến trước, còn thân đóng cửa phía trên.
- **C. Chưa phải đỉnh:** thân đóng cửa dưới thân nến trước nhưng vẫn trên low của nến đó (còn trong vùng râu dưới).
- **D. Là đỉnh:** chỉ so với nến LIỀN TRƯỚC, không so với nến tạo đỉnh. Nếu sau đỉnh có nến nhỏ đi ngang, nến đóng cửa dưới low của nến nhỏ đó là đủ để xác nhận.
- **E. Là đỉnh:** nhịp điều chỉnh nhỏ trong xu hướng tăng cũng tạo đỉnh, nếu thỏa quy tắc. Đỉnh sau chỉ là đỉnh mới khi nó đã phá vỡ đỉnh trước (xem mục "Khi nào xác định ĐỈNH MỚI").
- **F. Chưa phải đỉnh:** giá đóng cửa ĐÚNG BẰNG low của nến trước thì KHÔNG tính. Phải đóng cửa thấp hơn hẳn.

**Chưa chốt:**
- Phân loại đỉnh lớn và đỉnh nhỏ (có thể sẽ học ở bài cấu trúc thị trường).

**Cách xác định mức giá đỉnh trên biểu đồ (đã xác nhận):**
1. Chọn một cây nến bất kỳ làm điểm bắt đầu.
2. Đi tiếp sang phải cho đến khi gặp cây nến xác nhận đỉnh (thân đóng cửa thấp hơn hẳn low của nến liền trước).
3. **Đỉnh = râu cao nhất (high lớn nhất)** trong khoảng từ cây nến bắt đầu đến cây nến xác nhận, **TÍNH CẢ râu của chính cây nến xác nhận**. Đáy làm ngược lại: râu thấp nhất, tính cả nến xác nhận.

Minh họa: `examples/04-cach-xac-dinh-dinh-day.png` (ô 3: đã chọn cách (a)).

**Khi nào xác định ĐỈNH MỚI (đã xác nhận):**
- Chỉ xác định đỉnh mới **khi đỉnh cũ bị phá vỡ**.
- **Phá vỡ** = có một cây nến có **THÂN đóng cửa vượt qua đỉnh cũ**. Chỉ có râu vượt qua thì chưa phải phá vỡ.
- Hệ quả: các đỉnh nhỏ hình thành *dưới* đỉnh cũ khi đỉnh cũ chưa bị phá thì **không phải đỉnh mới**.
- Minh họa: `examples/05-dinh-moi-khi-pha-vo.png`
- Sau khi phá vỡ, **quét tìm đỉnh mới bắt đầu từ chính cây nến phá vỡ**.
- Thân đóng cửa **ĐÚNG BẰNG** đỉnh cũ thì **chưa tính** là phá vỡ, phải đóng cửa cao hơn hẳn.

## 2. Đáy (swing low)

**Quy tắc (ngược lại với đỉnh, đã xác nhận):** Đáy hình thành khi có **một cây nến có THÂN đóng cửa trên ĐỈNH (high) của cây nến LIỀN TRƯỚC**. Mức giá của đáy là low thấp nhất của nhịp giảm.

**Đáy mới (ngược lại với đỉnh, đã xác nhận):** chỉ xác định đáy mới khi đáy cũ bị phá vỡ, tức là có nến có **THÂN đóng cửa thấp hơn hẳn đáy cũ**. Quét tìm đáy mới bắt đầu từ cây nến phá vỡ. Mức giá đáy là râu thấp nhất từ nến phá vỡ đến nến xác nhận đáy (tính cả nến xác nhận). Các đáy nhỏ nằm trên đáy cũ chưa bị phá thì không phải đáy mới.

Các trường hợp A–F tương tự đỉnh, chỉ đảo chiều (xem `examples/03-cac-truong-hop-day.png`). Giá đóng cửa ĐÚNG BẰNG high của nến trước thì KHÔNG tính, phải đóng cửa cao hơn hẳn.

Ví dụ chart thật: `examples/01-dinh-day-xauusd-h4.jpg`

## 3. Cấu trúc thị trường

**Đáy giữa hai đỉnh (đã xác nhận):**
- Điểm thấp nhất giữa hai đỉnh được coi là đáy.
- "Giữa hai đỉnh" = từ nến tạo đỉnh cũ đến nến tạo đỉnh mới (đỉnh mới đã phá vỡ đỉnh cũ).
- "Điểm thấp nhất" = râu thấp nhất (low), không phải giá đóng cửa.
- **Không cần** thỏa quy tắc xác nhận đáy (mục 2). Cứ là điểm thấp nhất giữa hai đỉnh là đủ.
- Minh họa: `examples/06-day-giua-hai-dinh.png`

**Đỉnh giữa hai đáy (ngược lại, đã xác nhận):**
- Điểm cao nhất (râu cao nhất, high) giữa hai đáy được coi là đỉnh, tính từ nến tạo đáy cũ đến nến tạo đáy mới (đáy mới đã phá vỡ đáy cũ). Không cần thỏa quy tắc xác nhận đỉnh.
