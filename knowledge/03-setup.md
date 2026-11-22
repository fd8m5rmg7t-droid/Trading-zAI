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
- Con sóng đẩy giá **vượt qua vùng đi ngang** (phase 1) trước đó, **CÙNG CHIỀU xu hướng** (đã xác nhận): xu hướng tăng thì phase 2 đẩy giá phá lên để tăng tiếp; xu hướng giảm thì phase 2 đẩy giá phá xuống để giảm tiếp.
- Sóng phá **ngược chiều** xu hướng **không phải phase 2**, đó là dấu hiệu đảo chiều (mục 3).
- Minh họa cách hiểu: `examples/12-order-flow-phase2.png`
- **"Vượt qua"** = có nến có **thân đóng cửa ra ngoài vùng** tích lũy, giống quy tắc phá vỡ (đã chốt tạm thời).
- **Phase 2 bắt đầu** từ **đáy THẤP NHẤT trong vùng tích lũy** (xu hướng tăng), hoặc **đỉnh CAO NHẤT trong vùng tích lũy** (xu hướng giảm). Không phải đáy/đỉnh cuối cùng trong vùng (đã chốt tạm thời).

**Phase 3: HỒI** (người dùng đã giảng)
- Sau khi giá đã được đẩy lên một đoạn (phase 2), giá **hồi về một điểm nào đó**. Đó là phase 3.
- **Phase 2 kết thúc** tại đỉnh mới (xu hướng tăng) / đáy mới (xu hướng giảm), và **phase 3 bắt đầu từ đó** (đã xác nhận).
- Minh họa: `examples/13-order-flow-phase3.png`
- **Hồi về đâu:** về **vùng có thanh khoản**. Sẽ thảo luận chi tiết sau (bài thanh khoản).
- **Hồi sâu quá đáy tạo ra đỉnh mới** (xu hướng tăng) / **quá đỉnh tạo ra đáy mới** (xu hướng giảm): lúc này **xu hướng có thể đã thay đổi**.
- **Phase 3 kết thúc** khi giá tạo **đáy tạm thời** (xu hướng tăng) hoặc **đỉnh tạm thời** (xu hướng giảm).
- **Đáy/đỉnh tạm thời** được xác nhận bằng **quy tắc mục 1–2** (nến có thân đóng cửa qua high/low của nến liền trước) (đã xác nhận).

**Phase 4: TIẾP DIỄN** (người dùng đã giảng)
- Giá tiếp tục tăng (hoặc giảm), **phá vỡ đỉnh (hoặc đáy) cũ** để tiếp tục xu hướng.
- Phase 4 **bắt đầu từ đáy/đỉnh tạm thời** (cuối phase 3). "Đỉnh cũ" bị phá là **đỉnh mới tạo ra ở cuối phase 2**, phá bằng **thân nến đóng cửa**.
- **Sau phase 4, chu kỳ lặp lại** thành một order flow mới (tích lũy → sóng đẩy → hồi → tiếp diễn).
- **Phase 3 đã tạo đáy tạm thời nhưng giá không phá được đỉnh của phase 2** → quay lại **phase 1 (tích lũy)** của một order flow mới.
- (Người dùng trả lời "có" cho cả 4 ý trên; Claude hiểu là xác nhận tất cả.)
- Minh họa đủ 4 phase: `examples/14-order-flow-4-phase.png`

## 5. PnD tool (Premium & Discount)

**Định nghĩa (đã xác nhận):**
- Công cụ xác định **vùng premium** và **vùng discount**.
- Đo từ **đáy đến đỉnh của con sóng gần nhất** = **sóng đẩy phase 2**: từ đáy tạo ra đỉnh gần nhất đến đỉnh gần nhất (xu hướng giảm: từ đỉnh tạo ra đáy gần nhất đến đáy gần nhất).
- Đáy/đỉnh đo theo **râu nến** (low/high).
- **Đường trung bình** (50%) chia vùng giá thành 2 vùng:
  - **Premium:** từ đường trung bình lên đến đỉnh.
  - **Discount:** từ đường trung bình xuống đến đáy.
- **Đo lại** mỗi khi giá phá vỡ tạo đỉnh mới (hoặc đáy mới).
- **Cách dùng:** xu hướng tăng thì chờ giá hồi về **discount** để mua; xu hướng giảm thì chờ giá hồi lên **premium** để bán.
- Minh họa: `examples/15-pnd-tool.png`

**Điều kiện phase 3 hợp lệ – ORDER FLOW THIẾU (đã xác nhận):**
- Phase 3 chỉ **hợp lệ** khi giá hồi về **ít nhất chạm đường trung bình**, hoặc đi vào vùng **discount** (xu hướng tăng) / **premium** (xu hướng giảm).
- Nếu giá **không hồi đủ** mà **tiếp tục phá đỉnh (hoặc đáy)** luôn thì order flow đó được coi là **ORDER FLOW THIẾU**.
- Minh họa: `examples/16-order-flow-thieu.png`

- **"Chạm"** đường trung bình: chỉ cần **râu nến** chạm là đủ (đã xác nhận).
- **Sau order flow thiếu (đã xác nhận):** giá thường **hồi về vùng discount (hoặc premium) của order flow thiếu** để khai thác thêm một lần nữa, trước khi đẩy giá tiếp diễn xu hướng.
- **Đáy tạm chưa hồi đủ (đáy nông)** được coi là **một dạng thanh khoản**. **KHÔNG giao dịch ở đáy nông này**, chỉ giao dịch theo **cách quét thanh khoản** (người dùng sẽ dạy sau).
- Minh họa: `examples/17-order-flow-thieu-khai-thac.png`

- **PnD của order flow thiếu** đo từ **đáy bắt đầu phase 2** đến **đỉnh mới sau khi phá**, bỏ qua đáy nông (đã xác nhận).

**Các trường hợp khai thác order flow thiếu (ví dụ xu hướng tăng; đã xác nhận, xem `examples/18-order-flow-thieu-3-truong-hop.png`):**
1. **Đáy nông trùng đường trung bình** của PnD, hoặc **nằm trong vùng discount** → chỉ khai thác khi giá **quét thanh khoản đáy nông** (cách quét: học sau).
2. **Đáy nông nằm trong vùng premium** → **không khai thác** ở đáy nông; phải **đợi giá hồi về một vùng trong discount** mới khai thác.
3. Giá hồi về nhưng **không phá đáy nông**, sau đó đẩy lên **phá đỉnh mới**, hoàn thành **một order flow mới hoàn chỉnh** → **đánh dấu** order flow thiếu này lại.

- "Nằm dưới vùng discount" / "nằm trên vùng premium" trong lời giảng nghĩa là **nằm trong** vùng discount / premium (đã xác nhận).
- **Lý do đánh dấu (trường hợp 3):** lúc nào đó giá sẽ **quay lại khai thác vùng đó** và **hoàn thành order flow chưa hoàn thành**. Vùng đánh dấu được giữ cho đến khi giá quay lại hoàn thành nó.

## 6. Thanh khoản (liquidity)

**Định nghĩa (đã xác nhận, tách riêng với POI):** chỗ **tập trung lệnh chờ / stop loss**, ví dụ: trên đỉnh, dưới đáy, hai đỉnh bằng nhau. Giá hay **quét** qua những chỗ này.

**3 loại thanh khoản (đã xác nhận, xem `examples/19-thanh-khoan-3-loai.png`). Mỗi thanh khoản là MỘT MỨC GIÁ:**
1. **Đỉnh/đáy theo quy tắc phá vỡ – phụ thuộc xu hướng:**
   - **Xu hướng tăng:** các **ĐÁY tạo ra đỉnh mới** (đỉnh mới đã phá vỡ đỉnh trước) là thanh khoản. Các đỉnh KHÔNG tính là thanh khoản loại 1.
   - **Xu hướng giảm:** các **ĐỈNH tạo ra đáy mới** (đáy mới đã phá vỡ đáy trước) là thanh khoản.
   - Mức giá = chính đáy (râu thấp nhất) / đỉnh (râu cao nhất) đó.
2. **Đáy nông (đỉnh nông) của order flow thiếu.** Mức giá = giá đáy nông.
3. **Mô hình 2 đỉnh / 2 đáy:** chỉ xét **2 đỉnh (hoặc 2 đáy) LIÊN TIẾP**, mỗi cái xác nhận theo quy tắc mục 1–2. Hai đỉnh/đáy **chênh nhau vẫn tính**. Mức giá = **đỉnh CAO NHẤT** của 2 đỉnh / **đáy THẤP NHẤT** của 2 đáy.

**Quét thanh khoản (đã xác nhận, xem `examples/20-quet-thanh-khoan.png`):**
- **Quét thanh khoản ở đáy:** **râu nến chạy qua (xuống dưới) giá thanh khoản**, nhưng **giá đóng cửa của chính cây nến đó nằm TRÊN giá thanh khoản**.
- **Quét thanh khoản ở đỉnh:** ngược lại – râu chạy lên trên giá thanh khoản, giá đóng cửa của chính nến đó nằm DƯỚI.
- **Chỉ tính RÂU quét của MỘT nến.** Nến đóng cửa vượt qua (phá vỡ) rồi nến SAU mới đóng lại phía bên kia → **KHÔNG phải quét**.
- **Râu quét phải DÀI hơn thân nến.** Râu ngắn hơn thân → **KHÔNG coi là quét**.
- Thân nến đóng cửa vượt qua giá thanh khoản là **phá vỡ**, không phải quét.
- Giá đóng cửa **ĐÚNG BẰNG** giá thanh khoản → **KHÔNG tính là quét** (đã xác nhận).
- **Sau khi bị quét**, thanh khoản đó **không còn hiệu quả để khai thác lần 2** (đã xác nhận).

**Chưa chốt:**
- "Râu dài hơn thân": chỉ so phần râu quét (râu dưới khi quét đáy, râu trên khi quét đỉnh) với thân? (Claude đang hiểu như vậy.)

## 7. POI (point of interest)

**Định nghĩa (đã xác nhận, tách riêng với thanh khoản):** **vùng giá có khả năng phản ứng để vào lệnh**.

**POI theo cách của người dùng (đã xác nhận, xem `examples/22-poi-tranh-chap.png`):**
- POI là **vùng giá tranh chấp giữa bên mua và bên bán**, thể hiện qua hình thức nến.
- Điều kiện:
  1. **Nến 1 (nến liền trước) phải có ÍT NHẤT MỘT RÂU (trên hoặc dưới) dài HƠN THÂN.** Râu dài nhất chỉ bằng thân, hoặc chỉ tổng hai râu mới dài hơn thân → không phải POI. **Màu nến không quan trọng. Râu dài nằm ở phía nào không quan trọng.** (Xem `examples/23-poi-hinh-dang-nen.png`: ô 1–4 là POI, ô 5–7 không.)
  2. **Nến liền sau** có giá đóng cửa **KHÔNG thoát** khỏi vùng high–low của nến 1. Chỉ xét giá đóng cửa; râu nến sau vượt ra ngoài vẫn được.
  3. Giá đóng cửa **ĐÚNG BẰNG** high/low của nến 1 → chưa thoát → **vẫn là POI**.
- **Vùng POI = toàn bộ nến 1, tính cả râu** (từ high đến low).
- Nhiều nến liên tiếp cùng đóng cửa trong vùng → **POI vẫn chỉ là nến 1**, không mở rộng.

**Chọn POI để giao dịch (đã xác nhận, xem `examples/24-poi-hop-le.png`):**
- Trong một con sóng có rất nhiều POI. **Chỉ xét:**
  - POI ở vùng **DISCOUNT** cho lệnh **BUY**.
  - POI ở vùng **PREMIUM** cho lệnh **SELL**.
- POI đó **cần có FVG hỗ trợ** = FVG **cùng chiều lệnh**, hình thành **ngay sau POI** (bộ 3 nến tạo FVG bắt đầu trong vòng 2 nến sau nến POI).
- **Cả nến POI phải nằm TRỌN** trong discount (BUY) / premium (SELL). POI cắt ngang đường 50% thì không xét.
- **POI càng cách xa đường cân bằng 50% thì càng giá trị.**

**POI hết hiệu lực (người dùng đã giảng, chờ duyệt hình `examples/25-poi-het-hieu-luc.png`):**
- POI **chỉ dùng được MỘT lần**: khi giá đã về khai thác vùng đó rồi, nếu giá về khai thác **lần nữa** thì POI **không còn giá trị**.
- Hoặc: **ngay lần đầu** giá về vùng POI mà **cây nến đó có thân đóng qua POI** → POI hết hiệu lực.

**Chưa chốt:**
- "Đóng qua POI" = thân nến đóng cửa vượt ra ngoài phía bên kia của POI (dưới low POI khi BUY, trên high POI khi SELL)? Đóng cửa BÊN TRONG POI có tính là đóng qua không? Râu xuyên qua nhưng thân đóng cửa quay lại thì sao? (Claude đoán: cả hai chưa phải "đóng qua", POI vẫn dùng được.)
- Thế nào là "giá về khai thác": chỉ cần râu chạm vào vùng POI là tính một lần?

### 7.1 FVG (Fair Value Gap)
- **Định nghĩa (đã xác nhận, giống định nghĩa SMC phổ biến):** bộ 3 nến liên tiếp. FVG tăng: low nến 3 > high nến 1, vùng FVG = từ high nến 1 đến low nến 3. FVG giảm: high nến 3 < low nến 1, vùng = từ high nến 3 đến low nến 1. Râu nến 1 và 3 chồng nhau thì không có FVG.
- Minh họa: `examples/21-fvg.png`
- **Lưu ý:** cách hiểu phổ biến "giá thường quay lại lấp một phần/toàn bộ FVG rồi phản ứng" là **SAI** theo người dùng. Giá hồi về FVG như thế nào: **học sau**. Không tự áp dụng mức 50% FVG.
