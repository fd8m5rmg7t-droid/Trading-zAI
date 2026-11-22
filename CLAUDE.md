# Trading-zAI — Bộ kiến thức giao dịch

Repo này lưu phương pháp giao dịch do người dùng trực tiếp dạy cho Claude.
Đầu mỗi phiên: đọc file này và các file trong `knowledge/` trước khi phân tích hay trả lời về trading.

## Hồ sơ giao dịch
- **Thị trường:** Forex
- **Phong cách:** Scalping
- **Phương pháp:** SMC (Smart Money Concepts)

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
- **Đã xong:** Bài 1 Đỉnh/Đáy; Bài 2 Cấu trúc thị trường (xu hướng tăng/giảm, đi ngang, dấu hiệu và xác nhận đảo chiều, chưa rõ xu hướng); Bài 3 Order flow (4 phase: tích lũy, sóng đẩy, hồi, tiếp diễn). Chi tiết trong `knowledge/03-setup.md`.
- **Bài tiếp theo:** vùng thanh khoản (phase 3 hồi về đâu), BOS / CHoCH.
- **Đã đề xuất, chưa làm:** viết code tự động đánh dấu đỉnh/đáy và xu hướng trên dữ liệu giá thật để người dùng kiểm tra.
- **Còn mở:** phân loại đỉnh/đáy lớn và nhỏ.
- **Cách dạy người dùng ưa thích:** người dùng giảng, Claude vẽ hình minh họa cách mình hiểu (matplotlib, lưu vào `examples/`), người dùng duyệt rồi mới ghi là "đã xác nhận".
