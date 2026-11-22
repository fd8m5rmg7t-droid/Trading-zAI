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

**Khi nào dùng quy tắc nào (đã xác nhận):**
- **Mục 1 và 2** (nến có thân đóng cửa qua low/high của nến liền trước) dùng để xác nhận **bất kỳ** đỉnh/đáy nào đã hình thành. Mục đích: **xác định xu hướng** khi chưa biết xu hướng.
- **Khi đã biết xu hướng thì dùng mục 3:**
  - Xu hướng tăng: đỉnh theo dõi bằng quy tắc phá vỡ. Đáy = điểm thấp nhất giữa hai đỉnh.
  - Xu hướng giảm: đáy theo dõi bằng quy tắc phá vỡ. Đỉnh = điểm cao nhất giữa hai đáy.

**Định nghĩa xu hướng (đã xác nhận):**
- **Xu hướng tăng:** đỉnh sau cao hơn đỉnh trước VÀ đáy sau cao hơn đáy trước.
- **Xu hướng giảm:** đỉnh sau thấp hơn đỉnh trước VÀ đáy sau thấp hơn đáy trước.
- **Xác định xu hướng ban đầu:** chỉ cần **2 đỉnh và 2 đáy** (theo mục 1–2) là đủ kết luận.
- **Thời điểm kết luận xu hướng:** lúc cây nến xác nhận đỉnh/đáy thứ 4 đóng cửa (đã xác nhận).
- **Đỉnh và đáy đi ngược chiều: hai trường hợp KHÁC NHAU (đã xác nhận, người dùng sửa lại cách hiểu ban đầu):**
  - **Đỉnh cao dần, đáy thấp dần = DẤU HIỆU ĐẢO CHIỀU**, không phải đi ngang. Ví dụ: Đỉnh 2 phá Đỉnh 1 (đang tăng), rồi Đáy 2 phá Đáy 1, đó là dấu hiệu đảo chiều, chưa xác nhận. **Xác nhận tăng → giảm** khi hình thành Đỉnh 3 < Đỉnh 2 VÀ Đáy 3 < Đáy 2. Chiều ngược lại (giảm → tăng): Đáy 2 phá Đáy 1, rồi Đỉnh 2 phá Đỉnh 1 là dấu hiệu; xác nhận khi Đáy 3 > Đáy 2 VÀ Đỉnh 3 > Đỉnh 2.
  - Chiều giảm → tăng đã được xác nhận là đúng.
- **ĐI NGANG (sideway), đã xác nhận:**
  - Khi đang **xu hướng tăng**: xét **đỉnh gần nhất** và **đáy tạo ra đỉnh đó** (đáy thấp nhất giữa đỉnh trước và đỉnh gần nhất). Nếu giá **không phá được** đỉnh đó **cũng không phá được** đáy đó thì thị trường đang **đi ngang**.
  - Khi đang **xu hướng giảm**: ngược lại, xét **đáy gần nhất** và **đỉnh tạo ra đáy đó**.
  - Các đỉnh/đáy hình thành bên trong vùng này **không có ý nghĩa**.
  - Lưu ý: một đáy hình thành SAU đỉnh thì không phải "đáy tạo ra đỉnh" đó (lỗi trong cách vẽ ban đầu).
  - **Thoát sideway (đã xác nhận)**, ví dụ khi đang xu hướng tăng:
    - Nến có thân đóng cửa **trên đỉnh gần nhất** → thoát sideway, **xu hướng tăng tiếp diễn**.
    - Nến có thân đóng cửa **dưới đáy tạo ra đỉnh đó** → **dấu hiệu đảo chiều** (như trường hợp C); xác nhận giảm khi có đỉnh thấp hơn VÀ đáy thấp hơn.
    - Xu hướng giảm: làm ngược lại.
  - **Giữa lúc có dấu hiệu đảo chiều và lúc xác nhận đảo chiều:** thị trường ở trạng thái **CHƯA RÕ XU HƯỚNG** (đã xác nhận).
  - Minh họa: `examples/10-di-ngang-vs-dao-chieu.png`
- **Thứ tự không quan trọng:** gặp đỉnh trước hay đáy trước đều được, miễn đủ 2 đỉnh + 2 đáy thỏa điều kiện (đã xác nhận, xem `examples/08-thu-tu-dinh-day.png`).
- Minh họa: `examples/07-xac-dinh-xu-huong.png`

## 4. Order flow

**Định nghĩa:** order flow là cấu trúc của **một con sóng**, gồm **4 phase**.

**Phase 1: TÍCH LŨY (range phase)** (người dùng xem hình và chuyển sang phase 2, không sửa)
- Giá dao động **bên trong đỉnh và đáy của con sóng trước**.
- Cách hiểu của Claude: "con sóng trước" là nhịp từ **đáy tạo ra đỉnh** lên **đỉnh gần nhất** (xu hướng tăng), hoặc ngược lại với xu hướng giảm. Phase 1 trùng với trạng thái **đi ngang** ở mục 3.
- Minh họa: `examples/11-order-flow-phase1.png`

**Phase 2: SÓNG ĐẨY** (người dùng đã giảng)
- Con sóng đẩy giá **vượt qua vùng đi ngang** (phase 1) trước đó.
- Minh họa cách hiểu: `examples/12-order-flow-phase2.png`
- Chưa chốt:
  - "Vượt qua" = có nến có thân đóng cửa ra ngoài vùng (theo quy tắc phá vỡ)?
  - Phase 2 bắt đầu và kết thúc ở đâu (từ đáy cuối cùng trong vùng tích lũy đến đỉnh mới?)
  - Sóng đẩy phá ngược chiều xu hướng (xu hướng tăng mà phá xuống dưới đáy) có gọi là phase 2 không?

**Phase 3, 4:** chưa học.
