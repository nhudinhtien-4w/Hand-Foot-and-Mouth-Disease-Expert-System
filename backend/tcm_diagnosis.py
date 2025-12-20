"""
TCM Diagnosis System - Main Module
Hệ chuyên gia chẩn đoán bệnh Tay-Chân-Miệng

Mô hình hóa theo COPD Expert System:
- Sử dụng Forward Chaining
- Priority-based Conflict Resolution  
- Rule-based Diagnosis
- Không cần Database & Treatment
"""

from typing import Dict, List, Optional
from dataclasses import asdict

from knowledge_base import (
    PatientData,
    DemographicFact,
    VitalSignFact,
    SymptomFact,
    KnowledgeBase,
    DegreeLevel
)

from inference_engine import InferenceEngine


# ============================================================================
# DIAGNOSIS SYSTEM - Hệ thống chẩn đoán chính
# ============================================================================

class TCMDiagnosisSystem:
    """
    Hệ thống chẩn đoán bệnh Tay-Chân-Miệng
    
    Kiến trúc:
    - Knowledge Base: Chứa 40+ rules chẩn đoán
    - Inference Engine: Thực hiện suy diễn tiến
    - Patient Data: Biểu diễn dữ liệu bệnh nhân
    """
    
    def __init__(self, conflict_strategy: str = 'priority'):
        """
        Khởi tạo hệ thống
        
        Args:
            conflict_strategy: Chiến lược giải quyết xung đột
                              ('priority', 'severity', 'recency')
        """
        self.kb = KnowledgeBase()
        self.engine = InferenceEngine(self.kb)
        self.engine.set_conflict_resolution(conflict_strategy)
        
        print("="*80)
        print("🏥 HỆ THỐNG CHẨN ĐOÁN TCM - TCM DIAGNOSIS EXPERT SYSTEM")
        print("="*80)
        print(f"✓ Knowledge Base: {len(self.kb)} rules loaded")
        print(f"✓ Conflict Resolution: {conflict_strategy}")
        print(f"✓ Inference Method: Forward Chaining")
        print("="*80 + "\n")
    
    def diagnose(self, patient_data: PatientData, verbose: bool = False) -> Dict:
        """
        Chẩn đoán bệnh nhân
        
        Args:
            patient_data: Dữ liệu bệnh nhân (PatientData object)
            verbose: Hiển thị trace suy diễn chi tiết
            
        Returns:
            Kết quả chẩn đoán
        """
        result = self.engine.run(patient_data)
        
        if verbose:
            print(self.engine.explain(verbose=True))
        
        return result
    
    def diagnose_from_dict(self, clinical_data: Dict, verbose: bool = False) -> Dict:
        """
        Chẩn đoán từ dictionary
        
        Args:
            clinical_data: Dictionary chứa dữ liệu lâm sàng
            verbose: Hiển thị trace suy diễn chi tiết
            
        Returns:
            Kết quả chẩn đoán
        """
        result = self.engine.run_from_dict(clinical_data)
        
        if verbose:
            print(self.engine.explain(verbose=True))
        
        return result
    
    def explain_result(self, verbose: bool = False) -> str:
        """
        Giải thích kết quả chẩn đoán gần nhất
        
        Args:
            verbose: Hiển thị chi tiết trace
            
        Returns:
            Chuỗi giải thích
        """
        return self.engine.explain(verbose=verbose)
    
    def get_statistics(self) -> Dict:
        """Thống kê về hệ thống"""
        return self.engine.get_knowledge_base_stats()
    
    def calculate_hr_no_fever(self, hr_measured: int, temp_c: float) -> int:
        """
        Tính mạch điều chỉnh (loại trừ ảnh hưởng sốt)
        
        Công thức: HR_no_fever = HR_measured - max(0, (TempC - 38) * 10)
        
        Args:
            hr_measured: Mạch đo được (bpm)
            temp_c: Nhiệt độ (°C)
            
        Returns:
            Mạch điều chỉnh (bpm)
        """
        fever_adjustment = max(0, (temp_c - 38) * 10)
        hr_no_fever = hr_measured - fever_adjustment
        return int(hr_no_fever)
    
    def calculate_pulse_pressure(self, sbp: int, dbp: int) -> int:
        """
        Tính chênh áp (pulse pressure)
        
        Args:
            sbp: Huyết áp tâm thu (mmHg)
            dbp: Huyết áp tâm trương (mmHg)
            
        Returns:
            Chênh áp (mmHg)
        """
        return sbp - dbp


# ============================================================================
# HELPER FUNCTIONS - Các hàm tiện ích
# ============================================================================

def print_diagnosis_result(result: Dict, show_trace: bool = False):
    """
    In kết quả chẩn đoán một cách đẹp mắt
    
    Args:
        result: Kết quả từ diagnosis
        show_trace: Hiển thị trace suy diễn
    """
    print("\n" + "="*80)
    print("🏥 KẾT QUẢ CHẨN ĐOÁN TCM")
    print("="*80)
    
    if result['success']:
        print(f"\n✓ ĐỘ BỆNH: {result['degree']}")
        print(f"✓ ĐỘ ƯU TIÊN: {result['priority']}")
        
        rule = result['primary_rule']
        print(f"\n📋 LUẬT CHÍNH:")
        print(f"   • ID: {rule['rule_id']}")
        print(f"   • Mô tả: {rule['description']}")
        print(f"   • Nguồn: {rule['source']}")
        
        if result['total_matched'] > 1:
            print(f"\n📊 CÁC LUẬT KHÁC ĐÃ MATCH ({result['total_matched']}):")
            for i, r in enumerate(result['all_matched_rules'][:5], 1):
                print(f"   {i}. [{r['rule_id']}] Độ {r['degree']} (P:{r['priority']}) - {r['description']}")
            
            if result['total_matched'] > 5:
                print(f"   ... và {result['total_matched'] - 5} luật khác")
        
        if show_trace and 'inference_trace' in result:
            print(f"\n🔍 TRACE SUY DIỄN:")
            for trace_line in result['inference_trace']:
                print(f"   {trace_line}")
    else:
        print(f"\n✗ {result.get('message', 'Không xác định được độ bệnh')}")
        print("\n💡 GỢI Ý:")
        print("   • Kiểm tra lại các triệu chứng đặc trưng (ban tay chân, loét miệng)")
        print("   • Bổ sung thông tin về dấu hiệu sinh tồn (SpO₂, mạch, nhiệt độ)")
        print("   • Kiểm tra các dấu hiệu biến chứng (thần kinh, tuần hoàn, hô hấp)")
    
    print("="*80 + "\n")


def create_patient_from_dict(data: Dict) -> PatientData:
    """
    Tạo PatientData từ dictionary
    
    Args:
        data: Dictionary chứa dữ liệu lâm sàng
        
    Returns:
        PatientData object
    """
    return PatientData.from_dict(data)


def summarize_statistics(stats: Dict):
    """
    In thống kê về knowledge base
    
    Args:
        stats: Dictionary chứa thống kê
    """
    print("\n" + "="*80)
    print("📊 THỐNG KÊ KNOWLEDGE BASE")
    print("="*80)
    print(f"\nTổng số luật: {stats['total_rules']}")
    
    print(f"\nPhân bố theo độ bệnh:")
    for degree in ['4', '3', '2b', '2a', '1']:
        count = stats['by_degree'].get(degree, 0)
        print(f"   • Độ {degree}: {count} luật")
    
    print(f"\nPhân bố theo priority:")
    for priority in sorted(stats['by_priority'].keys(), reverse=True):
        count = stats['by_priority'][priority]
        print(f"   • Priority {priority}: {count} luật")
    
    print("="*80 + "\n")


# ============================================================================
# QUICK DIAGNOSIS FUNCTIONS
# ============================================================================

def quick_diagnose(clinical_data: Dict, verbose: bool = False) -> Dict:
    """
    Chẩn đoán nhanh từ dictionary
    
    Args:
        clinical_data: Dictionary chứa dữ liệu lâm sàng
        verbose: Hiển thị chi tiết
        
    Returns:
        Kết quả chẩn đoán
    """
    system = TCMDiagnosisSystem()
    result = system.diagnose_from_dict(clinical_data, verbose=verbose)
    
    if not verbose:
        print_diagnosis_result(result)
    
    return result


# ============================================================================
# MAIN - Demo & Testing
# ============================================================================

def main():
    """Hàm main - Demo hệ thống"""
    
    # Khởi tạo hệ thống
    system = TCMDiagnosisSystem(conflict_strategy='priority')
    
    # Hiển thị thống kê
    stats = system.get_statistics()
    summarize_statistics(stats)
    
    # Test cases
    print("\n" + "🎯"*40)
    print("DEMO CASES - TỰ ĐỘNG CHẨN ĐOÁN")
    print("🎯"*40 + "\n")
    
    # Case 1: Độ 4 - SpO₂ thấp nguy hiểm
    print("\n" + "="*80)
    print("TEST CASE 1: BÉ 3 TUỔI - SPO₂ THẤP NGUY HIỂM")
    print("="*80)
    
    case1_data = {
        'spo2': 88.0,
        'temp_c': 39.5,
        'heart_rate': 140,
        'respiratory_rate': 45,
        'rash_hf': True,
        'oral_ulcer': True,
        'age_months': 36
    }
    
    result1 = system.diagnose_from_dict(case1_data, verbose=False)
    print_diagnosis_result(result1)
    
    # Case 2: Độ 3 - Triệu chứng thần kinh
    print("\n" + "="*80)
    print("TEST CASE 2: BÉ 4 TUỔI - TRIỆU CHỨNG THẦN KINH")
    print("="*80)
    
    case2_data = {
        'startle_hist_30min': 3,
        'somnolent': True,
        'tremor': True,
        'nystagmus': True,
        'temp_c': 39.0,
        'rash_hf': True,
        'oral_ulcer': True,
        'age_months': 48,
        'spo2': 96.0
    }
    
    result2 = system.diagnose_from_dict(case2_data, verbose=False)
    print_diagnosis_result(result2)
    
    # Case 3: Độ 2b - Rối loạn tuần hoàn
    print("\n" + "="*80)
    print("TEST CASE 3: BÉ 8 THÁNG - RỐI LOẠN TUẦN HOÀN")
    print("="*80)
    
    # Tính HR không sốt
    hr_measured = 160
    temp = 38.5
    hr_no_fever = system.calculate_hr_no_fever(hr_measured, temp)
    
    case3_data = {
        'hr_no_fever': hr_no_fever,
        'age_months': 8,
        'cold_extremities': True,
        'capillary_refill_time': 3.5,
        'temp_c': temp,
        'rash_hf': True,
        'oral_ulcer': True
    }
    
    print(f"📝 Tính toán: HR đo = {hr_measured}, Temp = {temp}°C → HR (không sốt) = {hr_no_fever}")
    
    result3 = system.diagnose_from_dict(case3_data, verbose=False)
    print_diagnosis_result(result3)
    
    # Case 4: Độ 2a - Sốt cao kéo dài
    print("\n" + "="*80)
    print("TEST CASE 4: BÉ 5 TUỔI - SỐT CAO KÉO DÀI")
    print("="*80)
    
    case4_data = {
        'temp_c': 39.5,
        'fever_days': 4,
        'vomit_per_hour': 3,
        'startle_observed': True,
        'rash_hf': True,
        'oral_ulcer': True,
        'age_months': 60
    }
    
    result4 = system.diagnose_from_dict(case4_data, verbose=False)
    print_diagnosis_result(result4)
    
    # Case 5: Độ 1 - Không biến chứng
    print("\n" + "="*80)
    print("TEST CASE 5: BÉ 2 TUỔI - KHÔNG BIẾN CHỨNG")
    print("="*80)
    
    case5_data = {
        'rash_hf': True,
        'oral_ulcer': True,
        'temp_c': 38.0,
        'age_months': 24
    }
    
    result5 = system.diagnose_from_dict(case5_data, verbose=False)
    print_diagnosis_result(result5)
    
    # Case 6: Không xác định
    print("\n" + "="*80)
    print("TEST CASE 6: DỮ LIỆU KHÔNG ĐỦ")
    print("="*80)
    
    case6_data = {
        'temp_c': 37.5
    }
    
    result6 = system.diagnose_from_dict(case6_data, verbose=False)
    print_diagnosis_result(result6)
    
    # Tổng kết
    print("\n" + "="*80)
    print("✓ HOÀN THÀNH DEMO")
    print("="*80)
    print("\n💡 Để sử dụng trong code:")
    print("""
from tcm_diagnosis import TCMDiagnosisSystem

# Khởi tạo
system = TCMDiagnosisSystem()

# Chẩn đoán
data = {
    'spo2': 88.0,
    'temp_c': 39.5,
    'rash_hf': True,
    'oral_ulcer': True
}

result = system.diagnose_from_dict(data)
print(f"Độ bệnh: {result['degree']}")
    """)
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
