"""
Flask Web Application - TCM Diagnosis System
Hệ thống chẩn đoán bệnh Tay-Chân-Miệng trên web
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
import os

# Thêm backend vào path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from simple_inference import SimpleInferenceEngine

# Get base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))
CORS(app)  # Cho phép CORS

# Khởi tạo inference engine với rules.json mới
engine = SimpleInferenceEngine(os.path.join(BASE_DIR, 'data', 'rules.json'))

@app.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html')

@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    """
    API endpoint chẩn đoán
    
    Request body (theo rules.json mới):
    {
        "rash_hand_foot_mouth": true,
        "mouth_ulcer": true,
        "fever_temp_c": 39.5,
        "fever_days": 3,
        "startle_per_30min": 1,
        "startle_observed": false,
        "vomiting_many": true,
        "spo2": 95,
        "age_months": 24,
        ...
    }
    
    Response:
    {
        "success": true,
        "disease_level": "2a",
        "matched_rules": ["grade_2a_2"],
        "explanation": "...",
        "priority": 1
    }
    """
    try:
        # Lấy dữ liệu từ request
        data = request.json
        
        # Validate
        if not data:
            return jsonify({
                'success': False,
                'error': 'Không có dữ liệu đầu vào'
            }), 400
        
        # Chẩn đoán bằng inference engine
        result = engine.diagnose(data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    API lấy thống kê knowledge base
    """
    try:
        stats = engine.get_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/rules', methods=['GET'])
def get_rules():
    """
    API lấy toàn bộ rules
    """
    try:
        return jsonify({
            'success': True,
            'rules': engine.rules,
            'total': len(engine.rules)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def get_degree_name(degree):
    """Lấy tên đầy đủ của độ bệnh"""
    degree_names = {
        '1': 'Độ 1 - Bệnh không biến chứng',
        '2a': 'Độ 2a - Có nguy cơ biến chứng thần kinh',
        '2b1': 'Độ 2b1 - Biến chứng thần kinh không nặng',
        '2b2': 'Độ 2b2 - Biến chứng thần kinh nặng',
        '3': 'Độ 3 - Biến chứng tim mạch giai đoạn sớm',
        '4': 'Độ 4 - Biến chứng tim mạch giai đoạn muộn',
        'Không xác định': 'Không xác định'
    }
    return degree_names.get(degree, degree)

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🏥 TCM DIAGNOSIS WEB APPLICATION")
    print("="*80)
    print("Starting server...")
    print("Open browser: http://localhost:5000")
    print("="*80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
