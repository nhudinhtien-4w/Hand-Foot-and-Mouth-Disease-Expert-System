"""
Simple Forward Chaining Inference Engine
Engine đơn giản để xử lý rules.json theo format mới
"""

import json
import os

class SimpleInferenceEngine:
    def __init__(self, rules_file='data/rules.json'):
        """Khởi tạo engine với file rules"""
        self.rules_file = rules_file
        self.rules = []
        self.load_rules()
    
    def load_rules(self):
        """Load rules từ JSON file"""
        try:
            with open(self.rules_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.rules = data.get('conclusion_rules', [])
            print(f"✓ Loaded {len(self.rules)} rules from {self.rules_file}")
        except Exception as e:
            print(f"✗ Error loading rules: {e}")
            self.rules = []
    
    def evaluate_condition(self, condition, patient_data):
        """
        Đánh giá một condition
        
        Args:
            condition: {"field": "spo2", "operator": "<", "value": 92}
            patient_data: {"spo2": 88, ...}
        
        Returns:
            bool: True nếu condition thỏa mãn
        """
        field = condition['field']
        operator = condition['operator']
        expected_value = condition['value']
        
        # Lấy giá trị từ patient data
        actual_value = patient_data.get(field)
        
        # Nếu không có giá trị, coi như False
        if actual_value is None:
            return False
        
        # Đánh giá theo operator
        try:
            if operator == '==':
                return actual_value == expected_value
            elif operator == '!=':
                return actual_value != expected_value
            elif operator == '<':
                return float(actual_value) < float(expected_value)
            elif operator == '<=':
                return float(actual_value) <= float(expected_value)
            elif operator == '>':
                return float(actual_value) > float(expected_value)
            elif operator == '>=':
                return float(actual_value) >= float(expected_value)
            else:
                return False
        except (ValueError, TypeError):
            return False
    
    def evaluate_rule(self, rule, patient_data):
        """
        Đánh giá xem rule có match không
        
        Returns:
            bool: True nếu tất cả conditions đều thỏa mãn
        """
        conditions = rule.get('conditions', [])
        
        # Nếu không có conditions, coi như match (cho default rule)
        if not conditions:
            return True
        
        # Tất cả conditions phải thỏa mãn (AND logic)
        for condition in conditions:
            if not self.evaluate_condition(condition, patient_data):
                return False
        
        return True
    
    def diagnose(self, patient_data):
        """
        Chạy forward chaining để chẩn đoán
        
        Args:
            patient_data: dict chứa thông tin bệnh nhân
        
        Returns:
            dict: {
                'success': bool,
                'disease_level': str,
                'matched_rules': list,
                'explanation': str,
                'priority': int
            }
        """
        matched_rules = []
        
        # Tìm tất cả rules match
        for rule in self.rules:
            if self.evaluate_rule(rule, patient_data):
                matched_rules.append(rule)
        
        # Nếu không có rule nào match
        if not matched_rules:
            return {
                'success': False,
                'disease_level': 'Không xác định',
                'matched_rules': [],
                'explanation': 'Không có rule nào phù hợp với dữ liệu đầu vào',
                'priority': -1
            }
        
        # Chọn rule có priority cao nhất
        best_rule = max(matched_rules, key=lambda r: r.get('priority', 0))
        
        # Tạo explanation
        explanation_parts = [
            f"Phát hiện {len(matched_rules)} rule(s) phù hợp.",
            f"Chọn rule: {best_rule['name']}",
            f"Priority: {best_rule['priority']}",
            f"Conditions:"
        ]
        
        for condition in best_rule.get('conditions', []):
            field = condition['field']
            operator = condition['operator']
            value = condition['value']
            actual = patient_data.get(field, 'N/A')
            explanation_parts.append(f"  - {field} {operator} {value} (giá trị: {actual})")
        
        # Chuẩn bị matched_rules với đầy đủ thông tin
        matched_rules_info = []
        for rule in matched_rules:
            matched_rules_info.append({
                'id': rule['id'],
                'name': rule['name'],
                'priority': rule.get('priority', 0)
            })
        
        return {
            'success': True,
            'disease_level': best_rule['conclusion']['disease_level'],
            'matched_rules': matched_rules_info,
            'best_rule': best_rule,
            'explanation': '\n'.join(explanation_parts),
            'priority': best_rule.get('priority', 0),
            'total_matched': len(matched_rules)
        }
    
    def get_stats(self):
        """Lấy thống kê knowledge base"""
        grades = {}
        for rule in self.rules:
            grade = rule['conclusion']['disease_level']
            grades[grade] = grades.get(grade, 0) + 1
        
        return {
            'total_rules': len(self.rules),
            'rules_by_grade': grades,
            'priorities': {
                'min': min([r.get('priority', 0) for r in self.rules]) if self.rules else 0,
                'max': max([r.get('priority', 0) for r in self.rules]) if self.rules else 0
            }
        }


# Test
if __name__ == '__main__':
    print("\n" + "="*70)
    print("SIMPLE INFERENCE ENGINE TEST")
    print("="*70 + "\n")
    
    # Khởi tạo engine
    engine = SimpleInferenceEngine()
    
    # Stats
    stats = engine.get_stats()
    print(f"📊 Knowledge Base Stats:")
    print(f"   Total rules: {stats['total_rules']}")
    print(f"   Rules by grade: {stats['rules_by_grade']}")
    print(f"   Priority range: {stats['priorities']['min']} - {stats['priorities']['max']}")
    
    # Test case 1: Độ 4 - SpO2 thấp
    print("\n" + "-"*70)
    print("TEST 1: Độ 4 - SpO2 < 92%")
    print("-"*70)
    
    patient1 = {
        'spo2': 88,
        'age_months': 24,
        'rash_hand_foot_mouth': True
    }
    
    result1 = engine.diagnose(patient1)
    print(f"✓ Kết quả: Độ {result1['disease_level']}")
    print(f"✓ Rule: {result1.get('best_rule', {}).get('name')}")
    print(f"✓ Matched: {result1['total_matched']} rules")
    print(f"\nExplanation:\n{result1['explanation']}")
    
    # Test case 2: Độ 2a - Sốt cao
    print("\n" + "-"*70)
    print("TEST 2: Độ 2a - Sốt ≥ 39°C")
    print("-"*70)
    
    patient2 = {
        'fever_temp_c': 39.5,
        'rash_hand_foot_mouth': True
    }
    
    result2 = engine.diagnose(patient2)
    print(f"✓ Kết quả: Độ {result2['disease_level']}")
    print(f"✓ Rule: {result2.get('best_rule', {}).get('name')}")
    print(f"\nExplanation:\n{result2['explanation']}")
    
    # Test case 3: Độ 1 - Chỉ có phát ban
    print("\n" + "-"*70)
    print("TEST 3: Độ 1 - Chỉ có phát ban")
    print("-"*70)
    
    patient3 = {
        'rash_hand_foot_mouth': True,
        'spo2': 98
    }
    
    result3 = engine.diagnose(patient3)
    print(f"✓ Kết quả: Độ {result3['disease_level']}")
    print(f"✓ Rule: {result3.get('best_rule', {}).get('name')}")
    print(f"\nExplanation:\n{result3['explanation']}")
    
    print("\n" + "="*70 + "\n")
