// TCM Diagnosis System - 2 Phase JavaScript
const API_DIAGNOSIS = '/api/diagnose';
const API_CLASSIFY = '/api/classify';
const API_QUESTIONS = '/api/diagnosis-questions';

let diagnosisQuestions = null;
let hasFMD = false;

// Example Test Cases for Clinical Diagnosis (Phase 1 only)
const DIAGNOSIS_EXAMPLES = [
    {
        name: "CÓ TCM - Loét miệng + Phát ban tay chân",
        diagnosis: {
            fever_status: "no_fever",
            contact_patient: false,
            mouth_ulcer: true,
            rash_hand_foot_mouth: true,
            rash_buttocks: false,
            lab_pcr_positive: false
        }
    },
    {
        name: "CÓ TCM - Chỉ có phát ban tay chân miệng",
        diagnosis: {
            fever_status: "low_fever",
            contact_patient: true,
            mouth_ulcer: false,
            rash_hand_foot_mouth: true,
            rash_buttocks: false,
            lab_pcr_positive: false
        }
    },
    {
        name: "CÓ TCM - Chỉ có loét miệng",
        diagnosis: {
            fever_status: "no_fever",
            contact_patient: false,
            mouth_ulcer: true,
            rash_hand_foot_mouth: false,
            rash_buttocks: false,
            lab_pcr_positive: false
        }
    },
    {
        name: "CÓ TCM - Sốt + Tiếp xúc bệnh nhân + Loét miệng",
        diagnosis: {
            fever_status: "fever_2_days",
            contact_patient: true,
            mouth_ulcer: true,
            rash_hand_foot_mouth: false,
            rash_buttocks: false,
            lab_pcr_positive: false
        }
    },
    {
        name: "CÓ TCM - Triệu chứng đầy đủ + PCR dương tính",
        diagnosis: {
            fever_status: "high_fever",
            contact_patient: true,
            mouth_ulcer: true,
            rash_hand_foot_mouth: true,
            rash_buttocks: true,
            lab_pcr_positive: true
        }
    },
    {
        name: "CÓ TCM - Phát ban + mông + PCR dương tính",
        diagnosis: {
            fever_status: "low_fever",
            contact_patient: false,
            mouth_ulcer: false,
            rash_hand_foot_mouth: true,
            rash_buttocks: true,
            lab_pcr_positive: true
        }
    },
    {
        name: "KHÔNG TCM - Chỉ sốt, không có triệu chứng khác",
        diagnosis: {
            fever_status: "high_fever",
            contact_patient: false,
            mouth_ulcer: false,
            rash_hand_foot_mouth: false,
            rash_buttocks: false,
            lab_pcr_positive: false
        }
    },
    {
        name: "KHÔNG TCM - Chỉ tiếp xúc bệnh nhân nhưng không có triệu chứng",
        diagnosis: {
            fever_status: "no_fever",
            contact_patient: true,
            mouth_ulcer: false,
            rash_hand_foot_mouth: false,
            rash_buttocks: false,
            lab_pcr_positive: false
        }
    },
    {
        name: "KHÔNG TCM - Chỉ phát ban mông (không có tay chân)",
        diagnosis: {
            fever_status: "low_fever",
            contact_patient: false,
            mouth_ulcer: false,
            rash_hand_foot_mouth: false,
            rash_buttocks: true,
            lab_pcr_positive: false
        }
    },
    {
        name: "KHÔNG TCM - Sốt + Tiếp xúc nhưng PCR âm tính",
        diagnosis: {
            fever_status: "fever_2_days",
            contact_patient: true,
            mouth_ulcer: false,
            rash_hand_foot_mouth: false,
            rash_buttocks: false,
            lab_pcr_positive: false
        }
    }
];

// Load questions on page load
window.addEventListener('DOMContentLoaded', async () => {
    const container = document.getElementById('diagnosis-questions');
    if (container) {
        container.innerHTML = '<p style="color: #667eea; padding: 20px;">⏳ Đang tải câu hỏi...</p>';
    }
    await loadDiagnosisQuestions();
});

// Fetch diagnosis questions from API
async function loadDiagnosisQuestions() {
    try {
        const response = await fetch(API_QUESTIONS);
        const result = await response.json();
        
        if (result.success) {
            diagnosisQuestions = result.questions;
            renderDiagnosisQuestions();
        } else {
            alert('Không thể tải câu hỏi: ' + (result.error || 'Lỗi không xác định'));
        }
    } catch (error) {
        alert('Lỗi kết nối: ' + error.message);
    }
}

// Render all diagnosis question groups
function renderDiagnosisQuestions() {
    const container = document.getElementById('diagnosis-questions');
    if (!diagnosisQuestions) {
        container.innerHTML = '<p style="color: red;">Không có câu hỏi nào.</p>';
        return;
    }
    
    let html = '';
    
    // Basic Info
    if (diagnosisQuestions.basic_info && diagnosisQuestions.basic_info.length > 0) {
        html += '<div class="question-group basic-info-group">';
        html += '<h4>Thông tin cơ bản</h4>';
        diagnosisQuestions.basic_info.forEach(q => {
            html += createQuestionHTML(q);
        });
        html += '</div>';
    }
    
    // Symptoms Stage 1
    if (diagnosisQuestions.symptoms_stage_1 && diagnosisQuestions.symptoms_stage_1.questions) {
        html += '<div class="question-group">';
        html += '<h4>' + "Trong 1-2 ngày gần đây:" + '</h4>';
        diagnosisQuestions.symptoms_stage_1.questions.forEach(q => {
            html += createQuestionHTML(q);
        });
        html += '</div>';
    }
    
    // Symptoms Stage 2
    if (diagnosisQuestions.symptoms_stage_2 && diagnosisQuestions.symptoms_stage_2.questions) {
        html += '<div class="question-group">';
        html += '<h4>' + "Trong 3-10 ngày: " + '</h4>';
        diagnosisQuestions.symptoms_stage_2.questions.forEach(q => {
            html += createQuestionHTML(q);
        });
        html += '</div>';
    }
    
    // Warning Signs
    if (diagnosisQuestions.warning_signs && diagnosisQuestions.warning_signs.questions) {
        html += '<div class="question-group">';
        html += '<h4>' + "Các biến chứng nguy hiểm:" + '</h4>';
        diagnosisQuestions.warning_signs.questions.forEach(q => {
            html += createQuestionHTML(q);
        });
        html += '</div>';
    }
    
    // Epidemiology
    if (diagnosisQuestions.epidemiology && diagnosisQuestions.epidemiology.questions) {
        html += '<div class="question-group">';
        html += '<h4>' + diagnosisQuestions.epidemiology.title + '</h4>';
        diagnosisQuestions.epidemiology.questions.forEach(q => {
            html += createQuestionHTML(q);
        });
        html += '</div>';
    }
    
    // Lab Tests
    if (diagnosisQuestions.lab_tests && diagnosisQuestions.lab_tests.questions) {
        html += '<div class="question-group">';
        html += '<h4>' + diagnosisQuestions.lab_tests.title + '</h4>';
        diagnosisQuestions.lab_tests.questions.forEach(q => {
            html += createQuestionHTML(q);
        });
        html += '</div>';
    }
    
    container.innerHTML = html;
}

// Create HTML for a single question
function createQuestionHTML(q) {
    const id = q.id;
    
    if (q.type === 'yes_no') {
        return `
            <div class="question-item question-yesno">
                <span class="question-text">${q.question}</span>
                <div class="radio-group">
                    <label class="radio-option">
                        <input type="radio" id="${id}_yes" name="${id}" value="yes">
                        <span>Có</span>
                    </label>
                    <label class="radio-option">
                        <input type="radio" id="${id}_no" name="${id}" value="no" checked>
                        <span>Không</span>
                    </label>
                </div>
            </div>
        `;
    } else if (q.type === 'select') {
        let optionsHTML = '';
        if (q.options && q.options.length > 0) {
            q.options.forEach((opt, index) => {
                const checked = index === 0 ? 'checked' : '';
                optionsHTML += `
                    <label class="radio-option">
                        <input type="radio" id="${id}_${opt.value}" name="${id}" value="${opt.value}" ${checked}>
                        <span>${opt.label}</span>
                    </label>
                `;
            });
        }
        return `
            <div class="question-item question-select">
                <span class="question-text">${q.question}</span>
                <div class="radio-group radio-vertical">
                    ${optionsHTML}
                </div>
            </div>
        `;
    } else if (q.type === 'number') {
        const min = q.validation?.min || 0;
        const max = q.validation?.max || 1000;
        return `
            <div class="question-item question-number">
                <label class="question-text" for="${id}">${q.question}</label>
                <input type="number" id="${id}" name="${id}" 
                       min="${min}" max="${max}" 
                       placeholder="Nhập giá trị..." 
                       class="number-input">
            </div>
        `;
    }
    
    return '';
}

// Run Phase 1: Clinical Diagnosis
async function runDiagnosis() {
    const answers = {};
    
    // Collect radio button answers (yes/no and select types)
    document.querySelectorAll('#diagnosis-questions input[type="radio"]:checked').forEach(radio => {
        const value = radio.value;
        // For yes/no questions, convert to boolean
        if (value === 'yes') {
            answers[radio.name] = true;
        } else if (value === 'no') {
            answers[radio.name] = false;
        } else {
            // For select questions, keep the string value
            answers[radio.name] = value;
        }
    });
    
    // Collect number inputs
    document.querySelectorAll('#diagnosis-questions input[type="number"]').forEach(input => {
        if (input.value) {
            const key = input.name || input.id;
            answers[key] = parseFloat(input.value);
        }
    });
    
    // Debug: Log answers being sent
    console.log('Sending diagnosis data:', JSON.stringify(answers, null, 2));
    
    showLoading('diagnosis-result-container', 'Đang phân tích...');
    
    try {
        const response = await fetch(API_DIAGNOSIS, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(answers)
        });
        
        const result = await response.json();
        console.log('Diagnosis result:', JSON.stringify(result, null, 2));
        displayDiagnosisResult(result);
        
    } catch (error) {
        alert('Lỗi khi chẩn đoán: ' + error.message);
    }
}

// Display Phase 1 result
function displayDiagnosisResult(result) {
    const container = document.getElementById('diagnosis-result-container');
    
    if (!result.success) {
        container.innerHTML = `
            <div class="diagnosis-result diagnosis-negative">
                ${result.error || 'Không thể chẩn đoán'}
            </div>
        `;
        return;
    }
    
    const conclusions = result.conclusions || {};
    hasFMD = (conclusions.has_hfmd === true);
    
    if (hasFMD) {
        container.innerHTML = `
            <div class="diagnosis-result diagnosis-positive">
                <h3 style="margin: 0 0 15px 0;">CHẨN ĐOÁN: Bệnh nhân CÓ TCM</h3>
                <p style="margin: 5px 0;"><strong>Loại:</strong> ${conclusions.diagnosis_type || 'Không xác định'}</p>
                <p style="margin: 5px 0;"><strong>Tin cậy:</strong> ${conclusions.confidence || 'N/A'}</p>
                <p style="margin: 10px 0; color: #2d3748;">${conclusions.message || ''}</p>
                <div style="margin-top: 20px;">
                    <button class="btn-primary" onclick="goToClassification()" style="font-size: 16px; padding: 12px 30px;">
                        Tiếp Tục Phân Độ Bệnh
                    </button>
                </div>
            </div>
        `;
    } else {
        container.innerHTML = `
            <div class="diagnosis-result diagnosis-negative">
                <h3 style="margin: 0 0 10px 0;">CHẨN ĐOÁN: Bệnh nhân KHÔNG có TCM</h3>
            </div>
        `;
    }
}

// Run Phase 2: Severity Classification
async function runClassification() {
    if (!hasFMD) {
        alert('Chỉ phân độ khi bệnh nhân có HFMD');
        return;
    }
    
    const data = {
        has_hfmd: true
    };
    
    // Collect numeric fields
    const numericFields = [
        'age_months', 'fever_temp_c', 'fever_days', 
        'startle_per_30min', 'hr_no_fever', 'gcs', 
        'sbp', 'spo2', 'pulse_pressure'
    ];
    
    numericFields.forEach(field => {
        const value = document.getElementById(field)?.value;
        if (value) {
            data[field] = parseFloat(value);
        }
    });
    
    // Collect boolean checkboxes
    const booleanFields = [
        'mouth_ulcer', 'rash_hand_foot_mouth',
        'antipyretic_no_response', 'startle_observed', 'vomiting_many',
        'lethargy', 'sleep_difficulty', 'irritable', 'seizure_history',
        'ataxia', 'nystagmus_strabismus', 'limb_weakness', 
        'cranial_nerve_palsy', 'hypertonia', 'avpu_P',
        'resp_distress', 'mottled_sweat_cold', 'apnea_irregular_breath',
        'cyanosis', 'pulmonary_edema', 'shock_pulse_absent'
    ];
    
    booleanFields.forEach(field => {
        if (document.getElementById(field)?.checked) {
            data[field] = true;
        }
    });
    
    showLoading('classification-result-container', 'Đang phân độ...');
    
    try {
        const response = await fetch(API_CLASSIFY, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        displayClassificationResult(result);
        
    } catch (error) {
        alert('Lỗi khi phân độ: ' + error.message);
    }
}

// Display Phase 2 result
function displayClassificationResult(result) {
    const container = document.getElementById('classification-result-container');
    
    if (!result.success) {
        container.innerHTML = `
            <div class="diagnosis-result diagnosis-negative">
                ${result.error || 'Không thể phân độ'}
            </div>
        `;
        return;
    }
    
    const level = result.conclusions?.disease_level || 'Không xác định';
    const description = result.conclusions?.description || '';
    
    const levelNames = {
        '1': 'Bệnh không biến chứng',
        '2a': 'Có nguy cơ biến chứng thần kinh',
        '2b': 'Biến chứng thần kinh',
        '3': 'Biến chứng tim mạch giai đoạn sớm',
        '4': 'Biến chứng tim mạch giai đoạn muộn'
    };
    
    // Mapping nguồn tham chiếu
    const references = {
        '1': 'mục 6.1 phần I trang 9',
        '2a': 'mục 6.2 phần I trang 9',
        '2b': 'mục 6.2 phần I trang 10',
        '3': 'mục 6.3 phần I trang 10',
        '4': 'mục 6.4 phần I trang 10-11'
    };
    
    const levelName = levelNames[level] || level;
    const reference = references[level] || 'không xác định';
    
    // Tạo HTML cho TRACE (quá trình chẩn đoán tuần tự)
    let traceHTML = '';
    if (result.trace && result.trace.length > 0) {
        traceHTML = '<div style="margin: 20px 0; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 12px; text-align: left;">';
        traceHTML += '<h3 style="margin: 0 0 15px 0; color: white; font-size: 20px;">Quá trình chẩn đoán tuần tự</h3>';
        
        result.trace.forEach((step, index) => {
            if (step.type === 'input') {
                // Hiển thị triệu chứng đã nhập
                traceHTML += '<div style="margin: 15px 0; padding: 15px; background: rgba(52, 199, 89, 0.2); border-left: 4px solid #34c759; border-radius: 8px;">';
                traceHTML += '<h4 style="margin: 0 0 10px 0; color: #34c759; font-size: 16px;">' + step.message + '</h4>';
                traceHTML += '<ul style="margin: 5px 0; padding-left: 25px; color: white;">';
                
                step.symptoms.forEach(symptom => {
                    const fieldLabel = getFieldLabel(symptom.field);
                    const valueLabel = formatValue(symptom.value);
                    traceHTML += `<li style="margin: 5px 0;">${fieldLabel}: <strong>${valueLabel}</strong></li>`;
                });
                
                traceHTML += '</ul></div>';
                
            } else if (step.type === 'check') {
                // Hiển thị kết quả kiểm tra từng độ
                if (step.matched) {
                    traceHTML += `<div style="margin: 15px 0; padding: 15px; background: rgba(52, 199, 89, 0.3); border-left: 4px solid #34c759; border-radius: 8px;">`;
                    traceHTML += `<h4 style="margin: 0 0 10px 0; color: #34c759; font-size: 16px;">Kiểm tra ${step.degree_name}</h4>`;
                    traceHTML += '<p style="margin: 5px 0; color: white; font-weight: 600;">→ Tìm thấy triệu chứng khớp:</p>';
                    traceHTML += '<ul style="margin: 5px 0; padding-left: 25px; color: white;">';
                    
                    step.symptoms.forEach(symptom => {
                        const symptomName = symptom.name.replace(/^Độ \d+[ab]? - /, '');
                        traceHTML += `<li style="margin: 5px 0;">${symptomName}</li>`;
                    });
                    
                    traceHTML += '</ul></div>';
                } else {
                    traceHTML += `<div style="margin: 15px 0; padding: 15px; background: rgba(255, 255, 255, 0.05); border-left: 4px solid rgba(255,255,255,0.3); border-radius: 8px;">`;
                    traceHTML += `<h4 style="margin: 0; color: rgba(255,255,255,0.6); font-size: 16px;">⊘ Kiểm tra ${step.degree_name}</h4>`;
                    traceHTML += '<p style="margin: 5px 0 0 0; color: rgba(255,255,255,0.5);">→ Không có triệu chứng khớp, tiếp tục kiểm tra độ thấp hơn...</p>';
                    traceHTML += '</div>';
                }
                
            } else if (step.type === 'conclusion') {
                // Hiển thị kết luận
                traceHTML += '<div style="margin: 20px 0; padding: 20px; background: linear-gradient(135deg, rgba(52, 199, 89, 0.3) 0%, rgba(48, 209, 88, 0.2) 100%); border: 2px solid #34c759; border-radius: 12px;">';
                traceHTML += `<h3 style="margin: 0 0 15px 0; color: #34c759; font-size: 22px;">KẾT LUẬN: ${step.degree_name}</h3>`;
                traceHTML += `<p style="margin: 10px 0; color: white; font-size: 16px; font-weight: 600;">${step.description}</p>`;
                
                if (step.matched_symptoms && step.matched_symptoms.length > 0) {
                    traceHTML += '<div style="margin: 15px 0;">';
                    traceHTML += '<h4 style="margin: 0 0 10px 0; color: white; font-size: 15px;">Triệu chứng phù hợp:</h4>';
                    traceHTML += '<ul style="margin: 5px 0; padding-left: 25px; color: white;">';
                    
                    step.matched_symptoms.forEach(symptom => {
                        const symptomName = symptom.name.replace(/^Độ \d+[ab]? - /, '');
                        traceHTML += `<li style="margin: 5px 0;">${symptomName}</li>`;
                    });
                    
                    traceHTML += '</ul></div>';
                }
                
                if (step.source) {
                    traceHTML += `<div style="margin-top: 15px; padding: 12px; background: rgba(255,255,255,0.15); border-radius: 6px; font-size: 13px; font-style: italic; color: white;">`;
                    traceHTML += `<strong>Nguồn:</strong> ${step.source}`;
                    traceHTML += '</div>';
                } else if (step.degree && references[step.degree]) {
                    // Nếu không có source từ backend, dùng mapping
                    traceHTML += `<div style="margin-top: 15px; padding: 12px; background: rgba(255,255,255,0.15); border-radius: 6px; font-size: 13px; font-style: italic; color: white;">`;
                    traceHTML += `<strong>Nguồn:</strong> Dựa ${references[step.degree]} của Quyết định về việc ban hành Hướng dẫn chẩn đoán, điều trị bệnh TCM`;
                    traceHTML += '</div>';
                }
                
                traceHTML += '</div>';
            }
        });
        
        traceHTML += '</div>';
    }
    
    // Kết quả ngắn gọn ở đầu (giữ nguyên style cũ)
    container.innerHTML = `
        <div class="classification-result">
            <h3 style="margin: 0 0 10px 0;">ĐỘ ${level}</h3>
            <p style="font-size: 18px; margin: 10px 0; font-weight: 600;">${levelName}</p>
            <p style="font-size: 15px; margin: 10px 0; opacity: 0.95;">${description}</p>
            
            <!-- Nút gợi ý điều trị -->
            <button onclick="showTreatmentRecommendation('${level}')" class="btn-primary" style="margin-top: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); font-size: 16px; padding: 12px 30px;">
                Gợi Ý Điều Trị
            </button>
        </div>
        ${traceHTML}
    `;
}

// Helper: Lấy label cho field
function getFieldLabel(field) {
    const labels = {
        // Thông tin cơ bản
        'age_months': 'Tuổi (tháng)',
        'has_hfmd': 'Có TCM',
        
        // Triệu chứng sốt
        'fever_temp_c': 'Nhiệt độ sốt (°C)',
        'fever_days': 'Số ngày sốt',
        'temp_c': 'Nhiệt độ (°C)',
        'antipyretic_no_response': 'Hạ sốt không đáp ứng',
        
        // Triệu chứng thần kinh
        'startle_per_30min': 'Giật mình/30 phút',
        'startle_observed': 'Giật mình (quan sát)',
        'gcs': 'GCS',
        'vomiting_many': 'Nôn nhiều',
        'vomit_per_hour': 'Nôn (lần/giờ)',
        'lethargy': 'Ngủ nhiều',
        'sleep_difficulty': 'Khó ngủ',
        'irritable': 'Quấy khóc',
        'seizure_history': 'Co giật',
        'seizure': 'Co giật',
        'ataxia': 'Loạng choạng',
        'nystagmus_strabismus': 'Rung giật nhãn cầu/Lác mắt',
        'nystagmus': 'Rung giật nhãn cầu',
        'limb_weakness': 'Yếu chi',
        'cranial_nerve_palsy': 'Liệt thần kinh sọ',
        'hypertonia': 'Tăng trương lực cơ',
        'avpu_P': 'AVPU = P',
        'avpu_level': 'AVPU',
        'somnolent': 'Li bì',
        'tremor': 'Run',
        'coma': 'Hôn mê',
        
        // Triệu chứng tim mạch & hô hấp
        'hr_no_fever': 'Nhịp tim không sốt (bpm)',
        'heart_rate': 'Nhịp tim (bpm)',
        'sbp': 'Huyết áp tâm thu (mmHg)',
        'dbp': 'Huyết áp tâm trương (mmHg)',
        'spo2': 'SpO₂ (%)',
        'pulse_pressure': 'Hiệu áp (mmHg)',
        'respiratory_rate': 'Nhịp thở',
        'resp_distress': 'Khó thở',
        'mottled_sweat_cold': 'Da nổi vân tím/Đổ mồ hôi lạnh',
        'mottled_skin': 'Da nổi vân tím',
        'apnea_irregular_breath': 'Ngừng thở/Thở không đều',
        'apnea': 'Ngừng thở',
        'resp_irregular_severe': 'Thở không đều nặng',
        'cyanosis': 'Tím tái toàn thân',
        'pulmonary_edema': 'Phù phổi cấp',
        'pulm_edema_pink_froth': 'Phù phổi - sùi bọt hồng',
        'lung_rales_wet': 'Ran ẩm phổi',
        'shock_pulse_absent': 'Shock/Mạch không bắt được',
        'capillary_refill_time': 'CRT (giây)',
        'cold_extremities': 'Chi lạnh',
        'weak_pulse': 'Mạch yếu',
        'lactate': 'Lactate (mmol/L)',
        
        // Triệu chứng da/niêm mạc
        'mouth_ulcer': 'Loét miệng',
        'oral_ulcer': 'Loét miệng',
        'rash_hand_foot_mouth': 'Phát ban tay chân miệng',
        'rash_hf': 'Phát ban tay chân',
        'rash_typical_locations': 'Phát ban vị trí điển hình',
        
        // Xét nghiệm
        'wbc_count': 'Bạch cầu (G/L)',
        'blood_glucose': 'Đường huyết (mg%)',
        'platelet_count': 'Tiểu cầu (G/L)',
        'rt_pcr_result': 'RT-PCR',
        'lab_pcr_positive': 'PCR dương tính',
        
        // Dịch tễ
        'contact_patient': 'Tiếp xúc bệnh nhân TCM',
        'fever_status': 'Tình trạng sốt',
        'fatigue': 'Mệt mỏi',
        'sore_throat': 'Đau họng',
        'poor_appetite': 'Biếng ăn',
        'diarrhea': 'Tiêu chảy'
    };
    return labels[field] || field;
}

// Helper: Format giá trị
function formatValue(value) {
    if (typeof value === 'boolean') {
        return value ? 'Có' : 'Không';
    }
    return value;
}

// Show loading indicator
function showLoading(containerId, message) {
    const container = document.getElementById(containerId);
    container.innerHTML = `
        <div style="text-align: center; padding: 20px;">
            <div class="spinner" style="margin: 0 auto 10px auto;"></div>
            <p>${message}</p>
        </div>
    `;
}

// Navigate to classification phase
function goToClassification() {
    if (!hasFMD) {
        alert('Chỉ phân độ khi bệnh nhân có TCM');
        return;
    }
    
    // Hide phase 1, show phase 2
    document.getElementById('phase1').classList.add('phase-hidden');
    document.getElementById('phase2').classList.remove('phase-hidden');
    
    // Clear classification result
    document.getElementById('classification-result-container').innerHTML = '';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Go back to diagnosis phase
function goBackToDiagnosis() {
    // Show phase 1, hide phase 2
    document.getElementById('phase1').classList.remove('phase-hidden');
    document.getElementById('phase2').classList.add('phase-hidden');
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Load example WITH TCM - Fixed case
function loadExampleWithTCM() {
    // Reset all states
    hasFMD = false;
    document.getElementById('phase1').classList.remove('phase-hidden');
    document.getElementById('phase2').classList.add('phase-hidden');
    document.getElementById('diagnosis-result-container').innerHTML = '';
    document.getElementById('classification-result-container').innerHTML = '';
    
    // Fixed example: Có TCM - Loét miệng + Phát ban tay chân
    const example = {
        age_months: 36,
        fever_status: "mild_fever",
        contact_patient: true,
        mouth_ulcer: true,
        rash_hand_foot_mouth: true,
        rash_typical_locations: true,
        fatigue: false,
        sore_throat: false,
        poor_appetite: false,
        diarrhea: false,
        rt_pcr_result: false
    };
    
    // Fill Phase 1 fields
    Object.keys(example).forEach(field => {
        const value = example[field];
        
        if (typeof value === 'boolean') {
            const radioYes = document.getElementById(`${field}_yes`);
            const radioNo = document.getElementById(`${field}_no`);
            if (value) {
                if (radioYes) radioYes.checked = true;
            } else {
                if (radioNo) radioNo.checked = true;
            }
        } else if (typeof value === 'number') {
            const input = document.getElementById(field);
            if (input) {
                input.value = value;
            }
        } else {
            const radio = document.getElementById(`${field}_${value}`);
            if (radio) {
                radio.checked = true;
            }
        }
    });
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Load example WITHOUT TCM - Fixed case
function loadExampleWithoutTCM() {
    // Reset all states
    hasFMD = false;
    document.getElementById('phase1').classList.remove('phase-hidden');
    document.getElementById('phase2').classList.add('phase-hidden');
    document.getElementById('diagnosis-result-container').innerHTML = '';
    document.getElementById('classification-result-container').innerHTML = '';
    
    // Fixed example: Không TCM - Chỉ sốt, không có triệu chứng khác
    const example = {
        age_months: 48,
        fever_status: "high_fever",
        contact_patient: false,
        mouth_ulcer: false,
        rash_hand_foot_mouth: false,
        rash_typical_locations: false,
        fatigue: true,
        sore_throat: false,
        poor_appetite: true,
        diarrhea: false,
        rt_pcr_result: false
    };
    
    // Fill Phase 1 fields
    Object.keys(example).forEach(field => {
        const value = example[field];
        
        if (typeof value === 'boolean') {
            const radioYes = document.getElementById(`${field}_yes`);
            const radioNo = document.getElementById(`${field}_no`);
            if (value) {
                if (radioYes) radioYes.checked = true;
            } else {
                if (radioNo) radioNo.checked = true;
            }
        } else if (typeof value === 'number') {
            const input = document.getElementById(field);
            if (input) {
                input.value = value;
            }
        } else {
            const radio = document.getElementById(`${field}_${value}`);
            if (radio) {
                radio.checked = true;
            }
        }
    });
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Load classification examples for testing
function loadClassificationExample(grade) {
    let example = {};
    
    if (grade === 'grade1') {
        // Độ 1 - Không biến chứng
        example = {
            age_months: 36,
            fever_temp_c: 37.5,
            fever_days: 1,
            startle_per_30min: 0,
            gcs: 15
        };
    } else if (grade === 'grade2b') {
        // Độ 2b - Biến chứng thần kinh
        example = {
            age_months: 30,
            fever_temp_c: 39.5,
            fever_days: 3,
            antipyretic_no_response: true,
            startle_per_30min: 3,
            startle_observed: true,
            vomiting_many: true,
            hr_no_fever: 140,
            gcs: 13
        };
    } else if (grade === 'grade3') {
        // Độ 3 - Rối loạn thần kinh thực vật nặng
        example = {
            age_months: 24,
            fever_temp_c: 40,
            fever_days: 4,
            startle_per_30min: 5,
            startle_observed: true,
            hr_no_fever: 175,
            sbp: 120,
            spo2: 93,
            resp_distress: true,
            mottled_sweat_cold: true,
            gcs: 12
        };
    }
    
    // Clear all inputs first
    document.querySelectorAll('#phase2 input[type="number"]').forEach(input => {
        input.value = '';
    });
    document.querySelectorAll('#phase2 input[type="checkbox"]').forEach(checkbox => {
        checkbox.checked = false;
    });
    
    // Fill example data
    Object.keys(example).forEach(field => {
        const value = example[field];
        
        if (typeof value === 'boolean' && value === true) {
            const checkbox = document.getElementById(field);
            if (checkbox) checkbox.checked = true;
        } else if (typeof value === 'number') {
            const input = document.getElementById(field);
            if (input) input.value = value;
        }
    });
    
    // Clear result
    document.getElementById('classification-result-container').innerHTML = '';
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Treatment recommendation functions
async function showTreatmentRecommendation(diseaseLevel) {
    try {
        const response = await fetch('/api/treatment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                disease_level: diseaseLevel
            })
        });
        
        const result = await response.json();
        
        if (!result.success) {
            alert('Lỗi: ' + (result.error || 'Không thể lấy gợi ý điều trị'));
            return;
        }
        
        displayTreatment(result.treatment);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Lỗi khi lấy gợi ý điều trị: ' + error.message);
    }
}

function displayTreatment(treatment) {
    const modal = document.getElementById('treatmentModal');
    const content = document.getElementById('treatment-content');
    
    // Build HTML
    let html = `
        <div style="margin-bottom: 25px; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 12px;">
            <h2 style="margin: 0 0 10px 0; color: #FFD700; font-size: 26px; font-weight: 700;">
                ĐỘ ${treatment.disease_level}: ${treatment.disease_name}
            </h2>
            <p style="margin: 8px 0; font-size: 16px; color: rgba(255,255,255,0.9);">
                <strong>Nơi điều trị:</strong> ${treatment.treatment_location}
            </p>
            <p style="margin: 8px 0; font-size: 14px; color: rgba(255,255,255,0.7); font-style: italic;">
                <strong>Nguồn:</strong> ${treatment.reference}
            </p>
        </div>
    `;
    
    // Render treatments
    treatment.treatments.forEach((section, index) => {
        html += `
            <div style="margin-bottom: 20px; padding: 18px; background: rgba(255,255,255,0.05); border-left: 4px solid #FFD700; border-radius: 10px;">
                <h3 style="margin: 0 0 12px 0; color: #FFD700; font-size: 20px; font-weight: 600;">
                    ${index + 1}. ${section.category}
                </h3>
        `;
        
        // Medications (for "Liều lượng thuốc sử dụng" category)
        if (section.medications && section.medications.length > 0) {
            section.medications.forEach((med, medIndex) => {
                html += `<div style="margin: 12px 0; padding: 14px; background: rgba(255,255,255,0.08); border-left: 3px solid #00D4FF; border-radius: 8px;">`;
                html += `<h4 style="margin: 0 0 10px 0; color: #00D4FF; font-size: 17px; font-weight: 600;">${medIndex + 1}. ${med.name}</h4>`;
                
                // Indication
                if (med.indication) {
                    html += `<p style="margin: 6px 0; color: rgba(255,255,255,0.85);"><strong style="color: #FFD700;">Chỉ định:</strong> ${med.indication}</p>`;
                }
                
                // Dosage
                if (med.dosage) {
                    html += `<p style="margin: 6px 0; color: white;"><strong style="color: #34c759;">Liều lượng:</strong> ${med.dosage}</p>`;
                }
                
                // Options (for medications with multiple options like sedation)
                if (med.options && med.options.length > 0) {
                    html += '<p style="margin: 6px 0 4px 0; color: #FFD700; font-weight: 600;">Lựa chọn:</p>';
                    html += '<ul style="margin: 0; padding-left: 25px; color: white;">';
                    med.options.forEach(opt => {
                        html += `<li style="margin: 4px 0;">${opt}</li>`;
                    });
                    html += '</ul>';
                }
                
                // BP criteria
                if (med.bp_criteria && med.bp_criteria.length > 0) {
                    html += '<p style="margin: 8px 0 4px 0; color: #FFD700; font-weight: 600;">Tiêu chí huyết áp:</p>';
                    html += '<ul style="margin: 0; padding-left: 25px; color: white;">';
                    med.bp_criteria.forEach(bp => {
                        html += `<li style="margin: 4px 0;">${bp}</li>`;
                    });
                    html += '</ul>';
                }
                
                // Adjustment
                if (med.adjustment) {
                    html += `<p style="margin: 6px 0; color: rgba(255,255,255,0.85);"><strong style="color: #FFD700;">Điều chỉnh:</strong> ${med.adjustment}</p>`;
                }
                
                // Stop criteria
                if (med.stop_criteria && med.stop_criteria.length > 0) {
                    html += '<p style="margin: 8px 0 4px 0; color: #FF3B30; font-weight: 600;">🛑 Tiêu chí ngừng:</p>';
                    html += '<ul style="margin: 0; padding-left: 25px; color: white;">';
                    med.stop_criteria.forEach(sc => {
                        html += `<li style="margin: 4px 0;">${sc}</li>`;
                    });
                    html += '</ul>';
                }
                
                // Additional measures
                if (med.additional_measures && med.additional_measures.length > 0) {
                    html += '<p style="margin: 8px 0 4px 0; color: #FFD700; font-weight: 600;">Biện pháp bổ sung:</p>';
                    html += '<ul style="margin: 0; padding-left: 25px; color: white;">';
                    med.additional_measures.forEach(am => {
                        html += `<li style="margin: 4px 0;">${am}</li>`;
                    });
                    html += '</ul>';
                }
                
                // Note
                if (med.note) {
                    html += `<p style="margin: 8px 0 0 0; padding: 8px; background: rgba(255,204,0,0.15); border-radius: 4px; color: white; font-size: 14px; font-style: italic;"><strong>⚠️ Lưu ý:</strong> ${med.note}</p>`;
                }
                
                html += '</div>';
            });
        }
        
        // Interventions (for non-medication categories)
        if (section.interventions && section.interventions.length > 0) {
            html += '<ul style="margin: 8px 0; padding-left: 25px; color: white; line-height: 1.8;">';
            section.interventions.forEach(intervention => {
                html += `<li style="margin: 6px 0;">${intervention}</li>`;
            });
            html += '</ul>';
        }
        
        // Vital signs frequent monitoring (for "Theo dõi" category)
        if (section.vital_signs_frequent) {
            html += '<div style="margin: 12px 0; padding: 14px; background: rgba(52, 199, 89, 0.15); border-left: 3px solid #34c759; border-radius: 8px;">';
            html += '<h4 style="margin: 0 0 10px 0; color: #34c759; font-size: 16px; font-weight: 600;">Theo dõi sinh hiệu thường xuyên</h4>';
            
            if (section.vital_signs_frequent.parameters && section.vital_signs_frequent.parameters.length > 0) {
                html += '<p style="margin: 6px 0; color: white;"><strong>Các chỉ số:</strong></p>';
                html += '<ul style="margin: 4px 0; padding-left: 25px; color: white;">';
                section.vital_signs_frequent.parameters.forEach(param => {
                    html += `<li style="margin: 4px 0;">${param}</li>`;
                });
                html += '</ul>';
            }
            
            if (section.vital_signs_frequent.frequency) {
                html += `<p style="margin: 8px 0 0 0; color: rgba(255,255,255,0.9); font-style: italic;"><strong>Tần suất:</strong> ${section.vital_signs_frequent.frequency}</p>`;
            }
            
            html += '</div>';
        }
        
        // Invasive monitoring (for "Theo dõi" category)
        if (section.invasive_monitoring) {
            html += '<div style="margin: 12px 0; padding: 14px; background: rgba(255, 149, 0, 0.15); border-left: 3px solid #FF9500; border-radius: 8px;">';
            html += '<h4 style="margin: 0 0 10px 0; color: #FF9500; font-size: 16px; font-weight: 600;">Theo dõi xâm lấn</h4>';
            
            if (section.invasive_monitoring.parameters && section.invasive_monitoring.parameters.length > 0) {
                html += '<p style="margin: 6px 0; color: white;"><strong>Các chỉ số:</strong></p>';
                html += '<ul style="margin: 4px 0; padding-left: 25px; color: white;">';
                section.invasive_monitoring.parameters.forEach(param => {
                    html += `<li style="margin: 4px 0;">${param}</li>`;
                });
                html += '</ul>';
            }
            
            if (section.invasive_monitoring.frequency) {
                html += `<p style="margin: 8px 0 0 0; color: rgba(255,255,255,0.9); font-style: italic;"><strong>Tần suất:</strong> ${section.invasive_monitoring.frequency}</p>`;
            }
            
            html += '</div>';
        }
        
        // Criteria
        if (section.criteria) {
            if (Array.isArray(section.criteria)) {
                html += '<div style="margin: 10px 0; padding: 12px; background: rgba(255,255,255,0.08); border-radius: 6px;">';
                html += '<p style="margin: 0 0 8px 0; color: #FFD700; font-weight: 600;">Tiêu chí:</p>';
                html += '<ul style="margin: 0; padding-left: 25px; color: white;">';
                section.criteria.forEach(c => {
                    html += `<li style="margin: 5px 0;">${c}</li>`;
                });
                html += '</ul>';
                
                // Indications for degree 3 (hiển thị ngay sau criteria)
                if (section.indications_degree_3 && section.indications_degree_3.length > 0) {
                    html += '<ul style="margin: 5px 0 0 40px; padding-left: 25px; color: rgba(255,255,255,0.9); list-style-type: circle;">';
                    section.indications_degree_3.forEach(ind => {
                        html += `<li style="margin: 5px 0;">${ind}</li>`;
                    });
                    html += '</ul>';
                }
                
                html += '</div>';
            } else {
                html += `<p style="margin: 8px 0; padding: 10px; background: rgba(255,255,255,0.08); border-radius: 6px; color: white;"><strong>Tiêu chí:</strong> ${section.criteria}</p>`;
            }
        }
        
        // Warning signs
        if (section.warning_signs && section.warning_signs.length > 0) {
            html += '<div style="margin: 10px 0; padding: 12px; background: rgba(255, 59, 48, 0.15); border: 1px solid rgba(255, 59, 48, 0.3); border-radius: 6px;">';
            html += '<p style="margin: 0 0 8px 0; color: #FF3B30; font-weight: 600;">⚠️ Dấu hiệu cảnh báo:</p>';
            html += '<ul style="margin: 0; padding-left: 25px; color: white;">';
            section.warning_signs.forEach(sign => {
                html += `<li style="margin: 5px 0;">${sign}</li>`;
            });
            html += '</ul></div>';
        }
        
        // Risk factors
        if (section.risk_factors && section.risk_factors.length > 0) {
            html += '<div style="margin: 10px 0; padding: 12px; background: rgba(255,149,0,0.15); border: 1px solid rgba(255,149,0,0.3); border-radius: 6px;">';
            html += '<p style="margin: 0 0 8px 0; color: #FF9500; font-weight: 600;">⚠️ Yếu tố nguy cơ:</p>';
            html += '<ul style="margin: 0; padding-left: 25px; color: white;">';
            section.risk_factors.forEach(factor => {
                html += `<li style="margin: 5px 0;">${factor}</li>`;
            });
            html += '</ul></div>';
        }
        
        // Indication (category level)
        if (section.indication) {
            html += `<p style="margin: 8px 0; padding: 10px; background: rgba(52, 199, 89, 0.15); border-radius: 6px; color: white;"><strong>Chỉ định:</strong> ${section.indication}</p>`;
        }
        
        // BP criteria (category level - old structure)
        if (section.bp_criteria && section.bp_criteria.length > 0) {
            html += '<div style="margin: 10px 0; padding: 12px; background: rgba(255,255,255,0.08); border-radius: 6px;">';
            html += '<p style="margin: 0 0 8px 0; color: #FFD700; font-weight: 600;">Tiêu chí huyết áp:</p>';
            html += '<ul style="margin: 0; padding-left: 25px; color: white;">';
            section.bp_criteria.forEach(c => {
                html += `<li style="margin: 5px 0;">${c}</li>`;
            });
            html += '</ul></div>';
        }
        
        // Stop criteria (category level - old structure)
        if (section.stop_criteria && section.stop_criteria.length > 0) {
            html += '<div style="margin: 10px 0; padding: 12px; background: rgba(255, 59, 48, 0.15); border-radius: 6px;">';
            html += '<p style="margin: 0 0 8px 0; color: #FF3B30; font-weight: 600;">🛑 Tiêu chí ngừng:</p>';
            html += '<ul style="margin: 0; padding-left: 25px; color: white;">';
            section.stop_criteria.forEach(c => {
                html += `<li style="margin: 5px 0;">${c}</li>`;
            });
            html += '</ul></div>';
        }
        
        // Indications for degree 3
        if (section.indications_degree_3 && section.indications_degree_3.length > 0 && !section.criteria) {
            // Chỉ hiển thị riêng nếu KHÔNG có criteria (tránh duplicate)
            html += '<div style="margin: 10px 0; padding: 12px; background: rgba(52, 199, 89, 0.15); border-radius: 6px;">';
            html += '<p style="margin: 0 0 8px 0; color: #34c759; font-weight: 600;">Chỉ định cho độ 3:</p>';
            html += '<ul style="margin: 0; padding-left: 25px; color: white;">';
            section.indications_degree_3.forEach(ind => {
                html += `<li style="margin: 5px 0;">${ind}</li>`;
            });
            html += '</ul></div>';
        }
        
        html += '</div>';
    });
    
    content.innerHTML = html;
    modal.style.display = 'block';
}

function closeTreatmentModal() {
    const modal = document.getElementById('treatmentModal');
    modal.style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('treatmentModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Add CSS animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
