"""
Flask Web Application - HFMD Diagnosis System
Hệ thống chẩn đoán bệnh Tay-Chân-Miệng với 2 giai đoạn
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sys
import os
import json

# Thêm backend vào path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from simple_inference import SimpleInferenceEngine

# Get base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))
CORS(app)

# Khởi tạo 2 inference engines
diagnosis_engine = SimpleInferenceEngine(os.path.join(BASE_DIR, 'data', 'diagnosis_rules.json'))
classification_engine = SimpleInferenceEngine(os.path.join(BASE_DIR, 'data', 'classification_level_rules.json'))

@app.route('/')
def index():
    """Trang chủ"""
    return render_template('index.html')

@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    """
    API endpoint giai đoạn 1: Chẩn đoán lâm sàng
    Kiểm tra bệnh nhân có HFMD không
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Không có dữ liệu đầu vào'
            }), 400
        
        # Chẩn đoán bằng diagnosis engine
        result = diagnosis_engine.diagnose(data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/classify', methods=['POST'])
def classify():
    """
    API endpoint giai đoạn 2: Phân độ bệnh
    Chỉ chạy khi has_hfmd = TRUE
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Không có dữ liệu đầu vào'
            }), 400
        
        # Phân độ bằng classification engine
        result = classification_engine.diagnose(data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/diagnosis-questions', methods=['GET'])
def get_diagnosis_questions():
    """
    API lấy danh sách câu hỏi chẩn đoán
    """
    try:
        with open(os.path.join(BASE_DIR, 'data', 'diagnosis_rules.json'), 'r', encoding='utf-8') as f:
            rules = json.load(f)
            
        questions = rules.get('clinical_questions', {})
        
        return jsonify({
            'success': True,
            'questions': questions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/treatment', methods=['POST'])
def get_treatment():
    """
    API endpoint: Lấy gợi ý điều trị theo độ bệnh
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Không có dữ liệu đầu vào'
            }), 400
        
        disease_level = data.get('disease_level')
        
        if not disease_level:
            return jsonify({
                'success': False,
                'error': 'Thiếu thông tin độ bệnh'
            }), 400
        
        # Đọc file treatment.json
        with open(os.path.join(BASE_DIR, 'data', 'treatment.json'), 'r', encoding='utf-8') as f:
            treatment_data = json.load(f)
        
        # Tìm treatment rule theo disease_level
        treatment_rule = None
        for rule in treatment_data.get('treatment_rules', []):
            if rule.get('disease_level') == disease_level:
                treatment_rule = rule
                break
        
        if not treatment_rule:
            return jsonify({
                'success': False,
                'error': f'Không tìm thấy phác đồ điều trị cho độ {disease_level}'
            }), 404
        
        return jsonify({
            'success': True,
            'treatment': treatment_rule
        })
        
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
        diag_stats = diagnosis_engine.get_stats()
        class_stats = classification_engine.get_stats()
        
        return jsonify({
            'success': True,
            'stats': {
                'diagnosis': diag_stats,
                'classification': class_stats
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🏥 HFMD Diagnosis System - 2 Phase System")
    print("=" * 60)
    print(f"✅ Diagnosis Engine: {len(diagnosis_engine.rules)} rules")
    print(f"✅ Classification Engine: {len(classification_engine.rules)} rules")
    print("=" * 60)
    print("🌐 Server running at: http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
