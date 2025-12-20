"""
Test Cases & Examples - TCM Diagnosis System

Tập hợp các test cases để kiểm tra hệ thống
"""

from tcm_diagnosis import TCMDiagnosisSystem, print_diagnosis_result


def test_degree_4_cases():
    """Test cases cho Độ 4 - Biến chứng nặng"""
    
    print("\n" + "="*80)
    print("TEST SUITE: ĐỘ 4 - BIẾN CHỨNG NẶNG")
    print("="*80)
    
    system = TCMDiagnosisSystem()
    
    # Case 4.1: SpO₂ thấp
    print("\n[4.1] SpO₂ <92%")
    result = system.diagnose_from_dict({
        'spo2': 85.0,
        'rash_hf': True,
        'oral_ulcer': True
    })
    assert result['degree'] == '4', "Should be Degree 4"
    assert result['primary_rule']['rule_id'] == '04-01', "Should match rule 04-01"
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    # Case 4.2: Ngưng thở
    print("\n[4.2] Ngưng thở (Apnea)")
    result = system.diagnose_from_dict({
        'apnea': True,
        'rash_hf': True
    })
    assert result['degree'] == '4'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    # Case 4.3: GCS ≤8
    print("\n[4.3] Glasgow Coma Scale ≤8")
    result = system.diagnose_from_dict({
        'gcs': 6,
        'temp_c': 39.0
    })
    assert result['degree'] == '4'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    # Case 4.4: Sốc - SBP thấp trẻ <12 tháng
    print("\n[4.4] SBP <70 mmHg (trẻ <12 tháng)")
    result = system.diagnose_from_dict({
        'sbp_mmhg': 65,
        'age_months': 8,
        'rash_hf': True
    })
    assert result['degree'] == '4'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    # Case 4.5: Sốc - SBP thấp trẻ ≥12 tháng
    print("\n[4.5] SBP <80 mmHg (trẻ ≥12 tháng)")
    result = system.diagnose_from_dict({
        'sbp_mmhg': 75,
        'age_months': 24,
        'rash_hf': True
    })
    assert result['degree'] == '4'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    # Case 4.6: Lactate cao
    print("\n[4.6] Lactate ≥4 mmol/L")
    result = system.diagnose_from_dict({
        'lactate': 5.5,
        'temp_c': 39.0
    })
    assert result['degree'] == '4'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    print("\n✓ ALL DEGREE 4 TESTS PASSED")


def test_degree_3_cases():
    """Test cases cho Độ 3 - Biến chứng thần kinh"""
    
    print("\n" + "="*80)
    print("TEST SUITE: ĐỘ 3 - BIẾN CHỨNG THẦN KINH")
    print("="*80)
    
    system = TCMDiagnosisSystem()
    
    # Case 3.1: Giật mình nhiều lần
    print("\n[3.1] Giật mình ≥2 lần/30 phút")
    result = system.diagnose_from_dict({
        'startle_hist_30min': 3,
        'rash_hf': True,
        'spo2': 95.0  # Đảm bảo không rơi vào Độ 4
    })
    assert result['degree'] == '3'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    # Case 3.2: Li bì
    print("\n[3.2] Li bì (Somnolent)")
    result = system.diagnose_from_dict({
        'somnolent': True,
        'temp_c': 39.0,
        'spo2': 95.0
    })
    assert result['degree'] == '3'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    # Case 3.3: Rung giật nhãn cầu
    print("\n[3.3] Nystagmus")
    result = system.diagnose_from_dict({
        'nystagmus': True,
        'rash_hf': True,
        'spo2': 95.0
    })
    assert result['degree'] == '3'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    # Case 3.4: Co giật
    print("\n[3.4] Co giật (Seizure)")
    result = system.diagnose_from_dict({
        'seizure': True,
        'temp_c': 40.0,
        'spo2': 95.0
    })
    assert result['degree'] == '3'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    # Case 3.5: SpO₂ <94%
    print("\n[3.5] SpO₂ <94% (nhưng ≥92%)")
    result = system.diagnose_from_dict({
        'spo2': 93.0,
        'rash_hf': True
    })
    assert result['degree'] == '3'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    print("\n✓ ALL DEGREE 3 TESTS PASSED")


def test_degree_2b_cases():
    """Test cases cho Độ 2b - Rối loạn tuần hoàn"""
    
    print("\n" + "="*80)
    print("TEST SUITE: ĐỘ 2B - RỐI LOẠN TUẦN HOÀN")
    print("="*80)
    
    system = TCMDiagnosisSystem()
    
    # Case 2b.1: Mạch nhanh trẻ <12 tháng
    print("\n[2b.1] HR >150 bpm (trẻ <12 tháng)")
    result = system.diagnose_from_dict({
        'hr_no_fever': 160,
        'age_months': 8,
        'spo2': 95.0,
        'rash_hf': True
    })
    assert result['degree'] == '2b'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    # Case 2b.2: Mạch nhanh trẻ ≥12 tháng
    print("\n[2b.2] HR >130 bpm (trẻ ≥12 tháng)")
    result = system.diagnose_from_dict({
        'hr_no_fever': 140,
        'age_months': 24,
        'spo2': 95.0,
        'rash_hf': True
    })
    assert result['degree'] == '2b'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    # Case 2b.3: CRT ≥3 giây
    print("\n[2b.3] Capillary Refill Time ≥3s")
    result = system.diagnose_from_dict({
        'capillary_refill_time': 3.5,
        'temp_c': 38.5,
        'spo2': 95.0
    })
    assert result['degree'] == '2b'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    # Case 2b.4: Chi lạnh
    print("\n[2b.4] Chi lạnh")
    result = system.diagnose_from_dict({
        'cold_extremities': True,
        'temp_c': 39.0,
        'spo2': 95.0
    })
    assert result['degree'] == '2b'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    # Case 2b.5: Lactate 2-4
    print("\n[2b.5] Lactate 2-4 mmol/L")
    result = system.diagnose_from_dict({
        'lactate': 2.8,
        'rash_hf': True,
        'spo2': 95.0
    })
    assert result['degree'] == '2b'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    print("\n✓ ALL DEGREE 2B TESTS PASSED")


def test_degree_2a_cases():
    """Test cases cho Độ 2a - Có nguy cơ biến chứng"""
    
    print("\n" + "="*80)
    print("TEST SUITE: ĐỘ 2A - CÓ NGUY CƠ BIẾN CHỨNG")
    print("="*80)
    
    system = TCMDiagnosisSystem()
    
    # Case 2a.1: Sốt cao kéo dài
    print("\n[2a.1] Sốt ≥39°C, ≥3 ngày")
    result = system.diagnose_from_dict({
        'temp_c': 39.5,
        'fever_days': 4,
        'rash_hf': True,
        'spo2': 96.0
    })
    assert result['degree'] == '2a'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    # Case 2a.2: Nôn nhiều
    print("\n[2a.2] Nôn >2 lần/giờ")
    result = system.diagnose_from_dict({
        'vomit_per_hour': 3,
        'temp_c': 38.5,
        'spo2': 96.0
    })
    assert result['degree'] == '2a'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    # Case 2a.3: Giật mình
    print("\n[2a.3] Giật mình (quan sát)")
    result = system.diagnose_from_dict({
        'startle_observed': True,
        'rash_hf': True,
        'spo2': 96.0
    })
    assert result['degree'] == '2a'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    print("\n✓ ALL DEGREE 2A TESTS PASSED")


def test_degree_1_cases():
    """Test cases cho Độ 1 - Không biến chứng"""
    
    print("\n" + "="*80)
    print("TEST SUITE: ĐỘ 1 - KHÔNG BIẾN CHỨNG")
    print("="*80)
    
    system = TCMDiagnosisSystem()
    
    # Case 1.1: Ban + loét miệng
    print("\n[1.1] Phát ban tay chân + loét miệng")
    result = system.diagnose_from_dict({
        'rash_hf': True,
        'oral_ulcer': True,
        'temp_c': 37.8
    })
    assert result['degree'] == '1'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    # Case 1.2: Sốt + ban
    print("\n[1.2] Sốt + phát ban")
    result = system.diagnose_from_dict({
        'rash_hf': True,
        'temp_c': 38.5
    })
    assert result['degree'] == '1'
    print(f"✓ PASS: {result['degree']}, Rule: {result['primary_rule']['rule_id']}")
    
    print("\n✓ ALL DEGREE 1 TESTS PASSED")


def test_priority_resolution():
    """Test ưu tiên khi có nhiều rules match"""
    
    print("\n" + "="*80)
    print("TEST: CONFLICT RESOLUTION - PRIORITY")
    print("="*80)
    
    system = TCMDiagnosisSystem()
    
    # Case: Có cả triệu chứng Độ 1, 2a, 3, 4
    print("\n[Priority] BN có triệu chứng nhiều độ → Chọn độ cao nhất")
    result = system.diagnose_from_dict({
        # Độ 1
        'rash_hf': True,
        'oral_ulcer': True,
        # Độ 2a
        'temp_c': 39.5,
        'fever_days': 4,
        # Độ 3
        'somnolent': True,
        # Độ 4
        'spo2': 88.0
    })
    
    print(f"\n📊 Kết quả:")
    print(f"   • Độ chọn: {result['degree']}")
    print(f"   • Priority: {result['priority']}")
    print(f"   • Tổng rules match: {result['total_matched']}")
    print(f"   • Các độ đã match: ", end="")
    
    degrees_matched = set(r['degree'] for r in result['all_matched_rules'])
    print(", ".join(sorted(degrees_matched, key=lambda x: {'4': 4, '3': 3, '2b': 2.5, '2a': 2, '1': 1}.get(x, 0), reverse=True)))
    
    assert result['degree'] == '4', "Should select highest priority (Degree 4)"
    assert result['total_matched'] >= 4, "Should match multiple rules"
    
    print(f"\n✓ PASS: Chọn đúng Độ {result['degree']} (priority cao nhất)")


def test_complex_scenario():
    """Test case phức tạp - bệnh nhân thực tế"""
    
    print("\n" + "="*80)
    print("TEST: COMPLEX SCENARIO - BỆNH NHÂN THỰC TẾ")
    print("="*80)
    
    system = TCMDiagnosisSystem()
    
    print("\n📋 Tình huống:")
    print("   Bé trai 18 tháng, nhập viện với:")
    print("   • Sốt 40°C kéo dài 4 ngày")
    print("   • Phát ban tay chân, loét miệng")
    print("   • Li bì, giật mình 4 lần/30 phút")
    print("   • Mạch 170 bpm, SpO₂ 93%")
    print("   • Chi lạnh, CRT 3.5 giây")
    
    # Tính HR không sốt
    hr_measured = 170
    temp = 40.0
    hr_no_fever = system.calculate_hr_no_fever(hr_measured, temp)
    
    data = {
        # Nhân khẩu
        'age_months': 18,
        # Triệu chứng TCM
        'rash_hf': True,
        'oral_ulcer': True,
        # Sốt
        'temp_c': temp,
        'fever_days': 4,
        # Tuần hoàn
        'heart_rate': hr_measured,
        'hr_no_fever': hr_no_fever,
        'cold_extremities': True,
        'capillary_refill_time': 3.5,
        # Hô hấp
        'spo2': 93.0,
        # Thần kinh
        'somnolent': True,
        'startle_hist_30min': 4
    }
    
    result = system.diagnose_from_dict(data)
    print_diagnosis_result(result, show_trace=False)
    
    print("💡 Phân tích:")
    print(f"   • SpO₂ 93% → Độ 3 (rule 03-11)")
    print(f"   • Li bì → Độ 3 (rule 03-02)")
    print(f"   • Giật mình ≥2 lần → Độ 3 (rule 03-01)")
    print(f"   • Sốt cao ≥39°C, ≥3 ngày → Độ 2a (rule 2a-01)")
    print(f"   • Chi lạnh → Độ 2b (rule 2b-04)")
    print(f"   • CRT ≥3s → Độ 2b (rule 2b-03)")
    print(f"\n✓ Kết luận: Độ {result['degree']} (do SpO₂ và triệu chứng thần kinh)")
    
    assert result['degree'] == '3', "Should be Degree 3 based on SpO2 and neuro symptoms"


def run_all_tests():
    """Chạy tất cả test cases"""
    
    print("\n" + "🧪"*40)
    print("TCM DIAGNOSIS SYSTEM - COMPREHENSIVE TEST SUITE")
    print("🧪"*40)
    
    try:
        test_degree_4_cases()
        test_degree_3_cases()
        test_degree_2b_cases()
        test_degree_2a_cases()
        test_degree_1_cases()
        test_priority_resolution()
        test_complex_scenario()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS PASSED SUCCESSFULLY")
        print("="*80)
        print("\n📊 Tổng kết:")
        print("   • Tất cả 5 độ bệnh: ✓")
        print("   • Priority-based conflict resolution: ✓")
        print("   • Complex scenario: ✓")
        print("   • Forward chaining inference: ✓")
        print("="*80 + "\n")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()
