# Trading-zAI — Bộ kiến thức giao dịch

Repo này lưu phương pháp giao dịch do người dùng trực tiếp dạy cho Claude.
Đầu mỗi phiên: đọc file này và các file trong `knowledge/` trước khi phân tích hay trả lời về trading.

## Hồ sơ giao dịch
- **Thị trường:** Forex
- **Phong cách:** Scalping
- **Phương pháp:** SMC (Smart Money Concepts)
- **Cặp:** các cặp chính có USD + vàng XAUUSD
- **Khung thời gian:** M15 (xu hướng, order flow, POI) / M1 (vào lệnh)

## Nguyên tắc làm việc
- Chỉ áp dụng đúng quy tắc người dùng đã dạy; chỗ nào chưa được dạy thì hỏi, không tự bịa.
- Khi phát hiện mâu thuẫn hoặc rủi ro trong quy tắc, nói thẳng.
- Kiến thức mới được ghi vào đúng file trong `knowledge/`, ví dụ lệnh thật vào `examples/`.

## Mục lục
- `knowledge/01-triet-ly.md` — tư duy, quan điểm giao dịch
- `knowledge/02-thi-truong.md` — cặp tiền, phiên, khung thời gian
- `knowledge/03-setup.md` — định nghĩa SMC và các setup vào lệnh
- `knowledge/04-quan-ly-von.md` — rủi ro, khối lượng, cắt lỗ
- `knowledge/05-quan-ly-lenh.md` — chốt lời, dời SL, thoát lệnh
- `knowledge/06-tam-ly.md` — kỷ luật, lỗi cần tránh

## Tiến độ học (cập nhật 2026-11-22)
- **Đã xong:** Bài 1 Đỉnh/Đáy; Bài 2 Cấu trúc thị trường (xu hướng tăng/giảm, đi ngang, dấu hiệu và xác nhận đảo chiều, chưa rõ xu hướng); Bài 3 Order flow (4 phase: tích lũy, sóng đẩy, hồi, tiếp diễn); Bài 4 PnD tool (premium/discount, phase 3 hợp lệ, order flow thiếu và 3 trường hợp khai thác). Bài 5 Thanh khoản: định nghĩa (tách riêng với POI), 3 loại thanh khoản, quy tắc quét. Bài 6 POI: FVG (định nghĩa), POI = nến có râu dài hơn thân + nến sau không đóng cửa thoát; chọn POI trong discount/premium có FVG hỗ trợ; POI hết hiệu lực; vào lệnh tại 1/2 râu sau khi tạo đáy/đỉnh; dừng lỗ khi nến đóng thân qua điểm thấp/cao nhất. Chi tiết trong `knowledge/03-setup.md`.
- **Đã xong thêm:** vào lệnh khi quét thanh khoản (`03-setup.md` mục 6); Bài 7 Quản lý lệnh: chỉ thuận xu hướng, chỉ khai thác phase 4, chốt 1/2 khi chạm đỉnh/đáy cũ, dời SL về điểm vào (cả khi giá tạo đỉnh thấp hơn đỉnh cũ), chốt phần còn lại khi tạo đỉnh/đáy mới; khai thác phase 3 ngược xu hướng với TP toàn bộ tại POI có giá trị gần nhất (`05-quan-ly-lenh.md`). Quản lý vốn: SL cứng 3 pip/3 giá, rủi ro cố định mỗi lệnh, công cụ `tools/tinh_khoi_luong.py` (`04-quan-ly-von.md`).
- **Đã xong thêm:** thị trường (`02-thi-truong.md`): cặp, khung M15/M1, giờ giao phiên cấm giao dịch, tin tức do người dùng báo. KHÔNG dùng BOS/CHoCH.
- **Người dùng sẽ quyết định sau:** số tiền rủi ro cố định, thông số hợp đồng vàng.
- **Đang làm: bộ máy tự động + backtest** (`tools/smc_engine.py`). Đã có phần 1: đọc CSV (MT5/TradingView), nhận diện đỉnh/đáy + xu hướng M15, vẽ chart; mới chạy thử trên dữ liệu giả lập (`examples/33-...`). Còn: order flow, PnD, POI/FVG, thanh khoản, vào lệnh M1, quản lý lệnh, backtest.
- **Đang chờ người dùng:** file CSV nến M15 và M1 (xuất từ MT5) – Dukascopy chặn tải tự động (429), không vượt rào.
- **Còn mở:** phân loại đỉnh/đáy lớn và nhỏ.
- **Cách dạy người dùng ưa thích:** người dùng giảng, Claude vẽ hình minh họa cách mình hiểu (matplotlib, lưu vào `examples/`), người dùng duyệt rồi mới ghi là "đã xác nhận".
