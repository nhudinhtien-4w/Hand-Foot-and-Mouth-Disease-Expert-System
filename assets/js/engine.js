/**
 * DMN Decision Engine - Core Logic
 * Chứa các hàm xử lý logic đánh giá rules và so sánh điều kiện
 */

// Priority map (hit policy: Priority)
const DEGREE_SCORE = { "4": 400, "3": 300, "2b": 250, "2a": 200, "1": 100 };

// Operator normalization mapping
const OPS = { "≤": "<=", "≥": ">=", "＝": "=", "–": "-" };

// Regex pattern for numeric comparison
const numCmp = /^\s*([<>]=?|=)\s*([-+]?\d+(?:\.\d+)?)/;

/**
 * Normalize condition string by replacing special operators
 * @param {string} s - Input condition string
 * @returns {string} - Normalized string
 */
function normalize(s) {
  let t = s;
  Object.entries(OPS).forEach(([k, v]) => {
    t = t.replaceAll(k, v);
  });
  return t.trim();
}

/**
 * Parse set notation {A,B,C} into a Set
 * @param {string} s - Input string with set notation
 * @returns {Set} - Set of values
 */
function parseSet(s) {
  return new Set(
    s.replace(/[{}]/g, "")
      .split(",")
      .map(x => x.trim())
      .filter(Boolean)
  );
}

/**
 * Compare two numbers with given operator
 * @param {number} x - Value to compare
 * @param {string} op - Operator (<, <=, >, >=, =, ==)
 * @param {number} n - Comparison target
 * @returns {boolean} - Comparison result
 */
function compareNumbers(x, op, n) {
  switch (op) {
    case '<': return x < n;
    case '<=': return x <= n;
    case '>': return x > n;
    case '>=': return x >= n;
    case '=':
    case '==': return x === n;
    default: return false;
  }
}

/**
 * Check if a patient value meets a condition
 * @param {string|null} cond - Condition to check
 * @param {any} value - Patient value
 * @returns {boolean} - Whether condition is met
 */
function meets(cond, value) {
  // Empty condition always passes
  if (cond == null || cond === "") return true;
  // Empty value fails non-empty condition
  if (value == null || value === "") return false;

  const s = normalize(String(cond));
  const vRaw = value;

  // Boolean check
  if (s.toLowerCase() === "true" || s.toLowerCase() === "false") {
    return String(vRaw).toLowerCase() === s.toLowerCase();
  }

  // "không" means false
  if (s === "không") return !Boolean(vRaw);

  // Set membership {A,V,P}
  if (s.startsWith("{") && s.endsWith("}")) {
    return parseSet(s).has(String(vRaw).trim());
  }

  // Rate per hour (e.g., >2/h)
  if (s.endsWith("/h")) {
    const m = numCmp.exec(s.replace("/h", ""));
    if (!m) return false;
    const op = m[1], n = parseFloat(m[2]);
    const x = parseFloat(String(vRaw));
    if (Number.isNaN(x)) return false;
    return compareNumbers(x, op, n);
  }

  // Numeric comparison with operator prefix
  if (numCmp.test(s)) {
    const m = numCmp.exec(s);
    const op = m[1], n = parseFloat(m[2]);
    const x = parseFloat(String(vRaw));
    if (Number.isNaN(x)) return false;
    return compareNumbers(x, op, n);
  }

  // Numeric comparison without space
  if (s.match(/^[<>]=?\d+$/) || s.match(/^=\d+$/)) {
    const op = s.startsWith(">=") ? ">=" : 
               s.startsWith("<=") ? "<=" : 
               s.startsWith(">") ? ">" : 
               s.startsWith("<") ? "<" : "==";
    const n = parseFloat(s.replace(/[<>]=?|=/, ""));
    const x = parseFloat(String(vRaw));
    if (Number.isNaN(x)) return false;
    return compareNumbers(x, op, n);
  }

  // Age in months comparison
  if (s === "<12m" || s === "<=12m" || s === "≥12m" || s === ">=12m") {
    const months = parseFloat(String(vRaw));
    if (Number.isNaN(months)) return false;
    return s.includes("<") ? months < 12 : months >= 12;
  }

  // Exact string match
  return String(vRaw).trim().toLowerCase() === s.toLowerCase();
}

/**
 * Evaluate patient data against rules
 * @param {Object} patient - Patient facts/data
 * @param {Array} rules - Array of rule objects
 * @returns {Object} - Result with degree and explanation
 */
function evaluate(patient, rules) {
  // Find all rules that match patient data
  const matched = rules.filter(r => {
    const when = r.when || {};
    return Object.entries(when).every(([k, cond]) => meets(cond, patient[k]));
  });

  // No rules matched
  if (matched.length === 0) {
    return { 
      degree: "Không xác định", 
      explain: null 
    };
  }

  // Sort by priority (highest first) and pick the best
  const best = matched.sort((a, b) => {
    return (DEGREE_SCORE[b.result] - DEGREE_SCORE[a.result]) || 0;
  })[0];

  return {
    degree: best.result,
    explain: {
      row_id: best.id,
      notes: best.notes,
      source: best.source,
      matched_ids: matched.map(m => m.id)
    }
  };
}

// Export functions for use in app.js
window.DMNEngine = {
  evaluate,
  meets,
  normalize,
  DEGREE_SCORE
};
