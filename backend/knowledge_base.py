"""
Knowledge Base Module - TCM Diagnosis Expert System
Mô hình hóa theo COPD Expert System

Chứa:
- Facts: Biểu diễn dữ liệu bệnh nhân
- Rules: Tri thức y khoa về chẩn đoán TCM
- Knowledge Base: Quản lý tập luật
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Callable
from enum import Enum


# ============================================================================
# ENUMS - Định nghĩa các giá trị chuẩn
# ============================================================================

class DegreeLevel(Enum):
    """Độ bệnh TCM"""
    DEGREE_1 = "1"      # Độ 1 - Nhẹ
    DEGREE_2A = "2a"    # Độ 2a - Có nguy cơ biến chứng
    DEGREE_2B = "2b"    # Độ 2b - Biến chứng sớm
    DEGREE_3 = "3"      # Độ 3 - Biến chứng thần kinh
    DEGREE_4 = "4"      # Độ 4 - Biến chứng nặng
    UNKNOWN = "Không xác định"


class AVPU(Enum):
    """Thang đánh giá ý thức"""
    ALERT = "A"         # Tỉnh táo
    VERBAL = "V"        # Đáp ứng lời nói
    PAIN = "P"          # Đáp ứng đau
    UNRESPONSIVE = "U"  # Không đáp ứng


# ============================================================================
# FACTS - Biểu diễn dữ liệu lâm sàng
# ============================================================================

@dataclass
class ClinicalFact:
    """
    Fact base class - Biểu diễn một sự kiện lâm sàng
    Tương tự Fact trong COPD system
    """
    patient_id: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Chuyển fact thành dictionary"""
        return {k: v for k, v in self.__dict__.items() if v is not None}


@dataclass
class DemographicFact(ClinicalFact):
    """Thông tin nhân khẩu học"""
    age_months: Optional[int] = None
    age_years: Optional[float] = None
    weight_kg: Optional[float] = None


@dataclass
class VitalSignFact(ClinicalFact):
    """Dấu hiệu sinh tồn"""
    # Nhiệt độ
    temp_c: Optional[float] = None
    fever_days: Optional[int] = None
    
    # Tuần hoàn
    heart_rate: Optional[int] = None
    hr_no_fever: Optional[int] = None  # Mạch điều chỉnh
    sbp_mmhg: Optional[int] = None
    dbp_mmhg: Optional[int] = None
    pulse_pressure: Optional[int] = None
    
    # Hô hấp
    respiratory_rate: Optional[int] = None
    spo2: Optional[float] = None
    
    # Khác
    gcs: Optional[int] = None
    avpu_level: Optional[str] = None


@dataclass
class SymptomFact(ClinicalFact):
    """Triệu chứng lâm sàng"""
    # Triệu chứng đặc trưng TCM
    rash_hf: bool = False          # Ban tay chân
    oral_ulcer: bool = False       # Loét miệng
    
    # Tiêu hóa
    vomit_per_hour: Optional[float] = None
    
    # Thần kinh
    startle_observed: bool = False     # Giật mình quan sát
    startle_hist_30min: Optional[int] = None  # Số lần giật mình/30p
    somnolent: bool = False            # Li bì
    nystagmus: bool = False            # Rung giật nhãn cầu
    ataxia: bool = False               # Mất điều hòa
    tremor: bool = False               # Run
    limb_weakness: bool = False        # Liệt chi
    cranial_nerve_palsy: bool = False  # Liệt dây TK sọ
    hypertonia: bool = False           # Tăng trương lực cơ
    seizure: bool = False              # Co giật
    coma: bool = False                 # Hôn mê
    
    # Tuần hoàn
    cold_extremities: bool = False     # Chi lạnh
    weak_pulse: bool = False           # Mạch yếu
    mottled_skin: bool = False         # Da tái đốm
    capillary_refill_time: Optional[float] = None  # CRT (giây)
    
    # Hô hấp
    dyspnea: bool = False              # Khó thở
    shallow_breath: bool = False       # Thở nông
    abdominal_breath: bool = False     # Thở bụng
    chest_retraction: bool = False     # Co kéo lồng ngực
    stridor_insp: bool = False         # Thở rít
    
    # Biến chứng nặng
    apnea: bool = False                # Ngưng thở
    resp_irregular_severe: bool = False  # Rối loạn nhịp thở nặng
    pulm_edema_pink_froth: bool = False  # Phù phổi - sùi bọt hồng
    lung_rales_wet: bool = False         # Ran ẩm phổi
    pulse_absent: bool = False           # Mạch không bắt được
    bp_unrecordable: bool = False        # HA không đo được
    
    # Xét nghiệm
    lactate: Optional[float] = None    # Lactate máu (mmol/L)


@dataclass
class PatientData:
    """
    Tổng hợp tất cả facts của bệnh nhân
    Tương tự như working memory trong inference engine
    """
    demographic: DemographicFact = field(default_factory=DemographicFact)
    vital_signs: VitalSignFact = field(default_factory=VitalSignFact)
    symptoms: SymptomFact = field(default_factory=SymptomFact)
    
    def get_all_facts(self) -> Dict:
        """Lấy tất cả facts dưới dạng dictionary"""
        result = {}
        result.update(self.demographic.to_dict())
        result.update(self.vital_signs.to_dict())
        result.update(self.symptoms.to_dict())
        return result
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PatientData':
        """Tạo PatientData từ dictionary"""
        patient = cls()
        
        # Danh sách các trường cho mỗi fact type
        demographic_fields = {'age_months', 'age_years', 'weight_kg', 'patient_id'}
        vital_fields = {
            'temp_c', 'fever_days', 'heart_rate', 'hr_no_fever',
            'sbp_mmhg', 'dbp_mmhg', 'pulse_pressure',
            'respiratory_rate', 'spo2', 'gcs', 'avpu_level'
        }
        
        # Phân loại dữ liệu
        for key, value in data.items():
            if key in demographic_fields:
                setattr(patient.demographic, key, value)
            elif key in vital_fields:
                setattr(patient.vital_signs, key, value)
            else:
                # Còn lại đều là symptoms
                if hasattr(patient.symptoms, key):
                    setattr(patient.symptoms, key, value)
        
        return patient


# ============================================================================
# RULES - Tri thức y khoa
# ============================================================================

@dataclass
class Condition:
    """
    Một điều kiện trong luật
    """
    field: str
    operator: str  # '<', '<=', '>', '>=', '==', '!=', 'in', 'not_in'
    value: Any
    
    def evaluate(self, data: Dict) -> bool:
        """
        Đánh giá điều kiện với dữ liệu
        
        Args:
            data: Dictionary chứa dữ liệu bệnh nhân
            
        Returns:
            True nếu điều kiện thỏa mãn
        """
        # Lấy giá trị field từ data
        if self.field not in data:
            return False
        
        field_value = data[self.field]
        
        # Đánh giá theo operator
        if self.operator == '==':
            return field_value == self.value
        elif self.operator == '!=':
            return field_value != self.value
        elif self.operator == '<':
            return field_value < self.value
        elif self.operator == '<=':
            return field_value <= self.value
        elif self.operator == '>':
            return field_value > self.value
        elif self.operator == '>=':
            return field_value >= self.value
        elif self.operator == 'in':
            return field_value in self.value
        elif self.operator == 'not_in':
            return field_value not in self.value
        else:
            return False
    
    def __str__(self) -> str:
        return f"{self.field} {self.operator} {self.value}"


@dataclass
class Rule:
    """
    Luật chẩn đoán
    Tương tự như Rule trong COPD system với decorator @Rule
    
    Cấu trúc: IF (conditions) THEN (conclusion)
    """
    rule_id: str
    degree: str
    priority: int
    conditions: List[Condition]
    description: str = ""
    source: str = ""
    
    def match(self, data: Dict) -> bool:
        """
        Kiểm tra xem rule có match với dữ liệu không
        Tất cả conditions phải thỏa mãn (AND logic)
        
        Args:
            data: Dictionary chứa dữ liệu bệnh nhân
            
        Returns:
            True nếu tất cả conditions đều thỏa mãn
        """
        return all(cond.evaluate(data) for cond in self.conditions)
    
    def fire(self) -> Dict:
        """
        Kích hoạt rule và trả về kết luận
        Tương tự như declare() trong Experta
        
        Returns:
            Dictionary chứa kết quả
        """
        return {
            'rule_id': self.rule_id,
            'degree': self.degree,
            'priority': self.priority,
            'description': self.description,
            'source': self.source,
            'conditions': [str(c) for c in self.conditions]
        }
    
    def __str__(self) -> str:
        conds_str = " AND ".join(str(c) for c in self.conditions)
        return f"Rule {self.rule_id} (P:{self.priority}): IF {conds_str} THEN Độ {self.degree}"
    
    def __repr__(self) -> str:
        return f"Rule({self.rule_id}, Độ {self.degree}, P:{self.priority})"


@dataclass
class IntermediateRule:
    """
    Luật trung gian - Tạo sự kiện suy diễn mới
    
    Cấu trúc: IF (conditions) THEN (assert new_facts)
    Ví dụ: IF (hr_no_fever > 150 AND age_months < 12) THEN (tachycardia_for_age = True)
    """
    rule_id: str
    priority: int
    conditions: List[Condition]
    derived_facts: Dict[str, Any]  # Facts mới được tạo ra
    description: str = ""
    
    def match(self, data: Dict) -> bool:
        """Kiểm tra xem rule có match với dữ liệu không"""
        return all(cond.evaluate(data) for cond in self.conditions)
    
    def fire(self, working_memory: Dict) -> Dict:
        """
        Kích hoạt rule và thêm facts mới vào working memory
        
        Returns:
            Dictionary chứa thông tin về rule đã fire và facts mới
        """
        # Thêm derived facts vào working memory
        working_memory.update(self.derived_facts)
        
        return {
            'rule_id': self.rule_id,
            'type': 'intermediate',
            'priority': self.priority,
            'description': self.description,
            'derived_facts': self.derived_facts.copy(),
            'conditions': [str(c) for c in self.conditions]
        }
    
    def __str__(self) -> str:
        conds_str = " AND ".join(str(c) for c in self.conditions)
        facts_str = ", ".join(f"{k}={v}" for k, v in self.derived_facts.items())
        return f"IntermediateRule {self.rule_id} (P:{self.priority}): IF {conds_str} THEN ASSERT {facts_str}"
    
    def __repr__(self) -> str:
        return f"IntermediateRule({self.rule_id}, P:{self.priority})"


# ============================================================================
# KNOWLEDGE BASE - Quản lý tập luật
# ============================================================================

class KnowledgeBase:
    """
    Knowledge Base - Quản lý tập luật chẩn đoán TCM
    Hỗ trợ Forward Chaining với intermediate rules
    """
    
    def __init__(self):
        self.rules: List[Rule] = []                      # Rules kết luận cuối cùng
        self.intermediate_rules: List[IntermediateRule] = []  # Rules tạo facts mới
        self._initialize_rules()
        self._initialize_intermediate_rules()
    
    def _initialize_intermediate_rules(self):
        """
        Khởi tạo các luật trung gian (Intermediate Rules)
        Các luật này tạo ra sự kiện suy diễn mới
        """
        
        # ========== LUẬT SUY DIỄN MẠCH NHANH THEO TUỔI ==========
        
        self.add_intermediate_rule(IntermediateRule(
            rule_id='INT-01',
            priority=500,
            conditions=[
                Condition('hr_no_fever', '>', 150),
                Condition('age_months', '<', 12)
            ],
            derived_facts={'tachycardia_for_age': True},
            description='Mạch nhanh cho trẻ <12 tháng (HR >150)'
        ))
        
        self.add_intermediate_rule(IntermediateRule(
            rule_id='INT-02',
            priority=500,
            conditions=[
                Condition('hr_no_fever', '>', 130),
                Condition('age_months', '>=', 12)
            ],
            derived_facts={'tachycardia_for_age': True},
            description='Mạch nhanh cho trẻ ≥12 tháng (HR >130)'
        ))
        
        # ========== LUẬT SUY DIỄN SỐC ==========
        
        self.add_intermediate_rule(IntermediateRule(
            rule_id='INT-03',
            priority=500,
            conditions=[
                Condition('sbp_mmhg', '<', 70),
                Condition('age_months', '<', 12)
            ],
            derived_facts={'shock_present': True, 'hypotension': True},
            description='Sốc: SBP <70 mmHg ở trẻ <12 tháng'
        ))
        
        self.add_intermediate_rule(IntermediateRule(
            rule_id='INT-04',
            priority=500,
            conditions=[
                Condition('sbp_mmhg', '<', 80),
                Condition('age_months', '>=', 12)
            ],
            derived_facts={'shock_present': True, 'hypotension': True},
            description='Sốc: SBP <80 mmHg ở trẻ ≥12 tháng'
        ))
        
        # ========== LUẬT SUY DIỄN RỐI LOẠN TUẦN HOÀN ==========
        
        self.add_intermediate_rule(IntermediateRule(
            rule_id='INT-05',
            priority=450,
            conditions=[
                Condition('capillary_refill_time', '>=', 3)
            ],
            derived_facts={'circulatory_impairment': True},
            description='Rối loạn tuần hoàn: CRT ≥3 giây'
        ))
        
        self.add_intermediate_rule(IntermediateRule(
            rule_id='INT-06',
            priority=450,
            conditions=[
                Condition('cold_extremities', '==', True)
            ],
            derived_facts={'circulatory_impairment': True},
            description='Rối loạn tuần hoàn: Chi lạnh'
        ))
        
        self.add_intermediate_rule(IntermediateRule(
            rule_id='INT-07',
            priority=450,
            conditions=[
                Condition('tachycardia_for_age', '==', True)
            ],
            derived_facts={'circulatory_impairment': True},
            description='Rối loạn tuần hoàn: Mạch nhanh theo tuổi'
        ))
        
        # ========== LUẬT SUY DIỄN BIẾN CHỨNG THẦN KINH ==========
        
        self.add_intermediate_rule(IntermediateRule(
            rule_id='INT-08',
            priority=450,
            conditions=[
                Condition('startle_hist_30min', '>=', 2)
            ],
            derived_facts={'neurological_signs': True, 'startle_frequent': True},
            description='Dấu hiệu thần kinh: Giật mình ≥2 lần/30 phút'
        ))
        
        self.add_intermediate_rule(IntermediateRule(
            rule_id='INT-09',
            priority=450,
            conditions=[
                Condition('somnolent', '==', True)
            ],
            derived_facts={'neurological_signs': True, 'altered_consciousness': True},
            description='Dấu hiệu thần kinh: Li bì'
        ))
        
        self.add_intermediate_rule(IntermediateRule(
            rule_id='INT-10',
            priority=450,
            conditions=[
                Condition('gcs', '<', 10)
            ],
            derived_facts={'neurological_signs': True, 'altered_consciousness': True},
            description='Dấu hiệu thần kinh: GCS <10'
        ))
        
        # ========== LUẬT SUY DIỄN NGUY CƠ CAO ==========
        
        self.add_intermediate_rule(IntermediateRule(
            rule_id='INT-11',
            priority=400,
            conditions=[
                Condition('temp_c', '>=', 39),
                Condition('fever_days', '>=', 3)
            ],
            derived_facts={'high_risk_fever': True},
            description='Sốt cao kéo dài: ≥39°C và ≥3 ngày'
        ))
        
        self.add_intermediate_rule(IntermediateRule(
            rule_id='INT-12',
            priority=400,
            conditions=[
                Condition('neurological_signs', '==', True),
                Condition('circulatory_impairment', '==', True)
            ],
            derived_facts={'multi_organ_involvement': True},
            description='Liên quan nhiều cơ quan: Thần kinh + Tuần hoàn'
        ))
    
    def _initialize_rules(self):
        """Khởi tạo tất cả rules chẩn đoán TCM"""
        
        # ========== ĐỘ 4 (Priority: 400) - BIẾN CHỨNG NẶNG ==========
        
        self.add_rule(Rule(
            rule_id='04-01',
            degree='4',
            priority=400,
            conditions=[Condition('spo2', '<', 92)],
            description='SpO₂ <92%',
            source='QĐ 292/2015 - II.6 (Độ 4)'
        ))
        
        self.add_rule(Rule(
            rule_id='04-02',
            degree='4',
            priority=400,
            conditions=[Condition('apnea', '==', True)],
            description='Ngưng thở',
            source='QĐ 292/2015 - II.6 (Độ 4)'
        ))
        
        self.add_rule(Rule(
            rule_id='04-03',
            degree='4',
            priority=400,
            conditions=[Condition('resp_irregular_severe', '==', True)],
            description='Rối loạn nhịp thở nặng',
            source='QĐ 292/2015 - II.6 (Độ 4)'
        ))
        
        self.add_rule(Rule(
            rule_id='04-04',
            degree='4',
            priority=400,
            conditions=[Condition('pulm_edema_pink_froth', '==', True)],
            description='Phù phổi cấp - sùi bọt hồng',
            source='QĐ 292/2015 - II.6 (Độ 4)'
        ))
        
        self.add_rule(Rule(
            rule_id='04-05',
            degree='4',
            priority=400,
            conditions=[Condition('lung_rales_wet', '==', True)],
            description='Phù phổi - ran ẩm phổi',
            source='QĐ 292/2015 - II.6 (Độ 4)'
        ))
        
        self.add_rule(Rule(
            rule_id='04-06',
            degree='4',
            priority=400,
            conditions=[Condition('coma', '==', True)],
            description='Hôn mê',
            source='QĐ 292/2015 - II.6 (Độ 4)'
        ))
        
        self.add_rule(Rule(
            rule_id='04-07',
            degree='4',
            priority=400,
            conditions=[Condition('gcs', '<=', 8)],
            description='Glasgow Coma Scale ≤8',
            source='QĐ 292/2015 - II.6 (Độ 4)'
        ))
        
        self.add_rule(Rule(
            rule_id='04-08',
            degree='4',
            priority=400,
            conditions=[Condition('avpu_level', 'in', ['P', 'U'])],
            description='AVPU = P (đáp ứng đau) hoặc U (không đáp ứng)',
            source='QĐ 292/2015 - II.6 (Độ 4)'
        ))
        
        self.add_rule(Rule(
            rule_id='04-09',
            degree='4',
            priority=400,
            conditions=[Condition('pulse_absent', '==', True)],
            description='Mạch không bắt được (sốc)',
            source='QĐ 292/2015 - II.6 (Độ 4)'
        ))
        
        self.add_rule(Rule(
            rule_id='04-10',
            degree='4',
            priority=400,
            conditions=[Condition('bp_unrecordable', '==', True)],
            description='Huyết áp không đo được (sốc)',
            source='QĐ 292/2015 - II.6 (Độ 4)'
        ))
        
        self.add_rule(Rule(
            rule_id='04-11',
            degree='4',
            priority=400,
            conditions=[
                Condition('sbp_mmhg', '<', 70),
                Condition('age_months', '<', 12)
            ],
            description='SBP <70 mmHg ở trẻ <12 tháng',
            source='QĐ 292/2015 - II.6 (Độ 4)'
        ))
        
        self.add_rule(Rule(
            rule_id='04-12',
            degree='4',
            priority=400,
            conditions=[
                Condition('sbp_mmhg', '<', 80),
                Condition('age_months', '>=', 12)
            ],
            description='SBP <80 mmHg ở trẻ ≥12 tháng',
            source='QĐ 292/2015 - II.6 (Độ 4)'
        ))
        
        self.add_rule(Rule(
            rule_id='04-13',
            degree='4',
            priority=400,
            conditions=[Condition('pulse_pressure', '<', 25)],
            description='Chênh áp <25 mmHg (mạch nhanh nhỏ)',
            source='QĐ 292/2015 - II.6 (Độ 4)'
        ))
        
        self.add_rule(Rule(
            rule_id='04-14',
            degree='4',
            priority=400,
            conditions=[Condition('lactate', '>=', 4)],
            description='Lactate ≥4 mmol/L',
            source='QĐ 292/2015 - II.6 (Độ 4)'
        ))
        
        # ========== ĐỘ 3 (Priority: 300) - BIẾN CHỨNG THẦN KINH ==========
        
        self.add_rule(Rule(
            rule_id='03-01',
            degree='3',
            priority=300,
            conditions=[Condition('startle_hist_30min', '>=', 2)],
            description='Giật mình ≥2 lần/30 phút (tiền sử)',
            source='QĐ 292/2015 - II.5 (Độ 3)'
        ))
        
        self.add_rule(Rule(
            rule_id='03-02',
            degree='3',
            priority=300,
            conditions=[Condition('somnolent', '==', True)],
            description='Li bì',
            source='QĐ 292/2015 - II.5 (Độ 3)'
        ))
        
        self.add_rule(Rule(
            rule_id='03-03',
            degree='3',
            priority=300,
            conditions=[Condition('nystagmus', '==', True)],
            description='Rung giật nhãn cầu (nystagmus)',
            source='QĐ 292/2015 - II.5 (Độ 3)'
        ))
        
        self.add_rule(Rule(
            rule_id='03-04',
            degree='3',
            priority=300,
            conditions=[Condition('ataxia', '==', True)],
            description='Mất điều hòa vận động (ataxia)',
            source='QĐ 292/2015 - II.5 (Độ 3)'
        ))
        
        self.add_rule(Rule(
            rule_id='03-05',
            degree='3',
            priority=300,
            conditions=[Condition('tremor', '==', True)],
            description='Run',
            source='QĐ 292/2015 - II.5 (Độ 3)'
        ))
        
        self.add_rule(Rule(
            rule_id='03-06',
            degree='3',
            priority=300,
            conditions=[Condition('limb_weakness', '==', True)],
            description='Liệt chi',
            source='QĐ 292/2015 - II.5 (Độ 3)'
        ))
        
        self.add_rule(Rule(
            rule_id='03-07',
            degree='3',
            priority=300,
            conditions=[Condition('cranial_nerve_palsy', '==', True)],
            description='Liệt dây thần kinh sọ',
            source='QĐ 292/2015 - II.5 (Độ 3)'
        ))
        
        self.add_rule(Rule(
            rule_id='03-08',
            degree='3',
            priority=300,
            conditions=[Condition('hypertonia', '==', True)],
            description='Tăng trương lực cơ',
            source='QĐ 292/2015 - II.5 (Độ 3)'
        ))
        
        self.add_rule(Rule(
            rule_id='03-09',
            degree='3',
            priority=300,
            conditions=[Condition('seizure', '==', True)],
            description='Co giật',
            source='QĐ 292/2015 - II.5 (Độ 3)'
        ))
        
        self.add_rule(Rule(
            rule_id='03-10',
            degree='3',
            priority=300,
            conditions=[Condition('gcs', '<=', 9)],
            description='GCS 9 (ý thức giảm)',
            source='QĐ 292/2015 - II.5 (Độ 3)'
        ))
        
        self.add_rule(Rule(
            rule_id='03-11',
            degree='3',
            priority=300,
            conditions=[Condition('spo2', '<', 94)],
            description='SpO₂ <94%',
            source='QĐ 292/2015 - II.5 (Độ 3)'
        ))
        
        # ========== ĐỘ 2B (Priority: 250) - RỐI LOẠN TUẦN HOÀN ==========
        
        self.add_rule(Rule(
            rule_id='2b-01',
            degree='2b',
            priority=250,
            conditions=[
                Condition('hr_no_fever', '>', 150),
                Condition('age_months', '<', 12)
            ],
            description='Mạch >150 bpm (không sốt) ở trẻ <12 tháng',
            source='QĐ 292/2015 - II.4.b (Độ 2b)'
        ))
        
        self.add_rule(Rule(
            rule_id='2b-02',
            degree='2b',
            priority=250,
            conditions=[
                Condition('hr_no_fever', '>', 130),
                Condition('age_months', '>=', 12)
            ],
            description='Mạch >130 bpm (không sốt) ở trẻ ≥12 tháng',
            source='QĐ 292/2015 - II.4.b (Độ 2b)'
        ))
        
        self.add_rule(Rule(
            rule_id='2b-03',
            degree='2b',
            priority=250,
            conditions=[Condition('capillary_refill_time', '>=', 3)],
            description='Thời gian chảy màu mao mạch ≥3 giây (CRT ≥3s)',
            source='QĐ 292/2015 - II.4.b (Độ 2b)'
        ))
        
        self.add_rule(Rule(
            rule_id='2b-04',
            degree='2b',
            priority=250,
            conditions=[Condition('cold_extremities', '==', True)],
            description='Chi lạnh',
            source='QĐ 292/2015 - II.4.b (Độ 2b)'
        ))
        
        self.add_rule(Rule(
            rule_id='2b-05',
            degree='2b',
            priority=250,
            conditions=[Condition('weak_pulse', '==', True)],
            description='Mạch nhanh, nhỏ, yếu',
            source='QĐ 292/2015 - II.4.b (Độ 2b)'
        ))
        
        self.add_rule(Rule(
            rule_id='2b-06',
            degree='2b',
            priority=250,
            conditions=[Condition('mottled_skin', '==', True)],
            description='Da tái, xuất hiện đốm tím',
            source='QĐ 292/2015 - II.4.b (Độ 2b)'
        ))
        
        self.add_rule(Rule(
            rule_id='2b-07',
            degree='2b',
            priority=250,
            conditions=[
                Condition('lactate', '>=', 2),
                Condition('lactate', '<', 4)
            ],
            description='Lactate 2-4 mmol/L',
            source='QĐ 292/2015 - II.4.b (Độ 2b)'
        ))
        
        # ========== ĐỘ 2A (Priority: 200) - CÓ NGUY CƠ BIẾN CHỨNG ==========
        
        self.add_rule(Rule(
            rule_id='2a-01',
            degree='2a',
            priority=200,
            conditions=[
                Condition('temp_c', '>=', 39),
                Condition('fever_days', '>=', 3)
            ],
            description='Sốt ≥39°C kéo dài ≥3 ngày',
            source='QĐ 292/2015 - II.4.a (Độ 2a)'
        ))
        
        self.add_rule(Rule(
            rule_id='2a-02',
            degree='2a',
            priority=200,
            conditions=[Condition('vomit_per_hour', '>', 2)],
            description='Nôn >2 lần/giờ',
            source='QĐ 292/2015 - II.4.a (Độ 2a)'
        ))
        
        self.add_rule(Rule(
            rule_id='2a-03',
            degree='2a',
            priority=200,
            conditions=[Condition('startle_observed', '==', True)],
            description='Giật mình (quan sát được)',
            source='QĐ 292/2015 - II.4.a (Độ 2a)'
        ))
        
        # ========== ĐỘ 1 (Priority: 100) - BỆNH KHÔNG BIẾN CHỨNG ==========
        
        self.add_rule(Rule(
            rule_id='1-01',
            degree='1',
            priority=100,
            conditions=[
                Condition('rash_hf', '==', True),
                Condition('oral_ulcer', '==', True)
            ],
            description='Phát ban tay chân + loét miệng',
            source='QĐ 292/2015 - II.3 (Độ 1)'
        ))
        
        self.add_rule(Rule(
            rule_id='1-02',
            degree='1',
            priority=100,
            conditions=[
                Condition('rash_hf', '==', True),
                Condition('temp_c', '>=', 37.5)
            ],
            description='Sốt + phát ban tay chân',
            source='QĐ 292/2015 - II.3 (Độ 1)'
        ))
    
    def add_rule(self, rule: Rule):
        """Thêm một luật vào knowledge base"""
        self.rules.append(rule)
    
    def add_intermediate_rule(self, rule: IntermediateRule):
        """Thêm một luật trung gian vào knowledge base"""
        self.intermediate_rules.append(rule)
    
    def get_rule(self, rule_id: str) -> Optional[Rule]:
        """Lấy rule theo ID"""
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        return None
    
    def get_intermediate_rule(self, rule_id: str) -> Optional[IntermediateRule]:
        """Lấy intermediate rule theo ID"""
        for rule in self.intermediate_rules:
            if rule.rule_id == rule_id:
                return rule
        return None
    
    def get_rules_by_degree(self, degree: str) -> List[Rule]:
        """Lấy tất cả rules của một độ bệnh"""
        return [r for r in self.rules if r.degree == degree]
    
    def get_statistics(self) -> Dict:
        """Thống kê về knowledge base"""
        stats = {
            'total_rules': len(self.rules),
            'total_intermediate_rules': len(self.intermediate_rules),
            'by_degree': {},
            'by_priority': {}
        }
        
        for rule in self.rules:
            # Đếm theo degree
            stats['by_degree'][rule.degree] = stats['by_degree'].get(rule.degree, 0) + 1
            
            # Đếm theo priority
            stats['by_priority'][rule.priority] = stats['by_priority'].get(rule.priority, 0) + 1
        
        return stats
    
    def __len__(self) -> int:
        return len(self.rules) + len(self.intermediate_rules)
    
    def __iter__(self):
        return iter(self.rules)
