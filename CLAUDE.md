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
