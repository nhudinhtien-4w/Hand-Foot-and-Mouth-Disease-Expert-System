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
        Đánh giá một condition hoặc condition group
        
        Args:
            condition: {"field": "spo2", "operator": "<", "value": 92}
                   hoặc {"type": "OR", "conditions": [...]}
            patient_data: {"spo2": 88, ...}
        
        Returns:
            bool: True nếu condition thỏa mãn
        """
        # Xử lý condition groups (OR/AND)
        if 'type' in condition:
            condition_type = condition['type']
            sub_conditions = condition.get('conditions', [])
            
            if condition_type == 'OR':
                # Ít nhất 1 condition phải đúng
                return any(self.evaluate_condition(c, patient_data) for c in sub_conditions)
            elif condition_type == 'AND':
                # Tất cả conditions phải đúng
                return all(self.evaluate_condition(c, patient_data) for c in sub_conditions)
            else:
                # Unknown type
                return False
        
        # Xử lý condition đơn
        field = condition.get('field')
        if not field:
            return False
            
        operator = condition.get('operator')
        expected_value = condition.get('value')
        
        # Validate có đủ thông tin
        if operator is None or expected_value is None:
            return False
        
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
            elif operator == 'in':
                # Support for checking if value is in a list
                if isinstance(expected_value, list):
                    return actual_value in expected_value
                return False
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
        
        - Nếu rules có disease_level (phân độ): Kiểm tra tuần tự Độ 4→3→2b→2a→1
        - Nếu rules không có disease_level (chẩn đoán có/không bệnh): Chọn priority cao nhất
        
        Args:
            patient_data: dict chứa thông tin bệnh nhân
        
        Returns:
            dict: Kết quả chẩn đoán
        """
        # Tìm tất cả rules match
        matched_rules = []
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
        
        # Kiểm tra xem có phải rules phân độ không (có disease_level)
        has_disease_level = any(
            rule.get('conclusion', {}).get('disease_level') is not None 
            for rule in matched_rules
        )
        
        if has_disease_level:
            # Logic TUẦN TỰ cho phân độ bệnh với TRACE CHI TIẾT
            degree_priority_order = ['4', '3', '2b', '2a', '1']
            degree_names = {
                '4': 'Độ 4 (Nguy kịch)',
                '3': 'Độ 3 (Thần kinh nặng)',
                '2b': 'Độ 2b (Tuần hoàn)',
                '2a': 'Độ 2a (Cảnh báo)',
                '1': 'Độ 1 (Nhẹ)'
            }
            
            # Tạo trace chi tiết
            trace_steps = []
            
            # Bước 1: Hiển thị triệu chứng đã nhập
            input_symptoms = []
            for field, value in patient_data.items():
                if value and value != 0 and value != False:
                    input_symptoms.append({'field': field, 'value': value})
            
            trace_steps.append({
                'type': 'input',
                'message': 'Các triệu chứng đã nhập',
                'symptoms': input_symptoms
            })
            
            # Bước 2: Kiểm tra từng độ
            for target_degree in degree_priority_order:
                matched_rules_for_degree = []
                
                # Tìm rules của độ này
                for rule in matched_rules:
                    rule_degree = rule.get('conclusion', {}).get('disease_level', '')
                    if rule_degree == target_degree:
                        matched_rules_for_degree.append(rule)
                
                # Thêm trace cho độ này
                if matched_rules_for_degree:
                    # Có triệu chứng khớp
                    matched_symptoms = []
                    for rule in matched_rules_for_degree:
                        matched_symptoms.append({
                            'id': rule['id'],
                            'name': rule['name'],
                            'priority': rule.get('priority', 0),
                            'source': rule.get('source', '')
                        })
                    
                    trace_steps.append({
                        'type': 'check',
                        'degree': target_degree,
                        'degree_name': degree_names.get(target_degree, target_degree),
                        'matched': True,
                        'symptoms': matched_symptoms
                    })
                    
                    # Tìm thấy → DỪNG và KẾT LUẬN
                    best_rule = max(matched_rules_for_degree, key=lambda r: r.get('priority', 0))
                    conclusion = best_rule.get('conclusion', {})
                    
                    trace_steps.append({
                        'type': 'conclusion',
                        'degree': target_degree,
                        'degree_name': degree_names.get(target_degree, target_degree),
                        'description': conclusion.get('description', ''),
                        'matched_symptoms': matched_symptoms,
                        'source': best_rule.get('source', '')
                    })
                    
                    matched_rules_info = [
                        {
                            'id': r['id'],
                            'name': r['name'],
                            'priority': r.get('priority', 0),
                            'source': r.get('source', '')
                        }
                        for r in matched_rules_for_degree
                    ]
                    
                    return {
                        'success': True,
                        'conclusions': conclusion,
                        'matched_rules': matched_rules_info,
                        'best_rule': best_rule,
                        'explanation': f"Phân độ: {target_degree}",
                        'priority': best_rule.get('priority', 0),
                        'total_matched': len(matched_rules_for_degree),
                        'trace': trace_steps  # TRACE CHI TIẾT
                    }
                else:
                    # Không có triệu chứng khớp với độ này
                    trace_steps.append({
                        'type': 'check',
                        'degree': target_degree,
                        'degree_name': degree_names.get(target_degree, target_degree),
                        'matched': False
                    })
        
        # Logic CŨ cho chẩn đoán có/không bệnh (không có disease_level)
        # Chọn rule có priority cao nhất
        best_rule = max(matched_rules, key=lambda r: r.get('priority', 0))
        # Logic CŨ cho chẩn đoán có/không bệnh (không có disease_level)
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
            if 'type' in condition:
                condition_type = condition.get('type', 'UNKNOWN')
                sub_count = len(condition.get('conditions', []))
                explanation_parts.append(f"  - {condition_type} group with {sub_count} conditions")
            else:
                field = condition.get('field', 'UNKNOWN')
                operator = condition.get('operator', '?')
                value = condition.get('value', '?')
                actual = patient_data.get(field, 'N/A') if field != 'UNKNOWN' else 'N/A'
                explanation_parts.append(f"  - {field} {operator} {value} (giá trị: {actual})")
        
        matched_rules_info = []
        for rule in matched_rules:
            matched_rules_info.append({
                'id': rule['id'],
                'name': rule['name'],
                'priority': rule.get('priority', 0)
            })
        
        conclusion = best_rule.get('conclusion', {})
        
        return {
            'success': True,
            'conclusions': conclusion,
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
    
    # Khởi tạo engine với classification_level_rules.json
    engine = SimpleInferenceEngine('data/classification_level_rules.json')
    
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
    disease_level = result1.get('conclusions', {}).get('disease_level', 'Không xác định')
    print(f"✓ Kết quả: Độ {disease_level}")
    print(f"✓ Rule: {result1.get('best_rule', {}).get('name')}")
    print(f"✓ Matched: {result1.get('total_matched', 0)} rules")
    print(f"\nExplanation:\n{result1.get('explanation', 'N/A')}")
    
    # Test case 2: Độ 2a - Sốt cao
    print("\n" + "-"*70)
    print("TEST 2: Độ 2a - Sốt ≥ 39°C")
    print("-"*70)
    
    patient2 = {
        'fever_temp_c': 39.5,
        'rash_hand_foot_mouth': True
    }
    
    result2 = engine.diagnose(patient2)
    disease_level = result2.get('conclusions', {}).get('disease_level', 'Không xác định')
    print(f"✓ Kết quả: Độ {disease_level}")
    print(f"✓ Rule: {result2.get('best_rule', {}).get('name')}")
    print(f"\nExplanation:\n{result2.get('explanation', 'N/A')}")
    
    # Test case 3: Độ 1 - Chỉ có phát ban
    print("\n" + "-"*70)
    print("TEST 3: Độ 1 - Chỉ có phát ban")
    print("-"*70)
    
    patient3 = {
        'rash_hand_foot_mouth': True,
        'spo2': 98
    }
    
    result3 = engine.diagnose(patient3)
    disease_level = result3.get('conclusions', {}).get('disease_level', 'Không xác định')
    print(f"✓ Kết quả: Độ {disease_level}")
    print(f"✓ Rule: {result3.get('best_rule', {}).get('name')}")
    print(f"\nExplanation:\n{result3.get('explanation', 'N/A')}")
    
    print("\n" + "="*70 + "\n")
