# Backtest lần 1 – XAUUSD, 03/08 → 14/11/2026 (giờ VN)

Dữ liệu: HistData M1 (người dùng tải lên Google Drive), M15 gộp từ M1. Công cụ: `tools/backtest.py`.

Phạm vi: chỉ khai thác **phase 4 tại POI** (BUY xu hướng tăng / SELL xu hướng giảm). CHƯA có: vào lệnh kiểu quét
thanh khoản, khai thác phase 3, tránh tin tức. Spread trừ 0.30/lệnh. Kết quả tính bằng R.

## Kết quả
- Phễu lọc: 245 sóng → 56 POI hợp lệ → 16 lần giá chạm POI trong phase 3 → 13 lệnh chờ → **6 lệnh khớp**.
- **6 lệnh, thua cả 6, tổng −3.34R** (mỗi lệnh −0.27 đến −0.91R; đều thoát do nến M1 đóng cửa qua điểm thấp/cao nhất).
- Mẫu quá nhỏ để kết luận về phương pháp.

## Nhận xét (Claude)
- Trên M1, "nến xác nhận đáy" (đóng cửa trên high nến trước) xảy ra gần như ngay khi giá vừa chạm mép POI → điểm vào
  thường nằm ở mép POI, giá đi tiếp xuyên qua POI và lệnh bị dừng lỗ theo giá đóng cửa M1 sau vài phút.
- Bộ lọc POI rất chặt (nằm trọn trong discount + FVG ngay sau + chưa bị chạm) → rất ít cơ hội.
- Cần người dùng quyết định trước khi chỉnh: xem câu hỏi trong cuộc trò chuyện.

Hình từng lệnh: `xauusd-2026-08-11-lenh.png`. Danh sách lệnh: `xauusd-2026-08-11-lenh.csv`.

## Lần 2 – tìm xu hướng lại mỗi ngày từ giá đóng cửa ngày liền trước (`--xu-huong moi-ngay`)
- Ngày giao dịch tách theo khoảng nghỉ cuối ngày của vàng (nến cuối 04:45, mở lại 05:00/06:00 giờ VN).
- Mỗi ngày bộ máy bắt đầu lại từ nến đóng cửa của ngày trước, chưa biết xu hướng cho tới khi đủ 2 đỉnh + 2 đáy.
- Phễu: 289 sóng → 62 POI hợp lệ → 11 lần chạm → 10 lệnh chờ → **3 lệnh khớp, thua cả 3, tổng −1.31R**.
- So với lần 1 (6 lệnh, −3.34R): ít lệnh hơn, lỗ ít hơn nhưng vẫn không có lệnh thắng; mẫu vẫn quá nhỏ.

## Lần 3 – xu hướng/POI trên H4, vào lệnh trên M15 (`--khung H4/M15`)
- H4 gộp từ M15, mốc ngày 17:00 New York (04:00 VN mùa hè / 05:00 mùa đông) như máy chủ MT5 phổ biến.
- Phễu: 18 sóng → 6 POI hợp lệ → **0 lần giá chạm POI trong phase 3 → 0 lệnh**.
- Tìm xu hướng lại mỗi ngày trên H4 (chỉ ~6 nến/ngày) → không đủ 2 đỉnh + 2 đáy → 0 lệnh.
- Tham khảo H1/M5: 52 sóng → 9 POI → 2 lệnh, thua cả 2 (SL cứng), −2.13R.
- Kết luận: 3,5 tháng dữ liệu quá ít cho khung H4; cần dữ liệu nhiều năm.
- Hình đỉnh/đáy/xu hướng H4: `xauusd-h4-xu-huong.png`.

## Lần 4 – chỉ dùng M15 cho cả xác định xu hướng/POI lẫn vào lệnh (`--khung M15/M15`)
- Tìm xu hướng liên tục: 6 lệnh, thắng 0, **−5.34R** (5 lệnh dính SL cứng, 1 hòa vốn).
- Tìm xu hướng lại mỗi ngày: 3 lệnh, thắng 1 (+4.0R, chốt TP2), thua 1 (−1.06R), hòa 1 → **+2.88R**.
- Giới hạn: trong một nến M15 không biết giá chạm điểm vào hay SL trước → mô phỏng giả định SL trước (thận trọng);
  2 lệnh "vào và dính SL trong cùng 1 nến" có thể bị đánh giá xấu hơn thực tế. Có thể dùng dữ liệu M1 để biết thứ tự chính xác.
- Mẫu 3–6 lệnh: chưa đủ để kết luận. Hình 7 lệnh (gộp cả hai cách): `xauusd-m15m15-lenh.png`.

## Lần 5 – chỉ khai thác PHASE 4, KHÔNG cần POI (`--vung discount`)
Thay vì chờ giá về POI hợp lệ: chỉ cần phase 3 hợp lệ (giá hồi chạm đường 50% sóng đẩy, vào discount/premium),
sau đó chờ tạo đáy/đỉnh trên khung vào lệnh rồi vào lệnh ở 1/2 râu như cũ. Tối đa 1 lệnh mỗi sóng.

| Khung | Tìm xu hướng | Lệnh | Thắng/Thua/Hòa | Tổng | TB thắng / TB thua | Sụt giảm lớn nhất |
|---|---|---|---|---|---|---|
| M15/M15 | lại mỗi ngày | 32 | 7/21/4 | **+9.42R** | +3.38R / −0.67R | −7.4R |
| M15/M15 | liên tục | 30 | 2/24/4 | −14.45R | +1.54R / −0.72R | −14.5R |
| M15/M1 | lại mỗi ngày | 106 | 11/95/0 | +1.22R | +4.31R / −0.49R | −19.4R |
| M15/M1 | liên tục | 90 | 4/86/0 | −31.29R | +3.37R / −0.52R | −33.0R |

Đường lợi nhuận: `xauusd-phase4-equity.png`. Lưu ý: đã thử nhiều biến thể trên cùng 3,5 tháng dữ liệu → dễ "khớp dữ liệu";
cần kiểm tra lại trên dữ liệu khác (năm khác, cặp khác) trước khi tin.

## Giờ giao phiên trong backtest
- Hàm `blocked()` cấm ±30 phút quanh giờ mở phiên Á (07:00), Âu (14:00 hè / 15:00 đông) và Mỹ (19:00 hè / 20:00 đông) giờ VN,
  có tính các tuần lệch giờ giữa châu Âu và Mỹ (đã kiểm tra bằng tay).
- Mặc định: chỉ cấm **khớp lệnh** trong giờ cấm (lệnh chờ bị huỷ nếu giá chạm điểm vào trong giờ cấm). Lệnh đang mở vẫn được quản lý bình thường.
- `--gio-cam-chat`: bỏ luôn các thiết lập có nến xác nhận đáy/đỉnh nằm trong giờ cấm.
  M15/M15 mỗi ngày, không cần POI: 29 lệnh, +7.15R, sụt giảm −6.25R (so với mặc định 32 lệnh, +9.42R, −7.4R).
- Chưa lọc giờ tin tức (người dùng sẽ báo giờ tin).

## Sửa lỗi bộ máy (phát hiện khi vẽ ngày 21/10/2026)
- Lỗi: nến vừa XÁC NHẬN xu hướng đồng thời đóng cửa phá đáy (xu hướng giảm) / phá đỉnh (xu hướng tăng) thì bộ máy bỏ qua
  việc phá vỡ đó (ngày 21/10 lúc 09:00: nến đóng 4108.91 < đáy 4111.80 nhưng không được tính). Đã sửa trong `tools/smc_engine.py`.
- Chạy lại sau khi sửa:

| Khung | Xu hướng | Vùng | Lệnh | Thắng/Thua/Hòa | Tổng | Sụt giảm |
|---|---|---|---|---|---|---|
| M15/M15 | mỗi ngày | không cần POI | 30 | 6/20/4 | **+5.48R** | −7.34R |
| M15/M15 | mỗi ngày | POI | 2 | 0/2/0 | −1.12R | −1.12R |
| M15/M15 | liên tục | không cần POI | 30 | 2/24/4 | −14.45R | −14.45R |
| M15/M15 | liên tục | POI | 6 | 0/6/0 | −5.34R | −5.34R |
| M15/M1 | mỗi ngày | không cần POI | 105 | 11/94/0 | +1.40R | −19.25R |
| M15/M1 | mỗi ngày | POI | 3 | 0/3/0 | −1.31R | −1.31R |
| M15/M1 | liên tục | không cần POI | 90 | 4/86/0 | −31.14R | −32.87R |
| M15/M1 | liên tục | POI | 6 | 0/6/0 | −3.34R | −3.34R |

## Lần 6 – M1 vừa xác định xu hướng vừa vào lệnh (`--khung M1/M1`)
| Xu hướng | Vùng | Lệnh | Thắng/Thua/Hòa | Tổng | TB/lệnh | Sụt giảm |
|---|---|---|---|---|---|---|
| mỗi ngày | không cần POI | 527 | 108/418/1 | **+33.23R** | +0.063R | −18.65R |
| liên tục | không cần POI | 533 | 108/424/1 | +35.45R | +0.067R | −19.20R |
| mỗi ngày | POI | 61 | 8/53/0 | −1.33R | −0.022R | −7.46R |
| liên tục | POI | 59 | 8/51/0 | −0.81R | −0.014R | −7.37R |

- Khoảng cách điểm vào → SL cứng trung bình chỉ 3.48 giá (SL cứng 3 giá chiếm phần lớn) → **rất nhạy với chi phí**:
  spread 0.3 → +33.2R; spread 0.5 → +2.7R; spread 0.8 → −43.1R (cùng 527 lệnh). Hình: `xauusd-m1m1-equity.png`.
- Tháng 9 âm ở mọi biến thể. ~150 lệnh/tháng (~7 lệnh/ngày) → trượt giá thực tế quan trọng.

## Lần 7 – khung M5 (`--khung M5/M5` và `M5/M1`), M5 gộp từ M1
| Khung | Xu hướng | Vùng | Lệnh | Thắng/Thua/Hòa | Tổng | Sụt giảm |
|---|---|---|---|---|---|---|
| M5/M5 | mỗi ngày | không cần POI | 101 | 13/87/1 | −16.56R | −22.35R |
| M5/M5 | liên tục | không cần POI | 99 | 14/84/1 | −13.28R | −19.07R |
| M5/M5 | mỗi ngày | POI | 11 | 0/11/0 | −8.59R | −8.59R |
| M5/M5 | liên tục | POI | 12 | 0/12/0 | −7.68R | −7.68R |
| M5/M1 | mỗi ngày | không cần POI | 251 | 30/221/0 | +0.97R | −38.44R |
| M5/M1 | liên tục | không cần POI | 232 | 28/204/0 | −3.82R | −39.94R |
| M5/M1 | mỗi ngày | POI | 22 | 2/20/0 | −3.78R | −5.95R |
| M5/M1 | liên tục | POI | 17 | 1/16/0 | −4.23R | −5.05R |

- M5/M5 mỗi ngày không cần POI: âm cả 4 tháng; spread 0.5 → −21.7R, 0.8 → −29.5R.

## Lần 8 – xác định xu hướng đầu ngày theo quy tắc mới (`--xu-huong moi-ngay --mo-dau gia-dong-cua`)
Nến đóng cửa ngày trước = Đỉnh 1 (đi xuống trước) / Đáy 1 (đi lên trước); xác nhận khi Đáy 2 / Đỉnh 2 xác nhận.
Ngoài ra sửa lỗi: ở chế độ chưa rõ xu hướng, một nến không thể vừa là đỉnh vừa là đáy kế tiếp. "Không cần POI", spread 0.3.

| Khung | Quy tắc mới (giá đóng cửa) | Quy tắc cũ (2 đỉnh + 2 đáy) |
|---|---|---|
| M15/M15 | 30 lệnh, **+3.91R**, sụt −7.29R | 30 lệnh, +4.83R, sụt −7.34R |
| M15/M1 | 101 lệnh, **+2.69R**, sụt −18.19R | 109 lệnh, +2.46R, sụt −18.82R |
| M5/M5 | 101 lệnh, **−21.05R** | 102 lệnh, −17.71R |
| M1/M1 | 526 lệnh, **+26.73R**, sụt −18.05R | 529 lệnh, +33.64R, sụt −16.14R |

Khác biệt nhỏ: quy tắc mở đầu ngày chỉ ảnh hưởng tới vài giờ đầu mỗi ngày.

## Lần 9 – PnD sau pha hồi không đủ đo từ đỉnh/đáy nông (quy tắc mới)
- M15/M15 mỗi ngày, không cần POI: 42 lệnh, thắng 8 thua 30 hòa 4, **+5.52R** (trước: 33 lệnh, +3.05R).
- M1/M1 mỗi ngày, không cần POI: 728 lệnh, thắng 155 thua 573, **+51.32R** (trước: 526 lệnh, +26.76R). Spread 0.3.

## Lần 10 – huỷ lệnh chờ nếu giá tạo đáy (SELL) / đỉnh (BUY) theo cách 1 trước khi khớp
- M15/M15 mỗi ngày, không cần POI: 34 lệnh, thắng 5 thua 26 hòa 3, **+2.03R**, sụt −8.47R (trước: 42 lệnh, +5.52R).
- M1/M1: 543 lệnh, thắng 108 thua 435, **+11.15R**, sụt −16.39R (trước: 728 lệnh, +51.32R).
- Lệnh 22/10 15:00 (+5.43R) vẫn giữ nguyên.

## Lần 11 – quy tắc xác nhận xu hướng mới khi chưa rõ / đi ngang (người dùng chốt qua ngày 16/09)
- GIẢM: có đỉnh thấp hơn → phá đáy gần nhất → đáy thấp hơn được xác nhận. TĂNG: phá đỉnh trước đó → đáy cao hơn được xác nhận.
- Khi tăng được xác nhận bằng "phá đỉnh rồi đáy cao hơn", pha hồi của pha đẩy đó đã xong → không vào lệnh trên sóng này.
- M15/M15 mỗi ngày, không cần POI: 20 lệnh, thắng 2 thua 18, **+1.51R**. M1/M1: 342 lệnh, thắng 69 thua 273, **+15.79R**.

## Lần 12 – sửa lỗi so sánh "đỉnh thấp hơn" (quy tắc giảm) + lỗi vẽ điểm cuối pha hồi
- Lỗi: quy tắc giảm đang kiểm tra ngược (đỉnh CAO hơn thay vì THẤP hơn) → ngày 06/11 bị xác nhận giảm sai lúc 14:45; nay xác nhận lúc 19:15.
- M15/M15 mỗi ngày, không cần POI: 25 lệnh, thắng 3 thua 19 hòa 3, **−1.37R**, sụt −5.43R.
- M1/M1: 444 lệnh, thắng 103 thua 341, **+44.94R**, sụt −10.16R.
- Hình cả ngày: `ca-ngay-2026-11-06.png`, `ca-ngay-2026-09-04.png`, `ca-ngay-2026-09-16.png`.

## Lần 13 – M1/M1, không cần POI, dữ liệu 01/2025 → 14/11/2026 (quy tắc mới nhất)
| Năm | Lệnh | Thắng/Thua | Tổng (spread 0.3) | spread 0.2 | spread 0.5 | Sụt giảm |
|---|---|---|---|---|---|---|
| 2025 | 1383 | 256/1122 | **−36.0R** | +6.1R | −120.3R | −36.0R |
| 2026 (đến 14/11) | 1324 | 266/1057 | **+101.6R** | +139.4R | +26.0R | −27.3R |

- Khoảng điểm vào → SL cứng trung vị ~3.2–3.4 giá → kết quả rất nhạy với chi phí.
- 2025 âm 8/12 tháng; 2026 dương 8/11 tháng. Đường lợi nhuận: `xauusd-m1m1-2025-2026-equity.png`.

## Lần 14 – mốc cấu trúc = đỉnh/đáy pha hồi ĐỦ; PnD đo từ mốc cấu trúc (đáy/đỉnh nông chỉ là thanh khoản)
Vào lệnh vẫn theo cách cũ (không cần POI: hồi chạm 50% → tạo đáy/đỉnh → 1/2 râu). Chưa có thứ tự ưu tiên thanh khoản/POI/FVG.
| Dữ liệu | Lệnh | Thắng/Thua | Tổng | Sụt giảm |
|---|---|---|---|---|
| M1/M1 2025 | 807 | 95/710 | −22.4R | −27.1R |
| M1/M1 2026 (đến 14/11) | 677 | 74/600 | +85.2R | −24.2R |
| M15/M15 08–11/2026 | 21 | 2/18 | −3.7R | |

## Lần 15 – thứ tự ưu tiên vùng vào lệnh (thanh khoản / POI / FVG / bình thường), M1/M1 (`tools/vao_lenh_uu_tien.py`)
| Năm | Lệnh | Thắng/Thua | Tổng (0.3) | 0.2 | 0.5 | Sụt giảm | Bỏ 5 lệnh lãi lớn nhất |
|---|---|---|---|---|---|---|---|
| 2025 | 388 | 39/347 | **−10.9R** | +0.7R | −34.1R | −23.5R | −36.8R |
| 2026 (đến 14/11) | 320 | 34/283 | **+64.7R** | +73.5R | +47.0R | −30.0R | −24.2R |
- Theo kiểu: 2025 – FVG 174 lệnh −6.3R, bình thường 126 −0.9R, POI 35 +3.2R, quét TK 49 −5.9R. 2026 – FVG 164 +71.4R, bình thường 88 +9.4R, POI 38 −12.6R, quét TK 28 −3.1R.
- Kết quả phụ thuộc vài lệnh rất lớn (30/01/2026 +43.9R); bỏ 5 lệnh lớn nhất thì cả hai năm đều âm.

## Lần 16 – thứ tự ưu tiên vùng (đã duyệt 9 trường hợp, `examples/42-...`), cả năm, M1/M1 và M15/M15
| Khung | Năm | Lệnh | Thắng/Thua/Hòa | Tổng (0.3) | Sụt giảm | Bỏ 3 lệnh lãi lớn nhất | Chi phí 1.0 |
|---|---|---|---|---|---|---|---|
| M1 | 2025 | 388 | 39/347/2 | −10.9R | −23.5R | −29.4R | |
| M1 | 2026 | 320 | 34/283/3 | +64.7R | −30.0R | −2.7R | |
| M15 | 2025 | 43 | 12/30/1 | **+28.0R** | −6.1R | +5.2R | +20.7R |
| M15 | 2026 | 38 | 6/26/6 | **+12.0R** | −6.5R | −9.9R | +7.3R |
- M15 dương cả hai năm và ít nhạy với chi phí (khoảng rủi ro trung vị 4–6 giá); nhưng chỉ ~40 lệnh/năm → mẫu nhỏ.
- M1 vẫn phụ thuộc vài lệnh rất lớn và chi phí. Đường lợi nhuận: `uu-tien-2025-2026-equity.png`.

## Lần 17 – bỏ quy tắc "huỷ lệnh chờ khi giá tạo đỉnh (cách 1) trước khi khớp" (người dùng yêu cầu 24/11)
Còn lại 3 điều kiện huỷ: giá chạm đỉnh cũ T trước khi khớp, nến đóng thân qua điểm thấp/cao nhất, khớp trong giờ cấm.

| Khung | Năm | Lệnh | Thắng/Thua/Hòa | Tổng (0.3) | Sụt giảm | Bỏ 3 lệnh lãi lớn nhất | Chi phí 1.0 | So với Lần 16 |
|---|---|---|---|---|---|---|---|---|
| M1 | 2025 | 847 | 110/734/3 | +87.4R | −15.9R | +46.2R | −90.3R | −10.9R |
| M1 | 2026 | 686 | 76/599/11 | +121.3R | −34.0R | +43.3R | −10.1R | +64.7R |
| M15 | 2025 | 73 | 21/51/1 | **+67.1R** | −5.3R | +41.9R | +54.8R | +28.0R |
| M15 | 2026 | 71 | 12/48/11 | **+26.3R** | −6.4R | +1.3R | +17.0R | +12.0R |

- Số lệnh M15 gần gấp đôi; các lệnh mới thêm có tổng dương (2025: 31 lệnh +38.1R; 2026: 34 lệnh +13.2R).
- M15 vẫn dương cả hai năm kể cả khi chi phí 1.0 và khi bỏ 3 lệnh lãi lớn nhất (2026 chỉ còn +1.3R).
- M1 vẫn rất nhạy với chi phí (âm khi chi phí 1.0) → tiếp tục ưu tiên M15.

### Vẽ toàn bộ lệnh M15 để duyệt (đã cập nhật theo Lần 18)
`backtest/lenh-m15/2025/` (73 lệnh) và `backtest/lenh-m15/2026/` (71 lệnh): mỗi ảnh 6 lệnh đánh số, `danh-sach.md` liệt kê từng lệnh.
Vẽ bằng `python3 tools/ve_lenh_m15.py nen_M1.csv ket_qua_M15.csv thu_muc_ra NHAN`.

## Lần 18 – chiều GIẢM khi chưa rõ xu hướng cũng phải có THÂN nến đóng dưới đáy gần nhất (người dùng xác nhận 24/11)
Trước đây chỉ cần đáy mới thấp hơn (tính theo râu). Sơ đồ các trường hợp xu hướng: `examples/43a/43b/43c-*.png`.

| Khung | Năm | Lệnh | Thắng/Thua/Hòa | Tổng (0.3) | Sụt giảm | Bỏ 3 lệnh lãi lớn nhất | Chi phí 1.0 | Lần 17 |
|---|---|---|---|---|---|---|---|---|
| M1 | 2025 | 845 | 105/738/2 | +83.3R | −21.4R | +42.1R | −93.8R | +87.4R |
| M1 | 2026 | 654 | 60/583/11 | +72.0R | −36.9R | −6.0R | −53.4R | +121.3R |
| M15 | 2025 | 68 | 19/49/0 | **+62.2R** | −5.3R | +36.9R | +50.6R | +67.1R |
| M15 | 2026 | 69 | 10/48/11 | **+13.3R** | −6.4R | −10.0R | +4.3R | +26.3R |

- Quy tắc chặt hơn làm kết quả giảm, rõ nhất ở 2026. M15 2025 vẫn vững; M15 2026 còn dương nhưng phụ thuộc 3 lệnh lớn.
