// JavaScript cho TCM Diagnosis System

// API endpoint
const API_URL = '/api/diagnose';

// Hàm chẩn đoán
async function diagnose() {
    // Thu thập dữ liệu từ form
    const data = collectFormData();
    
    // Validate
    if (Object.keys(data).length === 0) {
        showError('Vui lòng nhập ít nhất một thông tin bệnh nhân');
        return;
    }
    
    // Hiển thị loading
    showLoading();
    
    try {
        // Gọi API
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error('Lỗi kết nối API');
        }
        
        const result = await response.json();
        
        // Hiển thị kết quả
        displayResult(result);
        
    } catch (error) {
        showError('Lỗi: ' + error.message);
    }
}

// Thu thập dữ liệu từ form
function collectFormData() {
    const data = {};
    
    // Tính tổng tuổi bằng tháng từ năm + tháng
    const age_years = parseFloat(document.getElementById('age_years')?.value || 0);
    const age_months_input = parseFloat(document.getElementById('age_months_input')?.value || 0);
    const total_age_months = (age_years * 12) + age_months_input;
    if (total_age_months > 0) {
        data['age_months'] = total_age_months;
    }
    
    // Các trường số khác
    const numberFields = [
        'fever_temp_c', 'fever_days', 'startle_per_30min',
        'hr_no_fever', 'gcs', 'sbp', 'spo2', 'pulse_pressure'
    ];
    
    numberFields.forEach(field => {
        const value = document.getElementById(field)?.value;
        if (value !== '' && value !== null) {
            data[field] = parseFloat(value);
        }
    });
    
    // Các trường boolean (checkbox)
    const booleanFields = [
        'rash_hand_foot_mouth', 'mouth_ulcer', 'startle_observed',
        'vomiting_many', 'lethargy', 'sleep_difficulty', 'irritable',
        'seizure_history', 'antipyretic_no_response', 'ataxia',
        'nystagmus_strabismus', 'limb_weakness', 'cranial_nerve_palsy',
        'hypertonia', 'avpu_P', 'resp_distress', 'mottled_sweat_cold',
        'apnea_irregular_breath', 'cyanosis', 'pulmonary_edema',
        'shock_pulse_absent'
    ];
    
    booleanFields.forEach(field => {
        const checkbox = document.getElementById(field);
        if (checkbox?.checked) {
            data[field] = true;
        }
    });
    
    return data;
}

// Hiển thị loading
function showLoading() {
    const container = document.getElementById('result-container');
    container.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <p style="margin-top: 20px; color: #667eea; font-weight: 600;">
                Đang phân tích dữ liệu...
            </p>
        </div>
    `;
}

// Hiển thị kết quả
function displayResult(result) {
    const container = document.getElementById('result-container');
    
    if (!result.success) {
        container.innerHTML = `
            <div class="error-message">
                <h3>❌ Không thể chẩn đoán</h3>
                <p>${result.message || result.error || 'Lỗi không xác định'}</p>
            </div>
        `;
        return;
    }
    
    const degreeMap = {
        '1': 'Độ 1 - Bệnh không biến chứng',
        '2a': 'Độ 2a - Có nguy cơ biến chứng thần kinh',
        '2b1': 'Độ 2b1 - Biến chứng thần kinh không nặng',
        '2b2': 'Độ 2b2 - Biến chứng thần kinh nặng',
        '3': 'Độ 3 - Biến chứng tim mạch giai đoạn sớm',
        '4': 'Độ 4 - Biến chứng tim mạch giai đoạn muộn'
    };
    
    const referenceMap = {
        '1': { section: '6.1', page: '9' },
        '2a': { section: '6.2.1', page: '9' },
        '2b1': { section: '6.2.2', page: '10' },
        '2b2': { section: '6.2.2', page: '10' },
        '3': { section: '6.3', page: '10' },
        '4': { section: '6.4', page: '10 và 11' }
    };
    
    const disease_level = result.disease_level || 'Không xác định';
    const degree_name = degreeMap[disease_level] || disease_level;
    const reference = referenceMap[disease_level];
    
    // Xác định class cho degree
    const degreeClass = `degree-${disease_level}`.replace('.', '');
    
    let html = `
        <div class="result-box">
            <div class="success-message">
                <h3>✅ Chẩn đoán thành công</h3>
            </div>
            
            <div style="text-align: center; margin: 20px 0;">
                <div class="degree-badge ${degreeClass}" style="display: inline-block; padding: 15px 30px; border-radius: 10px; font-size: 1.5em; font-weight: bold; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                    ${degree_name}
                </div>
            </div>
    `;
    
    // Hiển thị tài liệu tham khảo
    if (reference) {
        html += `
            <div class="info-section" style="background: #e8f4f8; border-left: 4px solid #2196f3; padding: 15px; margin: 15px 0; border-radius: 8px;">
                <h3 style="margin-top: 0; color: #1976d2;">📚 Tài liệu tham khảo</h3>
                <p style="margin: 0; line-height: 1.8;">
                    <strong>Mục ${reference.section}</strong> - Trang <strong>${reference.page}</strong>
                    <br>
                    <em style="color: #555; font-size: 0.95em;">
                        Quyết định về ban hành Hướng dẫn chẩn đoán, điều trị Tay chân miệng<br>
                        do Bộ Y Tế ban hành ngày 06/02/2024
                    </em>
                </p>
            </div>
        `;
    }
    
    // Hiển thị các luật đã khớp
    if (result.matched_rules && result.matched_rules.length > 0) {
        html += `
            <div class="info-section">
                <h3>📋 Các luật đã áp dụng (${result.matched_rules.length})</h3>
        `;
        
        result.matched_rules.forEach((rule, index) => {
            html += `
                <div class="inference-step" style="margin: 10px 0; padding: 10px; background: #f5f5f5; border-radius: 8px; border-left: 4px solid #667eea;">
                    <strong>Luật ${index + 1}:</strong> ${rule.name || rule.id}
                    <br>
                    <small style="color: #666;">Priority: ${rule.priority}</small>
                </div>
            `;
        });
        
        html += `</div>`;
    }
    
    html += `</div>`;
    
    container.innerHTML = html;
}

// Format derived facts
function formatDerivedFacts(facts) {
    if (!facts) return '';
    return Object.entries(facts)
        .map(([k, v]) => `<code>${k}=${v}</code>`)
        .join(', ');
}

// Toggle trace details
function toggleTrace() {
    const details = document.getElementById('trace-details');
    const toggle = document.getElementById('trace-toggle');
    
    if (details.style.display === 'none') {
        details.style.display = 'block';
        toggle.textContent = '▲';
    } else {
        details.style.display = 'none';
        toggle.textContent = '▼';
    }
}

// Hiển thị lỗi
function showError(message) {
    const container = document.getElementById('result-container');
    container.innerHTML = `
        <div class="error-message">
            <h3>❌ Lỗi</h3>
            <p>${message}</p>
        </div>
    `;
}

// Xóa form
function clearForm() {
    // Clear age inputs
    const ageInputs = ['age_years', 'age_months_input'];
    ageInputs.forEach(field => {
        const input = document.getElementById(field);
        if (input) input.value = '';
    });
    
    // Clear number inputs
    const numberFields = [
        'fever_temp_c', 'fever_days', 'startle_per_30min',
        'hr_no_fever', 'gcs', 'sbp', 'spo2', 'pulse_pressure'
    ];
    
    numberFields.forEach(field => {
        const input = document.getElementById(field);
        if (input) input.value = '';
    });
    
    // Clear checkboxes
    const booleanFields = [
        'rash_hand_foot_mouth', 'mouth_ulcer', 'startle_observed',
        'vomiting_many', 'lethargy', 'sleep_difficulty', 'irritable',
        'seizure_history', 'antipyretic_no_response', 'ataxia',
        'nystagmus_strabismus', 'limb_weakness', 'cranial_nerve_palsy',
        'hypertonia', 'avpu_P', 'resp_distress', 'mottled_sweat_cold',
        'apnea_irregular_breath', 'cyanosis', 'pulmonary_edema',
        'shock_pulse_absent'
    ];
    
    booleanFields.forEach(field => {
        const checkbox = document.getElementById(field);
        if (checkbox) checkbox.checked = false;
    });
    
    // Clear result
    const container = document.getElementById('result-container');
    container.innerHTML = `
        <div class="empty-state">
            <p>Nhập thông tin bệnh nhân và nhấn "Chẩn Đoán" để xem kết quả</p>
        </div>
    `;
}

// Load ví dụ
function loadExample() {
    // Example: Độ 2b1 - Giật mình
    document.getElementById('age_years').value = 2;
    document.getElementById('age_months_input').value = 0;
    document.getElementById('rash_hand_foot_mouth').checked = true;
    document.getElementById('mouth_ulcer').checked = true;
    document.getElementById('startle_observed').checked = true;
    document.getElementById('startle_per_30min').value = 2;
    
    // Auto diagnose
    setTimeout(() => diagnose(), 300);
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Enter key submit
document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            diagnose();
        }
    });
});
