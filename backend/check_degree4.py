import json

with open('data/treatment.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

degree4 = [r for r in data['treatment_rules'] if r['disease_level'] == '4'][0]
print(f"Số category: {len(degree4['treatments'])}")
for i, t in enumerate(degree4['treatments']):
    print(f"{i+1}. {t['category']}")
    if 'medications' in t:
        print(f"   - Có {len(t['medications'])} loại thuốc")
    if 'interventions' in t:
        print(f"   - Có {len(t['interventions'])} can thiệp")
    if 'vital_signs_frequent' in t:
        print(f"   - Có theo dõi sinh hiệu")
    if 'invasive_monitoring' in t:
        print(f"   - Có theo dõi xâm lấn")
