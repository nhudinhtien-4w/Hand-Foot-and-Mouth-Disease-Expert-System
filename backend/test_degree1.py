"""
Test script để kiểm tra logic phân độ 1
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from simple_inference import SimpleInferenceEngine

# Load classification engine
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
classification_engine = SimpleInferenceEngine(os.path.join(BASE_DIR, 'data', 'classification_level_rules.json'))

print("=" * 60)
print("TEST PHÂN ĐỘ 1")
print("=" * 60)

# Test 1: Chỉ có loét miệng
print("\n1. TEST: Chỉ có loét miệng")
result = classification_engine.diagnose({
    'mouth_ulcer': True
})
print(f"   Kết quả: {result.get('success')}")
print(f"   Độ: {result.get('conclusions', {}).get('disease_level')}")
print(f"   Mô tả: {result.get('conclusions', {}).get('description')}")
print(f"   Matched rules: {len(result.get('matched_rules', []))}")

# Test 2: Chỉ có phát ban
print("\n2. TEST: Chỉ có phát ban")
result = classification_engine.diagnose({
    'rash_hand_foot_mouth': True
})
print(f"   Kết quả: {result.get('success')}")
print(f"   Độ: {result.get('conclusions', {}).get('disease_level')}")
print(f"   Mô tả: {result.get('conclusions', {}).get('description')}")
print(f"   Matched rules: {len(result.get('matched_rules', []))}")

# Test 3: Không có gì (data rỗng)
print("\n3. TEST: Không có triệu chứng nào")
result = classification_engine.diagnose({})
print(f"   Kết quả: {result.get('success')}")
print(f"   Độ: {result.get('conclusions', {}).get('disease_level')}")
print(f"   Mô tả: {result.get('conclusions', {}).get('description')}")
print(f"   Matched rules: {len(result.get('matched_rules', []))}")
if not result.get('success'):
    print(f"   Lỗi: {result.get('explanation')}")

# Test 4: Có cả loét miệng và phát ban
print("\n4. TEST: Có cả loét miệng và phát ban")
result = classification_engine.diagnose({
    'mouth_ulcer': True,
    'rash_hand_foot_mouth': True
})
print(f"   Kết quả: {result.get('success')}")
print(f"   Độ: {result.get('conclusions', {}).get('disease_level')}")
print(f"   Mô tả: {result.get('conclusions', {}).get('description')}")
print(f"   Matched rules: {len(result.get('matched_rules', []))}")

print("\n" + "=" * 60)
