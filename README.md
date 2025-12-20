# CS217 Knowledge Base - Hệ Chuyên Gia Chẩn Đoán Bệnh Tay Chân Miệng

Hệ thống chuyên gia chẩn đoán bệnh **Tay-Chân-Miệng (HFMD)** cho trẻ em, phân độ bệnh từ 1 đến 4 theo tài liệu y khoa.

---

## 📋 Tổng quan

### Chức năng chính
- ✅ Nhập triệu chứng và chỉ số sinh tồn bệnh nhân
- ✅ Tự động phân độ bệnh: **Độ 1, 2a, 2b1, 2b2, 3, 4**
- ✅ Giải thích quyết định dựa trên luật y khoa
- ✅ Hỗ trợ cả web interface và API

### Công nghệ sử dụng

**Frontend:**
- HTML5, CSS3, Vanilla JavaScript
- Không cần framework - chạy trực tiếp trên trình duyệt

**Backend:**
- Python 3.11+
- Flask (Web Framework)
- Forward Chaining Inference Engine
- Production Rules từ `data/rules.json`

**Knowledge Base:**
- 36 production rules chuẩn y khoa
- Format JSON, dễ bảo trì và mở rộng
- Priority-based conflict resolution

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

### Option 1: Chỉ Frontend (Standalone)

```bash
# Mở file trong trình duyệt
start frontend/index.html

# Hoặc dùng Live Server trong VS Code
# Right-click index.html → Open with Live Server
```

### Option 2: Full Stack (Frontend + Backend)

```bash
# Chạy Flask server
python app.py

# Server sẽ chạy tại: http://localhost:5000
# Mở trình duyệt và truy cập http://localhost:5000
```

---

## 🌐 Deploy

### Deploy Frontend (Static hosting)

**GitHub Pages:**
```bash
# Đẩy code lên GitHub
git push origin main

# Enable GitHub Pages trong Settings → Pages
# Chọn branch: main, folder: / (root)
```

**Netlify/Vercel:**
- Kéo thả thư mục `frontend/` vào Netlify/Vercel
- Tự động deploy

### Deploy Backend (Python Flask)

**1. Render.com (Miễn phí)**

```bash
# Tạo file Procfile (đã có sẵn)
web: gunicorn app:app

# Push lên GitHub và connect với Render
```

**2. PythonAnywhere**

```bash
# Upload files lên PythonAnywhere
# Cấu hình WSGI file trỏ đến app.py
```

**3. Heroku**

```bash
# Cài Heroku CLI
heroku login
heroku create cs217-hfmd-diagnosis

# Deploy
git push heroku main

# Mở app
heroku open
```

**4. VPS (Ubuntu)**

```bash
# Cài đặt
sudo apt update
sudo apt install python3-pip nginx

# Clone repo
git clone https://github.com/your-username/CS217-Knowledge-Base.git
cd CS217-Knowledge-Base

# Install dependencies
pip3 install -r requirements.txt

# Chạy với Gunicorn
gunicorn --bind 0.0.0.0:5000 app:app

# Cấu hình Nginx reverse proxy
sudo nano /etc/nginx/sites-available/cs217
# ... cấu hình proxy_pass đến localhost:5000
```

---

### Web Interface

1. Mở `http://localhost:5000` (hoặc deployed URL)
2. Nhập thông tin bệnh nhân:
   - **Độ 1**: Phát ban, loét miệng
   - **Độ 2a**: Sốt cao, giật mình, triệu chứng kèm theo
   - **Độ 2b**: Biến chứng thần kinh
   - **Độ 3**: Rối loạn tuần hoàn
   - **Độ 4**: Suy hô hấp, sốc
3. Hệ thống tự động phân tích và đưa ra kết quả

### API Endpoint

**POST /api/diagnose**

```bash
curl -X POST http://localhost:5000/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{
    "fever_temp_c": 39.5,
    "spo2": 88,
    "rash_hand_foot_mouth": true,
    "age_months": 36
  }'
```

**Response:**
```json
{
  "disease_level": "4",
  "priority": 5,
  "matched_rules": ["grade_4_spo2"],
  "explanation": "SpO2 < 92% - Độ 4"
}
```

---

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

## 📄 License

MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết.

---

## 📞 Liên hệ

- **GitHub**: [@your-username](https://github.com/your-username)
- **Email**: your.email@example.com