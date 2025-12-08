# CS217 Knowledge Base - DMN Decision System

Hệ thống quyết định phân độ bệnh TCM (Tay-Chân-Miệng) dựa trên DMN (Decision Model and Notation) với Hit Policy: Priority.

## Cách sử dụng

### 1. Chạy ứng dụng

Mở file `frontend/index.html` trực tiếp trong trình duyệt. Không cần web server vì đây là ứng dụng thuần HTML/CSS/JS.

```bash
# Mở bằng trình duyệt mặc định (Windows)
start frontend/index.html

# Hoặc dùng VS Code Live Server
# Right-click vào index.html → Open with Live Server
```

### 2. Nhập dữ liệu bệnh nhân

- Tick các checkbox cho các triệu chứng có/không
- Nhập số liệu cho các trường số (nhiệt độ, mạch, SpO₂, v.v.)
- Hệ thống tự động tính toán và hiển thị kết quả phân độ

### 3. Tính toán HR (không sốt)

1. Nhập "Mạch đo được" (bpm)
2. Nhập "Nhiệt độ tối đa" (°C)
3. Click nút "Tính HR (không sốt)"
4. Giá trị HR điều chỉnh sẽ tự động được tính: `HR_no_fever = HR_measured - max(0, (TempC - 38) * 10)`

### 4. Cập nhật Rules

Trong khung "Rules JSON", bạn có thể:
- Chỉnh sửa rules hiện tại
- Dán toàn bộ JSON rules đầy đủ từ file `data/rules.json`
- Rules sẽ được validate và áp dụng ngay khi bạn chỉnh sửa

### 5. Xuất dữ liệu

Click nút "Tải CSV hàng ca bệnh" để xuất dữ liệu bệnh nhân ra file CSV theo format 40 cột chuẩn.

## Logic Engine

### Cấu trúc Rule

Mỗi rule có format:

```json
{
  "id": "4-01",
  "result": "4",
  "priority": 400,
  "when": {
    "SpO₂": "<92"
  },
  "notes": "SpO₂ <92% ⇒ Độ 4",
  "source": "QĐ 292 – II.6 (Độ 4)"
}
```

### Priority Map

- Độ 4: 400 điểm (cao nhất)
- Độ 3: 300 điểm
- Độ 2b: 250 điểm
- Độ 2a: 200 điểm
- Độ 1: 100 điểm

### Cú pháp điều kiện

Engine hỗ trợ nhiều loại điều kiện:

1. **Số so sánh**: `<92`, `>=39`, `<=130`
2. **Boolean**: `true`, `false`, `không`
3. **Tập hợp**: `{A,V,P}` (chứa một trong các giá trị)
4. **Tốc độ**: `>2/h` (số lần/giờ)
5. **Tuổi**: `<12m`, `≥12m`
6. **String exact**: so sánh chính xác

## Mở rộng cho Backend

Cấu trúc hiện tại đã được tổ chức sẵn cho việc tích hợp backend:

### Đề xuất kiến trúc:

```
CS217-Knowledge-Base/
├── frontend/           # (đã có)
├── assets/            # (đã có)
├── data/              # (đã có)
├── backend/           # (sẽ thêm)
│   ├── api/
│   │   ├── routes/
│   │   ├── controllers/
│   │   └── middleware/
│   ├── services/
│   │   ├── decision-engine.js
│   │   └── rules-manager.js
│   ├── models/
│   │   ├── Patient.js
│   │   └── Rule.js
│   ├── config/
│   │   └── database.js
│   └── server.js
├── tests/             # Unit tests
└── docs/              # Documentation
```

### API Endpoints đề xuất:

```
POST   /api/evaluate          # Đánh giá bệnh nhân
GET    /api/rules             # Lấy danh sách rules
POST   /api/rules             # Thêm rule mới
PUT    /api/rules/:id         # Cập nhật rule
DELETE /api/rules/:id         # Xóa rule
GET    /api/patients          # Lấy danh sách bệnh nhân
POST   /api/patients          # Lưu ca bệnh mới
```

## Tương lai

- [ ] Tích hợp backend (Node.js/Express)
- [ ] Database (MongoDB/PostgreSQL)
- [ ] Authentication & Authorization
- [ ] Lưu trữ lịch sử ca bệnh
- [ ] Export PDF report
- [ ] Dashboard phân tích thống kê
- [ ] Multi-language support