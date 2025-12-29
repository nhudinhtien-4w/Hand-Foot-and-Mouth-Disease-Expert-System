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
- 40 production rules chuẩn y khoa (4 luật chẩn đoán + 36 luật phân độ)
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

## � Hệ Luật Dẫn (Production Rules)

### Giai đoạn 1: Chẩn đoán lâm sàng (Xác định có bệnh HFMD)

#### R0-1: Chẩn đoán HFMD điển hình
```
IF (loét_miệng = TRUE OR phát_ban_tay_chân = TRUE)
   AND tuổi < 60 tháng
THEN có_bệnh_HFMD = TRUE
     độ_tin_cậy = "Cao"
```

#### R0-2: Chẩn đoán HFMD với yếu tố dịch tễ
```
IF (sốt = TRUE OR đau_họng = TRUE OR mệt_mỏi = TRUE)
   AND tuổi < 60 tháng
   AND (vùng_dịch = TRUE OR tiếp_xúc_bệnh_nhân = TRUE)
THEN có_bệnh_HFMD = TRUE
     độ_tin_cậy = "Trung bình"
     cần_xét_nghiệm = TRUE
```

#### R0-3: Chẩn đoán HFMD không điển hình
```
IF (giật_mình = TRUE OR rối_loạn_ý_thức = TRUE OR mạch_nhanh_bất_thường = TRUE)
   AND tuổi < 60 tháng
   AND (loét_miệng = FALSE AND phát_ban_tay_chân = FALSE)
THEN có_bệnh_HFMD = "Nghi ngờ - Thể không điển hình"
     cần_xét_nghiệm_RT_PCR = TRUE
```

#### R0-4: Cảnh báo biến chứng sớm
```
IF (bạch_cầu > 16 G/L OR đường_huyết > 160 mg% OR tiểu_cầu > 400 G/L)
   AND có_bệnh_HFMD = TRUE
THEN nguy_cơ_biến_chứng = "Cao"
     theo_dõi_chặt_chẽ = TRUE
```

---

### Giai đoạn 2: Phân độ bệnh HFMD

**Điều kiện tiên quyết:** `có_bệnh_HFMD = TRUE`

#### **Độ 1: Bệnh không biến chứng**

##### R1-1: Có loét miệng - không biến chứng
```
IF có_bệnh_HFMD = TRUE
   AND loét_miệng = TRUE
   AND (giật_mình = FALSE)
   AND (sốt < 39°C OR không_sốt = TRUE)
   AND (nôn_nhiều = FALSE)
   AND (mạch < 130 lần/phút OR không_đo_mạch = TRUE)
THEN độ_bệnh = 1
     dấu_hiệu = "Chỉ có loét miệng"
     biến_chứng = FALSE
```

##### R1-2: Có phát ban tay chân miệng - không biến chứng
```
IF có_bệnh_HFMD = TRUE
   AND phát_ban_tay_chân_miệng = TRUE
   AND (giật_mình = FALSE)
   AND (sốt < 39°C OR không_sốt = TRUE)
   AND (nôn_nhiều = FALSE)
   AND (mạch < 130 lần/phút OR không_đo_mạch = TRUE)
THEN độ_bệnh = 1
     dấu_hiệu = "Chỉ có phát ban tay chân miệng"
     biến_chứng = FALSE
```

---

#### **Độ 2a: Biến chứng thần kinh nhẹ (7 tiêu chuẩn)**

**Trẻ có ≥ 1 dấu hiệu sau:**

##### R2a-1: Giật mình trong bệnh sử (dưới 2 lần/30 phút, không ghi nhận lúc khám)
```
IF có_bệnh_HFMD = TRUE
   AND giật_mình_bệnh_sử = TRUE
   AND tần_suất_giật_mình < 2 lần/30 phút
   AND giật_mình_lúc_khám = FALSE
THEN độ_bệnh = "2a"
     dấu_hiệu = "Giật mình < 2 lần/30 phút (không ghi nhận lúc khám)"
```

##### R2a-2: Sốt trên 39°C
```
IF có_bệnh_HFMD = TRUE
   AND nhiệt_độ > 39°C
THEN độ_bệnh = "2a"
     dấu_hiệu = "Sốt > 39°C"
```

##### R2a-3: Sốt trên 2 ngày
```
IF có_bệnh_HFMD = TRUE
   AND thời_gian_sốt > 2 ngày
THEN độ_bệnh = "2a"
     dấu_hiệu = "Sốt kéo dài > 2 ngày"
```

##### R2a-4: Nôn ói nhiều
```
IF có_bệnh_HFMD = TRUE
   AND nôn_nhiều = TRUE
THEN độ_bệnh = "2a"
     dấu_hiệu = "Nôn ói nhiều"
```

##### R2a-5: Lừ đừ
```
IF có_bệnh_HFMD = TRUE
   AND lừ_đừ = TRUE
THEN độ_bệnh = "2a"
     dấu_hiệu = "Lừ đừ"
```

##### R2a-6: Khó ngủ
```
IF có_bệnh_HFMD = TRUE
   AND khó_ngủ = TRUE
THEN độ_bệnh = "2a"
     dấu_hiệu = "Khó ngủ"
```

##### R2a-7: Quấy khóc vô cớ
```
IF có_bệnh_HFMD = TRUE
   AND quấy_khóc_vô_cớ = TRUE
THEN độ_bệnh = "2a"
     dấu_hiệu = "Quấy khóc vô cớ"
```

---

#### **Độ 2b: Biến chứng thần kinh rõ (12 tiêu chuẩn)**

**Chia làm 2 nhóm dấu hiệu:**

---

##### **Nhóm 1 (4 tiêu chuẩn): Có ≥ 1 dấu hiệu**

##### R2b1-1: Giật mình ghi nhận lúc khám
```
IF có_bệnh_HFMD = TRUE
   AND giật_mình_lúc_khám = TRUE
THEN độ_bệnh = "2b"
     nhóm = "Nhóm 1"
     dấu_hiệu = "Giật mình ghi nhận lúc khám"
```

##### R2b1-2: Giật mình ≥ 2 lần/30 phút (bệnh sử)
```
IF có_bệnh_HFMD = TRUE
   AND giật_mình_bệnh_sử = TRUE
   AND tần_suất_giật_mình ≥ 2 lần/30 phút
THEN độ_bệnh = "2b"
     nhóm = "Nhóm 1"
     dấu_hiệu = "Giật mình ≥ 2 lần/30 phút"
```

##### R2b1-3: Giật mình kèm ngủ gà (bệnh sử)
```
IF có_bệnh_HFMD = TRUE
   AND giật_mình_bệnh_sử = TRUE
   AND ngủ_gà = TRUE
THEN độ_bệnh = "2b"
     nhóm = "Nhóm 1"
     dấu_hiệu = "Giật mình kèm ngủ gà"
```

##### R2b1-4: Giật mình kèm mạch nhanh > 130 (khi không sốt)
```
IF có_bệnh_HFMD = TRUE
   AND giật_mình_bệnh_sử = TRUE
   AND không_sốt = TRUE
   AND mạch > 130 lần/phút
THEN độ_bệnh = "2b"
     nhóm = "Nhóm 1"
     dấu_hiệu = "Giật mình + mạch nhanh > 130 (không sốt)"
```

---

##### **Nhóm 2 (8 tiêu chuẩn): Có ≥ 1 dấu hiệu**

##### R2b2-1: Dấu hiệu Nhóm 1 kèm sốt cao ≥ 39°C không đáp ứng thuốc hạ sốt
```
IF có_bệnh_HFMD = TRUE
   AND (giật_mình_lúc_khám = TRUE 
        OR tần_suất_giật_mình ≥ 2 lần/30 phút
        OR (giật_mình_bệnh_sử = TRUE AND ngủ_gà = TRUE)
        OR (giật_mình_bệnh_sử = TRUE AND không_sốt = TRUE AND mạch > 130 lần/phút))
   AND nhiệt_độ ≥ 39°C
   AND đáp_ứng_thuốc_hạ_sốt = FALSE
THEN độ_bệnh = "2b"
     nhóm = "Nhóm 2"
     dấu_hiệu = "Nhóm 1 + Sốt cao ≥ 39°C kháng thuốc"
```

##### R2b2-2: Mạch nhanh > 150 lần/phút (khi không sốt)
```
IF có_bệnh_HFMD = TRUE
   AND không_sốt = TRUE
   AND mạch > 150 lần/phút
THEN độ_bệnh = "2b"
     nhóm = "Nhóm 2"
     dấu_hiệu = "Mạch nhanh > 150 (không sốt)"
```

##### R2b2-3: Thất điều vận động
```
IF có_bệnh_HFMD = TRUE
   AND (run_chi = TRUE OR run_người = TRUE OR đi_loạng_choạng = TRUE)
THEN độ_bệnh = "2b"
     nhóm = "Nhóm 2"
     dấu_hiệu = "Thất điều: run chi, run người, đi loạng choạng"
```

##### R2b2-4: Rối loạn nhãn cầu
```
IF có_bệnh_HFMD = TRUE
   AND (rung_giật_nhãn_cầu = TRUE OR lác_mắt = TRUE)
THEN độ_bệnh = "2b"
     nhóm = "Nhóm 2"
     dấu_hiệu = "Rung giật nhãn cầu, lác mắt"
```

##### R2b2-5: Yếu hoặc liệt chi
```
IF có_bệnh_HFMD = TRUE
   AND (yếu_chi = TRUE OR liệt_chi = TRUE)
THEN độ_bệnh = "2b"
     nhóm = "Nhóm 2"
     dấu_hiệu = "Yếu hoặc liệt chi"
```

##### R2b2-6: Liệt thần kinh sọ
```
IF có_bệnh_HFMD = TRUE
   AND (nuốt_sặc = TRUE OR thay_đổi_giọng_nói = TRUE)
THEN độ_bệnh = "2b"
     nhóm = "Nhóm 2"
     dấu_hiệu = "Liệt thần kinh sọ: nuốt sặc, thay đổi giọng nói"
```

##### R2b2-7: Tăng trương lực cơ
```
IF có_bệnh_HFMD = TRUE
   AND tăng_trương_lực_cơ = TRUE
THEN độ_bệnh = "2b"
     nhóm = "Nhóm 2"
     dấu_hiệu = "Tăng trương lực cơ"
```

##### R2b2-8: Rối loạn tri giác
```
IF có_bệnh_HFMD = TRUE
   AND (Glasgow < 10 OR thang_điểm_AVPU = "P")
THEN độ_bệnh = "2b"
     nhóm = "Nhóm 2"
     dấu_hiệu = "Rối loạn tri giác (Glasgow < 10 hoặc AVPU = P)"
```

---

#### **Độ 3: Rối loạn thần kinh thực vật nặng (8 tiêu chuẩn)**

**Trẻ có ít nhất một trong các dấu hiệu sau:**

##### R3-1: Mạch nhanh > 170 lần/phút (khi không sốt)
```
IF có_bệnh_HFMD = TRUE
   AND không_sốt = TRUE
   AND mạch > 170 lần/phút
THEN độ_bệnh = 3
     dấu_hiệu = "Mạch nhanh > 170/phút (không sốt)"
     nguy_cơ = "Rối loạn thần kinh thực vật"
```

##### R3-2: Mạch chậm
```
IF có_bệnh_HFMD = TRUE
   AND mạch_chậm = TRUE
THEN độ_bệnh = 3
     dấu_hiệu = "Mạch chậm"
     lưu_ý = "Cần đánh giá thêm huyết áp và tri giác"
     nguy_cơ = "Rối loạn thần kinh thực vật"
```

##### R3-3: Tăng huyết áp tâm thu (trẻ < 12 tháng)
```
IF có_bệnh_HFMD = TRUE
   AND tuổi < 12 tháng
   AND huyết_áp_tâm_thu ≥ 100 mmHg
THEN độ_bệnh = 3
     dấu_hiệu = "Tăng HA tâm thu ≥ 100 mmHg (< 12 tháng)"
```

##### R3-4: Tăng huyết áp tâm thu (12 đến < 24 tháng)
```
IF có_bệnh_HFMD = TRUE
   AND tuổi ≥ 12 tháng AND tuổi < 24 tháng
   AND huyết_áp_tâm_thu ≥ 110 mmHg
THEN độ_bệnh = 3
     dấu_hiệu = "Tăng HA tâm thu ≥ 110 mmHg (12-24 tháng)"
```

##### R3-5: Tăng huyết áp tâm thu (≥ 24 tháng)
```
IF có_bệnh_HFMD = TRUE
   AND tuổi ≥ 24 tháng
   AND huyết_áp_tâm_thu ≥ 115 mmHg
THEN độ_bệnh = 3
     dấu_hiệu = "Tăng HA tâm thu ≥ 115 mmHg (≥ 24 tháng)"
```

##### R3-6: Thở nhanh
```
IF có_bệnh_HFMD = TRUE
   AND thở_nhanh = TRUE
THEN độ_bệnh = 3
     dấu_hiệu = "Thở nhanh"
```

##### R3-7: Khó thở hoặc thở rít
```
IF có_bệnh_HFMD = TRUE
   AND (khó_thở = TRUE OR thở_rít = TRUE)
THEN độ_bệnh = 3
     dấu_hiệu = "Khó thở hoặc thở rít"
```

##### R3-8: SpO2 < 94%
```
IF có_bệnh_HFMD = TRUE
   AND SpO2 < 94%
THEN độ_bệnh = 3
     dấu_hiệu = "SpO2 < 94%"
```

##### R3-9: Rối loạn vận mạch
```
IF có_bệnh_HFMD = TRUE
   AND (da_nổi_bông = TRUE OR vân_tím = TRUE)
   AND (vã_mồ_hôi = TRUE OR chi_lạnh = TRUE)
THEN độ_bệnh = 3
     dấu_hiệu = "Rối loạn vận mạch: da nổi bông/vân tím + mồ hôi/chi lạnh"
```

---

#### **Độ 4: Suy hô hấp tuần hoàn nặng (7 tiêu chuẩn)**

**Trẻ có ít nhất một trong các dấu hiệu sau:**

##### R4-1: Ngưng thở
```
IF có_bệnh_HFMD = TRUE
   AND ngưng_thở = TRUE
THEN độ_bệnh = 4
     dấu_hiệu = "Ngưng thở"
     cấp_cứu = "KHẨN CẤP"
```

##### R4-2: Rối loạn nhịp thở
```
IF có_bệnh_HFMD = TRUE
   AND rối_loạn_nhịp_thở = TRUE
THEN độ_bệnh = 4
     dấu_hiệu = "Rối loạn nhịp thở"
     cấp_cứu = "KHẨN CẤP"
```

##### R4-3: Tím tái
```
IF có_bệnh_HFMD = TRUE
   AND tím_tái = TRUE
THEN độ_bệnh = 4
     dấu_hiệu = "Tím tái"
     cấp_cứu = "KHẨN CẤP"
```

##### R4-4: SpO2 < 92%
```
IF có_bệnh_HFMD = TRUE
   AND SpO2 < 92%
THEN độ_bệnh = 4
     dấu_hiệu = "SpO2 < 92%"
     cấp_cứu = "KHẨN CẤP"
```

##### R4-5: Phù phổi cấp
```
IF có_bệnh_HFMD = TRUE
   AND phù_phổi_cấp = TRUE
THEN độ_bệnh = 4
     dấu_hiệu = "Phù phổi cấp"
     cấp_cứu = "KHẨN CẤP"
```

##### R4-6: Sốc (có 1 trong 3 tiêu chuẩn)
```
IF có_bệnh_HFMD = TRUE
   AND (
        (mạch_không_bắt = TRUE AND HA_không_đo_được = TRUE)
        OR (tuổi < 12 tháng AND HA_tâm_thu < 70 mmHg)
        OR (tuổi ≥ 12 tháng AND HA_tâm_thu < 80 mmHg)
        OR (hiệu_áp ≤ 25 mmHg)
   )
THEN độ_bệnh = 4
     dấu_hiệu = "Sốc"
     chi_tiết = "Mạch không bắt + HA không đo được; hoặc tụt HA theo tuổi; hoặc HA kẹp"
     cấp_cứu = "KHẨN CẤP"
```

##### R4-7: Ngưng thở, thở nặc (Phụ lục 1)
```
IF có_bệnh_HFMD = TRUE
   AND (ngưng_thở_phụ_lục = TRUE OR thở_nặc = TRUE)
THEN độ_bệnh = 4
     dấu_hiệu = "Ngưng thở, thở nặc (ghi nhận tại Phụ lục 1)"
     cấp_cứu = "KHẨN CẤP"
```

---

### Nguyên tắc áp dụng luật

1. **Conflict Resolution**: Khi nhiều luật cùng kích hoạt, chọn độ bệnh cao nhất
2. **Forward Chaining**: Áp dụng tuần tự từ R0 (chẩn đoán) → R1-R4 (phân độ)
3. **Priority**: Độ 4 > Độ 3 > Độ 2b > Độ 2a > Độ 1
4. **Điều kiện tiên quyết**: Phải xác định `có_bệnh_HFMD = TRUE` trước khi phân độ

### Tổng hợp số lượng luật

- **Giai đoạn 1 - Chẩn đoán**: 4 luật (R0-1 → R0-4)
- **Giai đoạn 2 - Phân độ**: 36 luật
  - Độ 1: 2 luật
  - Độ 2a: 7 luật  
  - Độ 2b: 12 luật (Nhóm 1: 4 luật, Nhóm 2: 8 luật)
  - Độ 3: 9 luật
  - Độ 4: 7 luật
- **Tổng cộng**: 40 production rules

---

## �📄 License

MIT License - xem file [LICENSE](LICENSE) để biết thêm chi tiết.

---

## 📞 Liên hệ

- **GitHub**: [@your-username](https://github.com/your-username)
- **Email**: your.email@example.com