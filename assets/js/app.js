/**
 * DMN Decision UI Controller
 * Quản lý tương tác UI và kết nối với engine
 */

// Column headers (must match DMN sheet)
const COLS = [
  "RowID", "Kết quả (Degree)",
  "RashHF", "OralUlcer",
  "TempC", "FeverDays", "VomitPerHour",
  "StartleObserved", "StartleHist/30'", "Somnolent", "Nystagmus", "Ataxia", "LimbWeakness", "CranialNervePalsy", "Hypertonia", "Seizure", "GCS", "AVPU",
  "HR (không sốt)", "SBP_HighForAge", "SBP_mmHg", "AgeMonthsCond", "PulsePressure",
  "RR_HighForAge", "StridorInsp", "ShallowBreath", "AbdominalBreath", "ChestRetraction",
  "SpO₂", "CRTsec", "MottledSkin", "ColdExtOrSweat",
  "Apnea", "RespIrregularSevere", "PulmEdemaPinkFroth", "LungRalesWet", "PulseAbsent", "BPUnrecordable",
  "Ghi chú", "Nguồn"
];

// Starter rules (minimal example set)
const STARTER_RULES = [
  { 
    id: "4-01", 
    result: "4", 
    priority: 400, 
    when: { "SpO₂": "<92" }, 
    notes: "SpO₂ <92% ⇒ Độ 4", 
    source: "QĐ 292 – II.6 (Độ 4)" 
  },
  { 
    id: "3-08", 
    result: "3", 
    priority: 300, 
    when: { "SpO₂": "<94" }, 
    notes: "SpO₂ <94% ⇒ Độ 3", 
    source: "QĐ 292 – II.6 (Độ 3)" 
  },
  { 
    id: "2b-G1-01", 
    result: "2b", 
    priority: 250, 
    when: { "StartleObserved": "true" }, 
    notes: "Giật mình ghi nhận lúc khám ⇒ 2b", 
    source: "QĐ 292 – II.6 (Độ 2b)" 
  },
  { 
    id: "2a-02", 
    result: "2a", 
    priority: 200, 
    when: { 
      "TempC": ">=39", 
      "SpO₂": ">=94", 
      "GCS": ">=10", 
      "AVPU": "{A,V}", 
      "HR (không sốt)": "<=130", 
      "CRTsec": "<=2" 
    }, 
    notes: "Sốt ≥39°C với chỉ số an toàn ⇒ 2a", 
    source: "QĐ 292 – II.6 (Độ 2a)" 
  },
  { 
    id: "1-01", 
    result: "1", 
    priority: 100, 
    when: { 
      "RashHF": "true", 
      "StartleObserved": "false", 
      "StartleHist/30'": "<2", 
      "Somnolent": "false", 
      "Nystagmus": "không", 
      "GCS": ">=10", 
      "AVPU": "{A,V}", 
      "HR (không sốt)": "<=130", 
      "SpO₂": ">=94", 
      "CRTsec": "<=2" 
    }, 
    notes: "Có ban – không có dấu hiệu nâng bậc ⇒ 1", 
    source: "QĐ 292 – II.6 (Độ 1) + guard" 
  }
];

// Application state
let patientFacts = { AVPU: "A" };
let currentRules = STARTER_RULES;

// DOM Elements
let rulesEditor;
let degreeResult;
let explanationSection;
let ruleId, ruleNotes, ruleSource, matchedIds;
let calcHRBtn, exportCsvBtn;

/**
 * Initialize application
 */
async function init() {
  // Get DOM references
  rulesEditor = document.getElementById('rulesJsonEditor');
  degreeResult = document.getElementById('degreeResult');
  explanationSection = document.getElementById('explanationSection');
  ruleId = document.getElementById('ruleId');
  ruleNotes = document.getElementById('ruleNotes');
  ruleSource = document.getElementById('ruleSource');
  matchedIds = document.getElementById('matchedIds');
  calcHRBtn = document.getElementById('calcHRBtn');
  exportCsvBtn = document.getElementById('exportCsvBtn');

  // Load rules from external file
  await loadRulesFromFile();

  // Initialize rules editor
  rulesEditor.value = JSON.stringify(currentRules, null, 2);

  // Bind events
  bindFormEvents();
  bindButtonEvents();
  bindRulesEditor();

  // Initial evaluation
  updateResult();
}

/**
 * Load rules from external JSON file
 */
async function loadRulesFromFile() {
  try {
    const response = await fetch('../data/rules.json');
    if (response.ok) {
      const rules = await response.json();
      if (Array.isArray(rules) && rules.length > 0) {
        currentRules = rules;
        console.log(`Loaded ${rules.length} rules from file`);
      }
    }
  } catch (error) {
    console.warn('Could not load rules.json, using STARTER_RULES:', error);
    currentRules = STARTER_RULES;
  }
}

/**
 * Bind all form input events
 */
function bindFormEvents() {
  // Checkbox fields
  const checkboxes = document.querySelectorAll('input[type="checkbox"]');
  checkboxes.forEach(cb => {
    cb.addEventListener('change', (e) => {
      const fieldName = e.target.id;
      patientFacts[fieldName] = e.target.checked;
      updateResult();
    });
  });

  // Text and number fields
  const textInputs = document.querySelectorAll('input[type="text"], input[type="number"]:not([readonly])');
  textInputs.forEach(input => {
    input.addEventListener('input', (e) => {
      const fieldName = e.target.id;
      let value = e.target.value;
      
      // Convert to number for number inputs
      if (e.target.type === 'number' && value !== '') {
        value = Number(value);
      }
      
      patientFacts[fieldName] = value;
      updateResult();
    });
  });
}

/**
 * Bind button click events
 */
function bindButtonEvents() {
  // Calculate HR (không sốt)
  calcHRBtn.addEventListener('click', () => {
    const hrMeasured = document.getElementById('hrMeasured').value;
    const tempC = document.getElementById('TempC').value;

    if (hrMeasured === '' || tempC === '') {
      alert('Vui lòng nhập cả Mạch đo được và Nhiệt độ');
      return;
    }

    const adjustment = Math.max(0, (Number(tempC) - 38) * 10);
    const hrNoFever = Math.round(Number(hrMeasured) - adjustment);

    document.getElementById('HR (không sốt)').value = hrNoFever;
    patientFacts['HR (không sốt)'] = hrNoFever;
    patientFacts['TempC'] = Number(tempC);

    updateResult();
  });

  // Export CSV
  exportCsvBtn.addEventListener('click', exportToCSV);
}

/**
 * Bind rules editor changes
 */
function bindRulesEditor() {
  rulesEditor.addEventListener('input', () => {
    try {
      const parsed = JSON.parse(rulesEditor.value);
      if (Array.isArray(parsed)) {
        currentRules = parsed;
        updateResult();
      }
    } catch (e) {
      // Invalid JSON, keep using current rules
      console.warn('Invalid JSON in rules editor');
    }
  });
}

/**
 * Update result display based on current patient facts
 */
function updateResult() {
  const result = window.DMNEngine.evaluate(patientFacts, currentRules);
  
  degreeResult.textContent = result.degree;
  
  if (result.explain) {
    explanationSection.classList.remove('hidden');
    ruleId.textContent = result.explain.row_id;
    ruleNotes.textContent = result.explain.notes;
    ruleSource.textContent = result.explain.source;
    matchedIds.textContent = result.explain.matched_ids.join(', ');
  } else {
    explanationSection.classList.add('hidden');
  }
}

/**
 * Export patient data to CSV
 */
function exportToCSV() {
  const result = window.DMNEngine.evaluate(patientFacts, currentRules);
  const arr = Array(COLS.length).fill('');
  
  arr[0] = 'PATIENT-ROW';
  arr[1] = result.degree;
  
  // Fill in patient data
  COLS.forEach((colName, idx) => {
    if (idx < 2 || idx >= COLS.length - 2) return;
    const value = patientFacts[colName];
    if (value !== undefined && value !== '') {
      arr[idx] = String(value);
    }
  });
  
  // Create CSV content
  const csvContent = COLS.join(',') + '\n' + arr.join(',');
  
  // Create and download blob
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `patient_row_${Date.now()}.csv`;
  link.click();
  URL.revokeObjectURL(url);
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
