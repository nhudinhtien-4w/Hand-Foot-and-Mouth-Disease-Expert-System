"""
Hệ thống chẩn đoán TCM - Pure Python (không cần Experta)
Tập trung: Rule-based Diagnosis với Priority-based Selection
Không có: Treatment, Database, External Dependencies
"""

import json
from typing import Dict, List, Optional, Any


class Rule:
    """Biểu diễn một luật chẩn đoán"""
    
    def __init__(self, rule_id: str, degree: str, priority: int, 
                 conditions: Dict, description: str = "", source: str = ""):
        self.rule_id = rule_id
        self.degree = degree
        self.priority = priority
        self.conditions = conditions
        self.description = description
        self.source = source
    
    def evaluate(self, data: Dict) -> bool:
        """
        Kiểm tra xem rule có match với dữ liệu không
        
        Returns:
            bool: True nếu tất cả điều kiện đều thỏa mãn
        """
        for field, condition in self.conditions.items():
            if not self._check_condition(data, field, condition):
                return False
        return True
    
    def _check_condition(self, data: Dict, field: str, condition: Any) -> bool:
        """Kiểm tra một điều kiện đơn"""
        # Nếu field không có trong data, coi như False
        if field not in data:
            return False
        
        value = data[field]
        
        # Boolean check
        if isinstance(condition, bool):
            return value == condition
        
        # String comparison check
        if isinstance(condition, str):
            # Numeric comparisons
            if condition.startswith('>='):
                threshold = float(condition[2:])
                return float(value) >= threshold
            elif condition.startswith('<='):
                threshold = float(condition[2:])
                return float(value) <= threshold
            elif condition.startswith('>'):
                threshold = float(condition[1:])
                return float(value) > threshold
            elif condition.startswith('<'):
                threshold = float(condition[1:])
                return float(value) < threshold
            elif condition.startswith('='):
                threshold = float(condition[1:])
                return float(value) == threshold
            else:
                # Exact string match
                return str(value) == condition
        
        # Numeric comparison
        if isinstance(condition, (int, float)):
            return value == condition
        
        # List/set check (value in list)
        if isinstance(condition, (list, set)):
            return value in condition
        
        return False
    
    def __repr__(self):
        return f"Rule({self.rule_id}, Độ {self.degree}, P:{self.priority})"


class DiagnosisEngine:
    """
    Engine chẩn đoán với Priority-based Selection
    """
    
    def __init__(self):
        self.rules: List[Rule] = []
        self._load_default_rules()
    
    def _load_default_rules(self):
        """Load các rules mặc định"""
        
        # ==================== ĐỘ 4 - PRIORITY 400 ====================
        
        self.add_rule(Rule(
            '04-01', '4', 400,
            {'spo2': '<92'},
            'SpO₂ <92%',
            'QĐ 292 – II.6'
        ))
        
        self.add_rule(Rule(
            '04-02', '4', 400,
            {'apnea': True},
            'Ngưng thở',
            'QĐ 292 – II.6'
        ))
        
        self.add_rule(Rule(
            '04-03', '4', 400,
            {'resp_irregular_severe': True},
            'Rối loạn nhịp thở nặng',
            'QĐ 292 – II.6'
        ))
        
        self.add_rule(Rule(
            '04-04', '4', 400,
            {'pulm_edema_pink_froth': True},
            'Phù phổi – sùi bọt hồng',
            'QĐ 292 – II.6'
        ))
        
        self.add_rule(Rule(
            '04-05', '4', 400,
            {'lung_rales_wet': True},
            'Phù phổi – ran ẩm',
            'QĐ 292 – II.6'
        ))
        
        self.add_rule(Rule(
            '04-06', '4', 400,
            {'coma': True},
            'Hôn mê',
            'QĐ 292 – II.6'
        ))
        
        self.add_rule(Rule(
            '04-07', '4', 400,
            {'gcs': '<=8'},
            'GCS ≤8',
            'QĐ 292 – II.6'
        ))
        
        self.add_rule(Rule(
            '04-08', '4', 400,
            {'avpu_level': ['P', 'U']},
            'AVPU = P hoặc U',
            'QĐ 292 – II.6'
        ))
        
        self.add_rule(Rule(
            '04-09', '4', 400,
            {'lactate': '>=4'},
            'Lactate ≥4 mmol/L',
            'QĐ 292 – II.6'
        ))
        
        # ==================== ĐỘ 3 - PRIORITY 300 ====================
        
        self.add_rule(Rule(
            '03-01', '3', 300,
            {'startle_hist_30min': '>=2'},
            'Giật mình ≥2 lần/30 phút',
            'QĐ 292 – II.5'
        ))
        
        self.add_rule(Rule(
            '03-02', '3', 300,
            {'somnolent': True},
            'Li bì',
            'QĐ 292 – II.5'
        ))
        
        self.add_rule(Rule(
            '03-03', '3', 300,
            {'nystagmus': True},
            'Rung giật nhãn cầu',
            'QĐ 292 – II.5'
        ))
        
        self.add_rule(Rule(
            '03-04', '3', 300,
            {'ataxia': True},
            'Mất điều hòa',
            'QĐ 292 – II.5'
        ))
        
        self.add_rule(Rule(
            '03-05', '3', 300,
            {'tremor': True},
            'Run',
            'QĐ 292 – II.5'
        ))
        
        self.add_rule(Rule(
            '03-06', '3', 300,
            {'limb_weakness': True},
            'Liệt chi',
            'QĐ 292 – II.5'
        ))
        
        self.add_rule(Rule(
            '03-07', '3', 300,
            {'cranial_nerve_palsy': True},
            'Liệt dây thần kinh sọ',
            'QĐ 292 – II.5'
        ))
        
        self.add_rule(Rule(
            '03-08', '3', 300,
            {'hypertonia': True},
            'Tăng trương lực cơ',
            'QĐ 292 – II.5'
        ))
        
        self.add_rule(Rule(
            '03-09', '3', 300,
            {'seizure': True},
            'Co giật',
            'QĐ 292 – II.5'
        ))
        
        # ==================== ĐỘ 2b - PRIORITY 250 ====================
        
        # Rule phức tạp: Mạch nhanh phụ thuộc tuổi
        self.add_rule(Rule(
            '2b-01', '2b', 250,
            {'hr_no_fever': '>150', 'age_months': '<12'},
            'Mạch >150 bpm (trẻ <12 tháng)',
            'QĐ 292 – II.4.b'
        ))
        
        self.add_rule(Rule(
            '2b-02', '2b', 250,
            {'hr_no_fever': '>130', 'age_months': '>=12'},
            'Mạch >130 bpm (trẻ ≥12 tháng)',
            'QĐ 292 – II.4.b'
        ))
        
        self.add_rule(Rule(
            '2b-03', '2b', 250,
            {'capillary_refill_time': '>=3'},
            'CRT ≥3 giây',
            'QĐ 292 – II.4.b'
        ))
        
        self.add_rule(Rule(
            '2b-04', '2b', 250,
            {'cold_extremities': True},
            'Chi lạnh',
            'QĐ 292 – II.4.b'
        ))
        
        self.add_rule(Rule(
            '2b-05', '2b', 250,
            {'weak_pulse': True},
            'Mạch nhanh, nhỏ, yếu',
            'QĐ 292 – II.4.b'
        ))
        
        self.add_rule(Rule(
            '2b-06', '2b', 250,
            {'mottled_skin': True},
            'Da tái, đốm tím',
            'QĐ 292 – II.4.b'
        ))
        
        self.add_rule(Rule(
            '2b-07', '2b', 250,
            {'lactate': '>=2'},  # Và <4, nhưng rule 04-09 sẽ có priority cao hơn
            'Lactate 2-4 mmol/L',
            'QĐ 292 – II.4.b'
        ))
        
        # ==================== ĐỘ 2a - PRIORITY 200 ====================
        
        self.add_rule(Rule(
            '2a-01', '2a', 200,
            {'temp_c': '>=39', 'fever_days': '>=3'},
            'Sốt ≥39°C, ≥3 ngày',
            'QĐ 292 – II.4.a'
        ))
        
        self.add_rule(Rule(
            '2a-02', '2a', 200,
            {'vomit_per_hour': '>2'},
            'Nôn >2 lần/giờ',
            'QĐ 292 – II.4.a'
        ))
        
        self.add_rule(Rule(
            '2a-03', '2a', 200,
            {'startle_observed': True},
            'Giật mình',
            'QĐ 292 – II.4.a'
        ))
        
        # ==================== ĐỘ 1 - PRIORITY 100 ====================
        
        self.add_rule(Rule(
            '1-01', '1', 100,
            {'rash_hf': True, 'oral_ulcer': True},
            'Phát ban tay chân + loét miệng',
            'QĐ 292 – II.3'
        ))
        
        self.add_rule(Rule(
            '1-02', '1', 100,
            {'rash_hf': True, 'temp_c': '>=37.5'},
            'Sốt + phát ban',
            'QĐ 292 – II.3'
        ))
    
    def add_rule(self, rule: Rule):
        """Thêm rule vào engine"""
        self.rules.append(rule)
    
    def diagnose(self, clinical_data: Dict) -> Dict:
        """
        Chẩn đoán dựa trên dữ liệu lâm sàng
        Kiểm tra TUẦN TỰ từ độ cao xuống thấp, dừng ngay khi tìm thấy độ đầu tiên phù hợp
        
        Args:
            clinical_data: Dictionary chứa các thông tin lâm sàng
            
        Returns:
            Dictionary chứa kết quả chẩn đoán
        """
        # Danh sách các độ theo thứ tự ưu tiên từ cao xuống thấp
        degree_priority_order = [
            ('4', 400),   # Độ 4 - Nguy kịch
            ('3', 300),   # Độ 3 - Thần kinh nặng
            ('2b', 250),  # Độ 2b - Tuần hoàn
            ('2a', 200),  # Độ 2a - Cảnh báo
            ('1', 100)    # Độ 1 - Nhẹ
        ]
        
        # Kiểm tra TUẦN TỰ từng độ theo thứ tự ưu tiên
        for target_degree, target_priority in degree_priority_order:
            # Tìm các rules của độ hiện tại
            matched_rules_for_degree = []
            
            for rule in self.rules:
                if rule.degree == target_degree and rule.evaluate(clinical_data):
                    matched_rules_for_degree.append({
                        'rule_id': rule.rule_id,
                        'degree': rule.degree,
                        'priority': rule.priority,
                        'description': rule.description,
                        'source': rule.source
                    })
            
            # Nếu tìm thấy ít nhất 1 rule phù hợp với độ này → DỪNG NGAY
            if matched_rules_for_degree:
                # Nếu có nhiều rules cùng độ, chọn rule đầu tiên tìm được
                best_match = matched_rules_for_degree[0]
                
                return {
                    'success': True,
                    'degree': best_match['degree'],
                    'priority': best_match['priority'],
                    'primary_rule': best_match,
                    'all_matched_rules': matched_rules_for_degree,
                    'total_rules_matched': len(matched_rules_for_degree),
                    'input_data': clinical_data
                }
        
        # Nếu không có độ nào match
        return {
            'success': False,
            'degree': 'Không xác định',
            'priority': 0,
            'primary_rule': None,
            'all_matched_rules': [],
            'total_rules_matched': 0,
            'input_data': clinical_data,
            'message': 'Không có rule nào được match. Cần bổ sung dữ liệu lâm sàng.'
        }
    
    def load_rules_from_json(self, filepath: str):
        """Load rules từ file JSON (tương thích với data/rules.json)"""
        with open(filepath, 'r', encoding='utf-8') as f:
            rules_data = json.load(f)
        
        for rule_data in rules_data:
            # Chuyển đổi format "when" sang conditions
            conditions = {}
            for field, condition_str in rule_data.get('when', {}).items():
                # Chuẩn hóa tên field
                field_normalized = field.replace('₂', '2').replace(' ', '_').lower()
                conditions[field_normalized] = condition_str
            
            rule = Rule(
                rule_id=rule_data['id'],
                degree=rule_data['result'],
                priority=rule_data['priority'],
                conditions=conditions,
                description=rule_data.get('notes', ''),
                source=rule_data.get('source', '')
            )
            self.add_rule(rule)
    
    def get_statistics(self) -> Dict:
        """Thống kê về rules trong engine"""
        stats = {
            'total_rules': len(self.rules),
            'by_degree': {},
            'by_priority': {}
        }
        
        for rule in self.rules:
            # Count by degree
            stats['by_degree'][rule.degree] = stats['by_degree'].get(rule.degree, 0) + 1
            
            # Count by priority
            stats['by_priority'][rule.priority] = stats['by_priority'].get(rule.priority, 0) + 1
        
        return stats


def print_diagnosis_result(result: Dict):
    """In kết quả chẩn đoán"""
    print("\n" + "="*80)
    print("🏥 KẾT QUẢ CHẨN ĐOÁN TCM - RULE-BASED DIAGNOSIS")
    print("="*80)
    
    if result['success']:
        print(f"\n✓ ĐỘ BỆNH: {result['degree']}")
        print(f"✓ PRIORITY: {result['priority']}")
        
        rule = result['primary_rule']
        print(f"\n📋 RULE CHÍNH:")
        print(f"   • ID: {rule['rule_id']}")
        print(f"   • Mô tả: {rule['description']}")
        print(f"   • Nguồn: {rule['source']}")
        
        if result['total_rules_matched'] > 1:
            print(f"\n📊 CÁC RULE KHÁC ĐƯỢC MATCH ({result['total_rules_matched']-1}):")
            for r in result['all_matched_rules'][1:6]:
                print(f"   • [{r['rule_id']}] Độ {r['degree']} (P:{r['priority']}) - {r['description']}")
            
            if result['total_rules_matched'] > 6:
                print(f"   ... và {result['total_rules_matched'] - 6} rule khác")
    else:
        print(f"\n✗ {result['message']}")
    
    print("="*80 + "\n")


# ==================== DEMO CASES ====================

def demo_case_1():
    """Độ 4 - SpO₂ thấp nguy hiểm"""
    print("\n🔬 TEST CASE 1: BÉ 3 TUỔI - SPO₂ THẤP (ĐỘ 4)")
    
    engine = DiagnosisEngine()
    
    data = {
        'spo2': 88.0,
        'temp_c': 39.5,
        'heart_rate': 140,
        'respiratory_rate': 45,
        'rash_hf': True,
        'oral_ulcer': True,
        'age_months': 36
    }
    
    result = engine.diagnose(data)
    print_diagnosis_result(result)
    return result


def demo_case_2():
    """Độ 2b - Rối loạn tuần hoàn"""
    print("\n🔬 TEST CASE 2: BÉ 8 THÁNG - RỐI LOẠN TUẦN HOÀN (ĐỘ 2B)")
    
    engine = DiagnosisEngine()
    
    data = {
        'hr_no_fever': 160,
        'age_months': 8,
        'cold_extremities': True,
        'capillary_refill_time': 3.5,
        'temp_c': 38.5,
        'rash_hf': True,
        'oral_ulcer': True
    }
    
    result = engine.diagnose(data)
    print_diagnosis_result(result)
    return result


def demo_case_3():
    """Độ 3 - Triệu chứng thần kinh"""
    print("\n🔬 TEST CASE 3: BÉ 4 TUỔI - TRIỆU CHỨNG THẦN KINH (ĐỘ 3)")
    
    engine = DiagnosisEngine()
    
    data = {
        'startle_hist_30min': 3,
        'somnolent': True,
        'tremor': True,
        'nystagmus': True,
        'temp_c': 39.0,
        'rash_hf': True,
        'oral_ulcer': True,
        'age_months': 48
    }
    
    result = engine.diagnose(data)
    print_diagnosis_result(result)
    return result


def demo_case_4():
    """Độ 1 - Nhẹ, không biến chứng"""
    print("\n🔬 TEST CASE 4: BÉ 2 TUỔI - KHÔNG BIẾN CHỨNG (ĐỘ 1)")
    
    engine = DiagnosisEngine()
    
    data = {
        'rash_hf': True,
        'oral_ulcer': True,
        'temp_c': 38.0,
        'age_months': 24
    }
    
    result = engine.diagnose(data)
    print_diagnosis_result(result)
    return result


def demo_case_5():
    """Độ 2a - Sốt cao kéo dài"""
    print("\n🔬 TEST CASE 5: BÉ 5 TUỔI - SỐT CAO KÉO DÀI (ĐỘ 2A)")
    
    engine = DiagnosisEngine()
    
    data = {
        'temp_c': 39.5,
        'fever_days': 4,
        'vomit_per_hour': 3,
        'startle_observed': True,
        'rash_hf': True,
        'oral_ulcer': True,
        'age_months': 60
    }
    
    result = engine.diagnose(data)
    print_diagnosis_result(result)
    return result


def run_all_demos():
    """Chạy tất cả demo cases"""
    print("\n" + "🎯"*40)
    print("HỆ THỐNG CHẨN ĐOÁN TCM - PURE PYTHON RULE-BASED ENGINE")
    print("✓ Tập trung: Dự đoán dựa trên luật")
    print("✓ Không cần: Treatment, Database, External Dependencies")
    print("✓ Priority-based Selection: 400 (Độ 4) → 100 (Độ 1)")
    print("🎯"*40)
    
    # Hiển thị thống kê
    engine = DiagnosisEngine()
    stats = engine.get_statistics()
    print(f"\n📊 THỐNG KÊ RULES:")
    print(f"   • Tổng rules: {stats['total_rules']}")
    print(f"   • Phân bố theo độ: {stats['by_degree']}")
    print(f"   • Phân bố theo priority: {stats['by_priority']}")
    
    # Chạy demo cases
    demo_case_1()  # Độ 4
    demo_case_2()  # Độ 2b
    demo_case_3()  # Độ 3
    demo_case_4()  # Độ 1
    demo_case_5()  # Độ 2a


def custom_diagnosis():
    """Cho phép người dùng nhập dữ liệu tùy chỉnh"""
    print("\n" + "="*80)
    print("💡 CHẨN ĐOÁN TÙY CHỈNH")
    print("="*80)
    
    engine = DiagnosisEngine()
    
    # Ví dụ: Nhập dữ liệu của bạn
    custom_data = {
        'spo2': 85,           # SpO₂ rất thấp
        'lactate': 5.2,       # Lactate cao
        'temp_c': 40.0,
        'rash_hf': True,
        'oral_ulcer': True
    }
    
    print("\n📝 Dữ liệu nhập vào:")
    for key, value in custom_data.items():
        print(f"   • {key}: {value}")
    
    result = engine.diagnose(custom_data)
    print_diagnosis_result(result)
    
    return result


if __name__ == "__main__":
    # Chạy demos
    run_all_demos()
    
    # Uncomment để test custom diagnosis
    # custom_diagnosis()
