# CS217 Knowledge Base - Hệ Chuyên Gia Chẩn Đoán Bệnh Tay Chân Miệng

Hệ thống chuyên gia chẩn đoán bệnh **Tay-Chân-Miệng (HFMD)** cho trẻ em, phân độ bệnh từ 1 đến 4 theo tài liệu y khoa.

---

## 📋 Tổng quan

### Chức năng chính
- ✅ Nhập triệu chứng và chỉ số sinh tồn bệnh nhân
- ✅ Tự động phân độ bệnh: **Độ 1, 2a, 2b1, 2b2, 3, 4**
- ✅ Giải thích quyết định dựa trên luật y khoa
- ✅ Hỗ trợ cả web interface và API

---

## 🚀 Cài đặt

### 1. Clone Repository

```bash
git clone https://github.com/your-username/CS217-Knowledge-Base.git
cd CS217-Knowledge-Base
```

### 2. Tạo Virtual Environment

```bash
# Tạo virtual environment
python -m venv cs217_venv

# Kích hoạt (Windows)
cs217_venv\Scripts\activate

# Kích hoạt (Linux/Mac)
source cs217_venv/bin/activate
```

### 3. Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies chính:**
- Flask==3.0.0
- Flask-CORS==4.0.0
- python-dotenv==1.0.0

---

## 💻 Chạy ứng dụng

```bash
# Chạy Flask server
python app.py

```

---

### Web Interface

1. Mở `http://localhost:5000` (hoặc deployed URL)
2. Nhập thông tin bệnh nhân, triệu chứng người bệnh
3. Hệ thống tự động phân tích, đưa ra kết quả và gợi ý pháp đồ điều trị

## 📚 Tài liệu tham khảo

- [Hướng dẫn chẩn đoán bệnh TCM - Bộ Y Tế](...)
- [Forward Chaining Algorithm](https://en.wikipedia.org/wiki/Forward_chaining)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## 👥 Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng:
1. Fork repo
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

---

