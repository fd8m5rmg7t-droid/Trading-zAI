# Quản lý vốn

## Rủi ro mỗi lệnh (đã xác nhận)
- Mỗi lệnh, nếu lỗ thì chỉ mất **một số tiền CỐ ĐỊNH**. Claude tự tính khối lượng (lot) cho từng lệnh.
- Số tiền cố định: **chưa chốt** (chờ người dùng cho biết, ví dụ X USD).

## Stop loss cứng (đã xác nhận khoảng cách)
- **Cặp tiền: 3 pip. Vàng: 3 giá (3.00).**
- SL cứng đặt **cách điểm thấp nhất (BUY) / cao nhất (SELL) thêm 3 pip / 3 giá** (đã xác nhận), đóng vai trò bảo hiểm cho quy tắc dừng lỗ theo giá đóng cửa (`03-setup.md`).

## Cách tính khối lượng
- Lot = số tiền rủi ro / (khoảng cách từ điểm vào đến SL cứng × giá trị 1 đơn vị giá của 1 lot), làm tròn XUỐNG theo bước 0.01 lot.
- Công cụ: `tools/tinh_khoi_luong.py` (giả định hợp đồng chuẩn: cặp tiền 1 lot = 100.000; XAUUSD 1 lot = 100 oz). Chưa tính spread, phí, trượt giá.
- Tính theo SL cứng nên mức lỗ tối đa ≈ số tiền cố định, kể cả khi dừng lỗ theo giá đóng cửa chưa kịp kích hoạt.

**Người dùng sẽ quyết định sau:**
- Số tiền rủi ro cố định mỗi lệnh; đơn vị tiền tài khoản (USD?).
- Thông số hợp đồng của sàn (đặc biệt vàng: 1 lot = 100 oz?).
