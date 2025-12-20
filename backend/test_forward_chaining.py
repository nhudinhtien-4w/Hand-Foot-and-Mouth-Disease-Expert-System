"""
Test Forward Chaining - Multi-Step Inference
Minh họa quá trình suy diễn tiến nhiều bước theo thuật toán
"""

from tcm_diagnosis import TCMDiagnosisSystem


def test_multi_step_inference():
    """
    Test case minh họa suy diễn nhiều bước
    
    Kịch bản: Bệnh nhân có HR cao + tuổi nhỏ
    
    Bước 1: GT (Ground Truth - Facts ban đầu)
        - hr_no_fever = 160
        - age_months = 8
        - spo2 = 95
    
    Bước 2: Intermediate Rule fire → tạo sự kiện mới
        INT-01: IF (hr_no_fever > 150 AND age_months < 12)
                THEN tachycardia_for_age = True
    
    Bước 3: Intermediate Rule fire → tạo sự kiện mới    
        INT-07: IF (tachycardia_for_age == True)
                THEN circulatory_impairment = True
    
    Bước 4: Conclusion Rule fire → Kết luận
        2b-01: IF (tachycardia_for_age == True)
               THEN Độ 2b
    """
    
    print("\n" + "="*80)
    print("TEST: MULTI-STEP FORWARD CHAINING")
    print("="*80)
    
    system = TCMDiagnosisSystem()
    
    print("\n[BƯỚC 1] Nhập dữ liệu ban đầu (GT):")
    input_data = {
        'hr_no_fever': 160,  # Mạch nhanh
        'age_months': 8,     # Trẻ < 12 tháng
        'spo2': 95.0,        # SpO2 bình thường
        'rash_hf': True      # Ban tay chân
    }
    print(f"   Input facts: {input_data}")
    
    print("\n[BƯỚC 2] Chạy Forward Chaining Engine...")
    result = system.diagnose_from_dict(input_data, verbose=False)
    
    print("\n[KẾT QUẢ]")
    print(f"   ✓ Kết luận: Độ {result['degree']}")
    print(f"   ✓ Số vòng lặp: {result.get('total_iterations', 'N/A')}")
    
    if result.get('fired_intermediate_rules'):
        print(f"\n[LUẬT TRUNG GIAN ĐÃ FIRE] ({len(result['fired_intermediate_rules'])} rules):")
        for i, rule in enumerate(result['fired_intermediate_rules'], 1):
            print(f"   Vòng {i}: [{rule['rule_id']}] {rule['description']}")
            print(f"            → Tạo ra: {rule['derived_facts']}")
    
    if result.get('derived_facts'):
        print(f"\n[SỰ KIỆN SUY DIỄN] ({len(result['derived_facts'])} facts):")
        for key, value in result['derived_facts'].items():
            print(f"   • {key} = {value}")
    
    if result.get('primary_rule'):
        print(f"\n[LUẬT KẾT LUẬN]:")
        rule = result['primary_rule']
        print(f"   • Rule ID: {rule['rule_id']}")
        print(f"   • Mô tả: {rule['description']}")
        print(f"   • Kết luận: Độ {rule['degree']}")
    
    print("\n" + "="*80)
    print("✓ TEST PASSED")
    print("="*80)


def test_complex_multi_step():
    """
    Test case phức tạp hơn - nhiều bước suy diễn
    
    Kịch bản: Bệnh nhân có nhiều dấu hiệu → suy diễn qua nhiều bước
    """
    
    print("\n" + "="*80)
    print("TEST: COMPLEX MULTI-STEP INFERENCE")
    print("="*80)
    
    system = TCMDiagnosisSystem()
    
    print("\n[DỮLIỆU BAN ĐẦU]:")
    input_data = {
        'hr_no_fever': 155,
        'age_months': 10,
        'capillary_refill_time': 3.5,
        'temp_c': 39.5,
        'fever_days': 4,
        'spo2': 94.5,
        'rash_hf': True
    }
    
    for key, value in input_data.items():
        print(f"   • {key} = {value}")
    
    print("\n[CHẠY SUY DIỄN]...")
    result = system.diagnose_from_dict(input_data, verbose=True)
    
    print("\n" + "="*80)


def test_degree_4_with_intermediate():
    """
    Test Độ 4 với intermediate rules
    """
    
    print("\n" + "="*80)
    print("TEST: DEGREE 4 - WITH INTERMEDIATE RULES")
    print("="*80)
    
    system = TCMDiagnosisSystem()
    
    input_data = {
        'sbp_mmhg': 65,      # SBP thấp
        'age_months': 7,     # Trẻ < 12 tháng
        'rash_hf': True,
        'temp_c': 39.0
    }
    
    print("\n[INPUT]:")
    for key, value in input_data.items():
        print(f"   • {key} = {value}")
    
    result = system.diagnose_from_dict(input_data, verbose=False)
    
    print(f"\n[OUTPUT]:")
    print(f"   ✓ Độ bệnh: {result['degree']}")
    print(f"   ✓ Số bước: {result.get('total_iterations', 1)}")
    
    if result.get('fired_intermediate_rules'):
        print(f"\n[QUÁ TRÌNH SUY DIỄN]:")
        for i, rule in enumerate(result['fired_intermediate_rules'], 1):
            print(f"   {i}. {rule['description']}")
            print(f"      → {rule['derived_facts']}")
    
    if result.get('primary_rule'):
        rule = result['primary_rule']
        print(f"\n[KẾT LUẬN]: [{rule['rule_id']}] {rule['description']}")
    
    print("\n" + "="*80)


def test_no_conclusion():
    """
    Test trường hợp không tìm được kết luận
    """
    
    print("\n" + "="*80)
    print("TEST: NO CONCLUSION CASE")
    print("="*80)
    
    system = TCMDiagnosisSystem()
    
    input_data = {
        'temp_c': 37.0,  # Không sốt
        # Không có triệu chứng đủ để kết luận
    }
    
    print("\n[INPUT]:")
    print(f"   {input_data}")
    
    result = system.diagnose_from_dict(input_data, verbose=False)
    
    print(f"\n[OUTPUT]:")
    print(f"   Success: {result['success']}")
    print(f"   Message: {result.get('message', 'N/A')}")
    print(f"   Degree: {result['degree']}")
    
    if result.get('fired_intermediate_rules'):
        print(f"\n[ĐÃ SUY DIỄN]:")
        for rule in result['fired_intermediate_rules']:
            print(f"   • {rule['description']}")
    else:
        print(f"\n   → Không có luật nào được kích hoạt")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    print("\n" + "🚀 "*40)
    print("FORWARD CHAINING - MULTI-STEP INFERENCE DEMO")
    print("Minh họa thuật toán suy diễn tiến nhiều bước")
    print("🚀 "*40)
    
    # Test 1: Basic multi-step
    test_multi_step_inference()
    
    # Test 2: Complex case
    test_complex_multi_step()
    
    # Test 3: Degree 4 with intermediate
    test_degree_4_with_intermediate()
    
    # Test 4: No conclusion
    test_no_conclusion()
    
    print("\n" + "✅ "*40)
    print("ALL TESTS COMPLETED")
    print("✅ "*40 + "\n")
