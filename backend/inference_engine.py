"""
Inference Engine Module - TCM Diagnosis Expert System
Mô hình hóa theo COPD Expert System

Thực hiện:
- Forward Chaining: Suy diễn tiến từ dữ liệu đến kết luận
- Conflict Resolution: Giải quyết xung đột bằng Priority
- Working Memory: Quản lý facts và matched rules
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime

from knowledge_base import (
    Rule,
    IntermediateRule,
    KnowledgeBase, 
    PatientData,
    DegreeLevel
)


# ============================================================================
# WORKING MEMORY - Bộ nhớ làm việc
# ============================================================================

@dataclass
class WorkingMemory:
    """
    Working Memory - Lưu trữ facts và trạng thái suy diễn
    Hỗ trợ tracking derived facts (sự kiện suy diễn)
    """
    facts: Dict = field(default_factory=dict)
    derived_facts: Dict = field(default_factory=dict)  # Facts được suy diễn
    matched_rules: List[Dict] = field(default_factory=list)
    fired_rules: Set[str] = field(default_factory=set)
    fired_intermediate_rules: List[Dict] = field(default_factory=list)  # Track intermediate rules
    conclusion: Optional[Dict] = None
    
    def add_fact(self, key: str, value):
        """Thêm fact vào working memory"""
        self.facts[key] = value
    
    def add_facts(self, facts: Dict):
        """Thêm nhiều facts"""
        self.facts.update(facts)
    
    def add_derived_fact(self, key: str, value):
        """Thêm derived fact (fact được suy diễn)"""
        self.derived_facts[key] = value
        self.facts[key] = value  # Cũng thêm vào facts chung
    
    def add_derived_facts(self, facts: Dict):
        """Thêm nhiều derived facts"""
        self.derived_facts.update(facts)
        self.facts.update(facts)
    
    def get_fact(self, key: str):
        """Lấy giá trị của fact"""
        return self.facts.get(key)
    
    def get_all_facts(self) -> Dict:
        """Lấy tất cả facts (bao gồm cả derived facts)"""
        return self.facts.copy()
    
    def record_match(self, rule_result: Dict):
        """Ghi nhận rule đã match"""
        self.matched_rules.append(rule_result)
        self.fired_rules.add(rule_result['rule_id'])
    
    def record_intermediate_rule(self, rule_result: Dict):
        """Ghi nhận intermediate rule đã fire"""
        self.fired_intermediate_rules.append(rule_result)
        self.fired_rules.add(rule_result['rule_id'])
    
    def set_conclusion(self, conclusion: Dict):
        """Đặt kết luận cuối cùng"""
        self.conclusion = conclusion
    
    def clear(self):
        """Xóa toàn bộ working memory"""
        self.facts.clear()
        self.derived_facts.clear()
        self.matched_rules.clear()
        self.fired_rules.clear()
        self.fired_intermediate_rules.clear()
        self.conclusion = None


# ============================================================================
# CONFLICT RESOLUTION STRATEGY
# ============================================================================

class ConflictResolutionStrategy:
    """
    Chiến lược giải quyết xung đột khi có nhiều rules match
    """
    
    @staticmethod
    def priority_based(matched_rules: List[Dict]) -> Dict:
        """
        Priority-based selection: Chọn rule có priority cao nhất
        Nếu bằng nhau, chọn rule đầu tiên
        
        Args:
            matched_rules: Danh sách rules đã match
            
        Returns:
            Rule có priority cao nhất
        """
        if not matched_rules:
            return None
        
        # Sắp xếp theo priority giảm dần
        sorted_rules = sorted(
            matched_rules, 
            key=lambda x: x['priority'], 
            reverse=True
        )
        
        return sorted_rules[0]
    
    @staticmethod
    def severity_based(matched_rules: List[Dict]) -> Dict:
        """
        Severity-based: Ưu tiên độ bệnh nặng hơn
        4 > 3 > 2b > 2a > 1
        """
        degree_order = {'4': 5, '3': 4, '2b': 3, '2a': 2, '1': 1}
        
        if not matched_rules:
            return None
        
        sorted_rules = sorted(
            matched_rules,
            key=lambda x: degree_order.get(x['degree'], 0),
            reverse=True
        )
        
        return sorted_rules[0]
    
    @staticmethod
    def recency_based(matched_rules: List[Dict]) -> Dict:
        """
        Recency-based: Chọn rule mới nhất (đã match gần đây nhất)
        """
        if not matched_rules:
            return None
        
        return matched_rules[-1]


# ============================================================================
# INFERENCE ENGINE - Forward Chaining
# ============================================================================

class InferenceEngine:
    """
    Inference Engine - Thực hiện suy diễn tiến (Forward Chaining)
    
    Quy trình:
    1. Load facts vào working memory
    2. Match phase: Tìm tất cả rules thỏa mãn
    3. Conflict resolution: Chọn rule tốt nhất
    4. Execute: Kích hoạt rule và tạo kết luận
    5. Return: Trả về kết quả chẩn đoán
    """
    
    def __init__(self, knowledge_base: Optional[KnowledgeBase] = None):
        """
        Khởi tạo inference engine
        
        Args:
            knowledge_base: Knowledge base chứa rules. Nếu None, tạo mới.
        """
        self.kb = knowledge_base or KnowledgeBase()
        self.working_memory = WorkingMemory()
        self.conflict_resolver = ConflictResolutionStrategy.priority_based
        self.inference_trace: List[str] = []
        
    def reset(self):
        """Reset engine về trạng thái ban đầu"""
        self.working_memory.clear()
        self.inference_trace.clear()
    
    def set_conflict_resolution(self, strategy: str):
        """
        Đặt chiến lược giải quyết xung đột
        
        Args:
            strategy: 'priority', 'severity', hoặc 'recency'
        """
        strategies = {
            'priority': ConflictResolutionStrategy.priority_based,
            'severity': ConflictResolutionStrategy.severity_based,
            'recency': ConflictResolutionStrategy.recency_based
        }
        
        if strategy in strategies:
            self.conflict_resolver = strategies[strategy]
            self._trace(f"Conflict resolution strategy: {strategy}")
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
    
    def _trace(self, message: str):
        """Ghi lại quá trình suy diễn"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.inference_trace.append(f"[{timestamp}] {message}")
    
    def load_facts(self, patient_data: PatientData):
        """
        Load dữ liệu bệnh nhân vào working memory
        
        Args:
            patient_data: Dữ liệu bệnh nhân
        """
        facts = patient_data.get_all_facts()
        self.working_memory.add_facts(facts)
        self._trace(f"Loaded {len(facts)} facts into working memory")
    
    def load_facts_from_dict(self, facts: Dict):
        """
        Load facts từ dictionary
        
        Args:
            facts: Dictionary chứa dữ liệu
        """
        self.working_memory.add_facts(facts)
        self._trace(f"Loaded {len(facts)} facts from dictionary")
    
    def match_phase(self) -> List[Rule]:
        """
        MATCH PHASE: Tìm tất cả rules match với working memory
        
        Returns:
            Danh sách rules đã match
        """
        matched_rules = []
        facts = self.working_memory.facts
        
        self._trace(f"Starting match phase with {len(self.kb.rules)} rules")
        
        for rule in self.kb.rules:
            if rule.match(facts):
                matched_rules.append(rule)
                self._trace(f"  ✓ Matched: {rule.rule_id} (Độ {rule.degree}, P:{rule.priority})")
        
        self._trace(f"Match phase complete: {len(matched_rules)} rules matched")
        return matched_rules
    
    def conflict_resolution(self, matched_rules: List[Rule]) -> Optional[Rule]:
        """
        CONFLICT RESOLUTION: Chọn rule tốt nhất từ tập matched rules
        
        Args:
            matched_rules: Danh sách rules đã match
            
        Returns:
            Rule được chọn, hoặc None nếu không có rule nào
        """
        if not matched_rules:
            self._trace("No rules to resolve")
            return None
        
        # Chuyển rules thành dicts để resolve
        rule_dicts = [r.fire() for r in matched_rules]
        
        # Áp dụng conflict resolution strategy
        selected_dict = self.conflict_resolver(rule_dicts)
        
        # Tìm rule object tương ứng
        selected_rule = next(
            (r for r in matched_rules if r.rule_id == selected_dict['rule_id']),
            None
        )
        
        if selected_rule:
            self._trace(
                f"Selected rule: {selected_rule.rule_id} "
                f"(Độ {selected_rule.degree}, P:{selected_rule.priority})"
            )
        
        return selected_rule
    
    def execute_phase(self, selected_rule: Rule) -> Dict:
        """
        EXECUTE PHASE: Kích hoạt rule và tạo kết luận
        
        Args:
            selected_rule: Rule được chọn
            
        Returns:
            Kết quả chẩn đoán
        """
        if not selected_rule:
            return None
        
        result = selected_rule.fire()
        self.working_memory.record_match(result)
        self._trace(f"Fired rule: {selected_rule.rule_id}")
        
        return result
    
    def forward_chaining_cycle(self, max_iterations: int = 10) -> bool:
        """
        FORWARD CHAINING - Vòng lặp suy diễn tiến theo thuật toán
        
        Thuật toán (theo slide):
        while (KL chưa nằm trong Known) do
            2.1. Tìm luật r để áp dụng: gt(r) ⊂ Known, kl(r) ∉ Known
            2.2. if (không có r) then Dừng
            2.3. Thêm r vào Solution; thêm kl(r) vào Known
        
        Args:
            max_iterations: Số vòng lặp tối đa để tránh vòng lặp vô hạn
            
        Returns:
            True nếu tìm được kết luận (degree), False nếu không
        """
        iteration = 0
        
        self._trace(f"=== Starting Forward Chaining Cycle ===")
        self._trace(f"Initial facts: {len(self.working_memory.facts)} facts")
        
        while iteration < max_iterations:
            iteration += 1
            self._trace(f"\n--- Iteration {iteration} ---")
            
            # Kiểm tra xem đã có kết luận (degree) chưa
            if 'final_degree' in self.working_memory.facts:
                self._trace(f"✓ Goal reached: final_degree = {self.working_memory.facts['final_degree']}")
                return True
            
            # 2.1. Tìm luật r: gt(r) ⊂ Known và kl(r) ∉ Known
            facts = self.working_memory.get_all_facts()
            
            # Tìm intermediate rules khớp (chưa fire)
            applicable_intermediate = []
            for rule in self.kb.intermediate_rules:
                if rule.rule_id not in self.working_memory.fired_rules and rule.match(facts):
                    # Kiểm tra xem derived facts đã có chưa
                    new_facts = any(k not in facts for k in rule.derived_facts.keys())
                    if new_facts:
                        applicable_intermediate.append(rule)
                        self._trace(f"  Found applicable intermediate rule: {rule.rule_id}")
            
            # Tìm conclusion rules khớp
            applicable_conclusion = []
            for rule in self.kb.rules:
                if rule.rule_id not in self.working_memory.fired_rules and rule.match(facts):
                    applicable_conclusion.append(rule)
                    self._trace(f"  Found applicable conclusion rule: {rule.rule_id}")
            
            # 2.2. if (không có r) then Dừng
            if not applicable_intermediate and not applicable_conclusion:
                self._trace("No more applicable rules. Stopping.")
                return False
            
            # 2.3. Thêm r vào Solution; thêm kl(r) vào Known
            
            # Ưu tiên fire intermediate rules trước
            if applicable_intermediate:
                # Chọn rule có priority cao nhất
                rule_to_fire = max(applicable_intermediate, key=lambda r: r.priority)
                
                self._trace(f"→ Firing intermediate rule: {rule_to_fire.rule_id}")
                result = rule_to_fire.fire(self.working_memory.facts)
                self.working_memory.record_intermediate_rule(result)
                self.working_memory.add_derived_facts(rule_to_fire.derived_facts)
                
                self._trace(f"  Derived facts: {rule_to_fire.derived_facts}")
                self._trace(f"  Total facts now: {len(self.working_memory.facts)}")
                
            # Nếu có conclusion rule, kiểm tra xem có thể kết luận không
            elif applicable_conclusion:
                # Chọn rule theo THỨ TỰ ƯU TIÊN: Độ 4 → 3 → 2b → 2a → 1
                # Dừng ngay khi tìm thấy độ đầu tiên phù hợp
                degree_priority_order = ['4', '3', '2b', '2a', '1']
                
                selected_rule = None
                for target_degree in degree_priority_order:
                    # Tìm rules của độ hiện tại
                    rules_for_degree = [r for r in applicable_conclusion if r.degree == target_degree]
                    if rules_for_degree:
                        # Tìm thấy độ này → Chọn rule đầu tiên và DỪNG NGAY
                        selected_rule = rules_for_degree[0]
                        self._trace(f"  Sequential selection: Found degree {target_degree}, stopping search")
                        break
                
                if selected_rule:
                    self._trace(f"→ Firing conclusion rule: {selected_rule.rule_id}")
                    result = selected_rule.fire()
                    self.working_memory.record_match(result)
                    
                    # Thêm kết luận vào working memory
                    self.working_memory.add_derived_fact('final_degree', selected_rule.degree)
                    self._trace(f"  Conclusion: Degree = {selected_rule.degree}")
                    return True
        
        self._trace(f"⚠ Max iterations ({max_iterations}) reached")
        return False
    
    def run(self, patient_data: PatientData) -> Dict:
        """
        Chạy inference engine với Forward Chaining đầy đủ
        
        Args:
            patient_data: Dữ liệu bệnh nhân
            
        Returns:
            Kết quả chẩn đoán
        """
        self.reset()
        self._trace("=== Inference Engine Started (Multi-Step Forward Chaining) ===")
        
        # Bước 1: Solution = []; Known = GT
        self.load_facts(patient_data)
        
        # Bước 2: Forward Chaining Cycle
        goal_reached = self.forward_chaining_cycle(max_iterations=10)
        
        # Bước 3: Tạo kết quả
        if goal_reached and 'final_degree' in self.working_memory.facts:
            final_degree = self.working_memory.facts['final_degree']
            
            # Tìm primary rule (rule đã cho kết luận)
            primary_rule = None
            if self.working_memory.matched_rules:
                primary_rule = self.working_memory.matched_rules[-1]  # Rule cuối cùng
            
            conclusion = {
                'success': True,
                'degree': final_degree,
                'primary_rule': primary_rule,
                'all_matched_rules': self.working_memory.matched_rules,
                'fired_intermediate_rules': self.working_memory.fired_intermediate_rules,
                'derived_facts': self.working_memory.derived_facts.copy(),
                'total_matched': len(self.working_memory.matched_rules),
                'total_iterations': len(self.working_memory.fired_intermediate_rules) + 1,
                'input_facts': {k: v for k, v in self.working_memory.facts.items() 
                               if k not in self.working_memory.derived_facts},
                'all_facts': self.working_memory.get_all_facts(),
                'inference_trace': self.inference_trace.copy()
            }
        else:
            # Không tìm được kết luận
            conclusion = {
                'success': False,
                'degree': DegreeLevel.UNKNOWN.value,
                'primary_rule': None,
                'all_matched_rules': [],
                'fired_intermediate_rules': self.working_memory.fired_intermediate_rules,
                'derived_facts': self.working_memory.derived_facts.copy(),
                'total_matched': 0,
                'input_facts': self.working_memory.facts.copy(),
                'message': 'Không tìm được kết luận. Cần bổ sung thông tin lâm sàng.',
                'inference_trace': self.inference_trace.copy()
            }
        
        self.working_memory.set_conclusion(conclusion)
        self._trace("=== Inference Engine Completed ===")
        
        return conclusion
    
    def run_from_dict(self, facts: Dict) -> Dict:
        """
        Chạy inference engine với facts dạng dictionary
        Sử dụng Forward Chaining đầy đủ
        
        Args:
            facts: Dictionary chứa dữ liệu lâm sàng
            
        Returns:
            Kết quả chẩn đoán
        """
        self.reset()
        self._trace("=== Inference Engine Started (from dict, Multi-Step FC) ===")
        
        # Bước 1: Solution = []; Known = GT
        self.load_facts_from_dict(facts)
        
        # Bước 2: Forward Chaining Cycle
        goal_reached = self.forward_chaining_cycle(max_iterations=10)
        
        # Bước 3: Tạo kết quả
        if goal_reached and 'final_degree' in self.working_memory.facts:
            final_degree = self.working_memory.facts['final_degree']
            
            # Tìm primary rule
            primary_rule = None
            if self.working_memory.matched_rules:
                primary_rule = self.working_memory.matched_rules[-1]
            
            conclusion = {
                'success': True,
                'degree': final_degree,
                'primary_rule': primary_rule,
                'all_matched_rules': self.working_memory.matched_rules,
                'fired_intermediate_rules': self.working_memory.fired_intermediate_rules,
                'derived_facts': self.working_memory.derived_facts.copy(),
                'total_matched': len(self.working_memory.matched_rules),
                'total_iterations': len(self.working_memory.fired_intermediate_rules) + 1,
                'input_facts': {k: v for k, v in self.working_memory.facts.items() 
                               if k not in self.working_memory.derived_facts},
                'all_facts': self.working_memory.get_all_facts(),
                'inference_trace': self.inference_trace.copy()
            }
        else:
            conclusion = {
                'success': False,
                'degree': DegreeLevel.UNKNOWN.value,
                'primary_rule': None,
                'all_matched_rules': [],
                'fired_intermediate_rules': self.working_memory.fired_intermediate_rules,
                'derived_facts': self.working_memory.derived_facts.copy(),
                'total_matched': 0,
                'input_facts': self.working_memory.facts.copy(),
                'message': 'Không tìm được kết luận. Cần bổ sung thông tin lâm sàng.',
                'inference_trace': self.inference_trace.copy()
            }
        
        self.working_memory.set_conclusion(conclusion)
        self._trace("=== Inference Engine Completed ===")
        
        return conclusion
    
    def run_legacy(self, patient_data: PatientData) -> Dict:
        """
        Chạy inference engine - Phiên bản cũ (single-step)
        Giữ lại để tương thích ngược
        
        Args:
            patient_data: Dữ liệu bệnh nhân
            
        Returns:
            Kết quả chẩn đoán
        """
        self.reset()
        self._trace("=== Inference Engine Started (Legacy Single-Step) ===")
        
        # 1. Load facts
        self.load_facts(patient_data)
        
        # 2. Match phase
        matched_rules = self.match_phase()
        
        # 3. Conflict resolution
        selected_rule = self.conflict_resolution(matched_rules)
        
        # 4. Execute
        if selected_rule:
            primary_result = self.execute_phase(selected_rule)
            
            # Record tất cả matched rules
            for rule in matched_rules:
                if rule.rule_id != selected_rule.rule_id:
                    self.working_memory.record_match(rule.fire())
            
            # Tạo conclusion
            conclusion = {
                'success': True,
                'degree': selected_rule.degree,
                'priority': selected_rule.priority,
                'primary_rule': primary_result,
                'all_matched_rules': self.working_memory.matched_rules,
                'total_matched': len(matched_rules),
                'input_facts': self.working_memory.facts.copy(),
                'inference_trace': self.inference_trace.copy()
            }
        else:
            # Không có rule nào match
            conclusion = {
                'success': False,
                'degree': DegreeLevel.UNKNOWN.value,
                'priority': 0,
                'primary_rule': None,
                'all_matched_rules': [],
                'total_matched': 0,
                'input_facts': self.working_memory.facts.copy(),
                'message': 'Không có luật nào thỏa mãn. Cần bổ sung thông tin lâm sàng.',
                'inference_trace': self.inference_trace.copy()
            }
        
        self.working_memory.set_conclusion(conclusion)
        self._trace("=== Inference Engine Completed (Legacy) ===")
        
        return conclusion
    
    def explain(self, verbose: bool = False) -> str:
        """
        Giải thích kết quả suy diễn
        
        Args:
            verbose: Hiển thị chi tiết trace hay không
            
        Returns:
            Chuỗi giải thích
        """
        if not self.working_memory.conclusion:
            return "Chưa có kết quả suy diễn"
        
        result = self.working_memory.conclusion
        lines = []
        
        lines.append("="*80)
        lines.append("GIẢI THÍCH QUÁ TRÌNH SUY DIỄN (FORWARD CHAINING)")
        lines.append("="*80)
        
        if result['success']:
            lines.append(f"\n✓ KẾT LUẬN: Độ {result['degree']}")
            
            # Hiển thị intermediate rules đã fire
            if result.get('fired_intermediate_rules'):
                lines.append(f"\n🔄 LUẬT TRUNG GIAN ĐÃ FIRE ({len(result['fired_intermediate_rules'])}):")
                for i, r in enumerate(result['fired_intermediate_rules'], 1):
                    lines.append(f"   Bước {i}: [{r['rule_id']}] {r['description']}")
                    lines.append(f"           → Tạo: {r['derived_facts']}")
            
            # Hiển thị derived facts
            if result.get('derived_facts'):
                lines.append(f"\n💡 SỰ KIỆN SUY DIỄN ({len(result['derived_facts'])}):")
                for k, v in result['derived_facts'].items():
                    lines.append(f"   • {k} = {v}")
            
            # Luật kết luận
            if result.get('primary_rule'):
                rule = result['primary_rule']
                lines.append(f"\n📋 LUẬT KẾT LUẬN:")
                lines.append(f"   • ID: {rule['rule_id']}")
                lines.append(f"   • Mô tả: {rule['description']}")
                lines.append(f"   • Nguồn: {rule['source']}")
            
            lines.append(f"\n📊 SỐ VÒNG LẶP: {result.get('total_iterations', 1)}")
            
        else:
            lines.append(f"\n✗ {result.get('message', 'Không xác định')}")
            
            # Vẫn hiển thị các bước đã thực hiện
            if result.get('fired_intermediate_rules'):
                lines.append(f"\n🔄 ĐÃ THỰC HIỆN {len(result['fired_intermediate_rules'])} BƯỚC:")
                for i, r in enumerate(result['fired_intermediate_rules'], 1):
                    lines.append(f"   Bước {i}: [{r['rule_id']}] {r['description']}")
        
        if verbose and 'inference_trace' in result:
            lines.append(f"\n🔍 TRACE SUY DIỄN CHI TIẾT:")
            for trace_line in result['inference_trace']:
                lines.append(f"   {trace_line}")
        
        lines.append("="*80)
        
        return "\n".join(lines)
    
    def get_knowledge_base_stats(self) -> Dict:
        """Lấy thống kê về knowledge base"""
        return self.kb.get_statistics()
