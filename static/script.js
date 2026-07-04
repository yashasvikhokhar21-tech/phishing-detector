/**
 * Phishing Detector - JavaScript
 * Frontend logic for URL analysis
 */

let batchData = [];
const HISTORY_KEY = 'phishing_recent_checks';
const THEME_KEY = 'phishing_theme';

/**
 * Validate URL format
 */
function isValidUrl(url) {
    try {
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
            url = 'https://' + url;
        }
        new URL(url);
        return true;
    } catch (error) {
        return false;
    }
}

/**
 * Check a single URL
 */
async function checkUrl() {
    const urlInput = document.getElementById('url-input');
    const url = urlInput.value.trim();
    const resultDiv = document.getElementById('single-result');
    const errorDiv = document.getElementById('error-message');
    const loadingDiv = document.getElementById('loading');

    resultDiv.style.display = 'none';
    errorDiv.style.display = 'none';
    errorDiv.textContent = '';

    if (!url) {
        errorDiv.textContent = 'Please enter a URL';
        errorDiv.style.display = 'block';
        urlInput.focus();
        return;
    }

    if (!isValidUrl(url)) {
        errorDiv.textContent = 'Please enter a valid URL (e.g., example.com or https://example.com)';
        errorDiv.style.display = 'block';
        return;
    }

    loadingDiv.style.display = 'block';

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'An error occurred');
        }

        displayResult(data);
        resultDiv.style.display = 'block';
        saveRecentCheck(data);
    } catch (error) {
        errorDiv.textContent = `Error: ${error.message}`;
        errorDiv.style.display = 'block';
    } finally {
        loadingDiv.style.display = 'none';
    }
}

/**
 * Display single prediction result
 */
function displayResult(data) {
    const statusDiv = document.getElementById('result-status');
    const detailsDiv = document.getElementById('result-details');
    const featuresList = document.getElementById('features-list');

    const isPhishing = data.is_phishing;
    const statusClass = isPhishing ? 'status-phishing' : 'status-legitimate';
    const statusText = isPhishing ? '⚠️ PHISHING DETECTED' : '✓ LEGITIMATE';
    statusDiv.className = statusClass;
    statusDiv.textContent = statusText;

    const ruleScore = data.rule_score !== undefined ? (data.rule_score * 100).toFixed(2) : '0.00';
    const finalScore = data.final_score !== undefined ? (data.final_score * 100).toFixed(2) : '0.00';
    const mlConfidence = (data.confidence * 100).toFixed(2);

    const dashboardHtml = `
        <div class="score-card score-ml">
            <span>ML Confidence</span>
            <strong>${mlConfidence}%</strong>
        </div>
        <div class="score-card score-rule">
            <span>Rule Score</span>
            <strong>${ruleScore}%</strong>
        </div>
        <div class="score-card score-final">
            <span>Final Score</span>
            <strong>${finalScore}%</strong>
        </div>
    `;
    document.getElementById('result-dashboard').innerHTML = dashboardHtml;

    detailsDiv.innerHTML = `
        <p><strong>URL:</strong> ${escapeHtml(data.url)}</p>
        <p><strong>Prediction:</strong> ${escapeHtml(data.prediction_text)}</p>
    `;

    const reasons = Array.isArray(data.rule_reasons) ? data.rule_reasons : [];
    const reasonsContainer = document.getElementById('rule-reasons');
    if (reasons.length > 0) {
        let reasonsHtml = '<h4>Triggered Rules</h4><ul class="rule-list">';
        reasons.forEach(reason => {
            reasonsHtml += `<li>${escapeHtml(reason.replace(/_/g, ' '))}</li>`;
        });
        reasonsHtml += '</ul>';
        reasonsContainer.innerHTML = reasonsHtml;
    } else {
        reasonsContainer.innerHTML = '<p class="muted">No rule-based risks detected.</p>';
    }

    let featuresHtml = '';
    for (const [key, value] of Object.entries(data.features)) {
        featuresHtml += `
            <div class="feature-item">
                <strong>${escapeHtml(key)}:</strong>
                <span>${escapeHtml(String(value))}</span>
            </div>
        `;
    }
    featuresList.innerHTML = featuresHtml;
}

/**
 * Check multiple URLs (batch)
 */
async function checkBatch() {
    const batchInput = document.getElementById('batch-input');
    const inputText = batchInput.value.trim();
    const resultDiv = document.getElementById('batch-result');
    const errorDiv = document.getElementById('batch-error');
    const loadingDiv = document.getElementById('batch-loading');

    resultDiv.style.display = 'none';
    errorDiv.style.display = 'none';
    errorDiv.textContent = '';

    const urls = inputText
        .split('\n')
        .map(url => url.trim())
        .filter(url => url.length > 0);

    if (urls.length === 0) {
        errorDiv.textContent = 'Please enter at least one URL';
        errorDiv.style.display = 'block';
        batchInput.focus();
        return;
    }

    if (urls.length > 100) {
        errorDiv.textContent = 'Maximum 100 URLs allowed';
        errorDiv.style.display = 'block';
        return;
    }

    const invalidUrls = urls.filter(url => !isValidUrl(url));
    if (invalidUrls.length > 0) {
        errorDiv.textContent = `Invalid URL format: ${invalidUrls[0]}`;
        errorDiv.style.display = 'block';
        return;
    }

    loadingDiv.style.display = 'block';

    try {
        const response = await fetch('/batch-predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ urls: urls })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'An error occurred');
        }

        displayBatchResults(data);
        resultDiv.style.display = 'block';
    } catch (error) {
        errorDiv.textContent = `Error: ${error.message}`;
        errorDiv.style.display = 'block';
    } finally {
        loadingDiv.style.display = 'none';
    }
}

/**
 * Display batch prediction results
 */
function displayBatchResults(data) {
    document.getElementById('total-urls').textContent = data.total;
    document.getElementById('phishing-count').textContent = data.phishing_count;
    document.getElementById('safe-count').textContent = data.safe_count || 0;
    document.getElementById('error-count').textContent = data.error_count || 0;

    batchData = data.results || [];

    const resultsList = document.getElementById('batch-results-list');
    let html = '';

    for (const result of batchData) {
        if (result.error) {
            html += `
                <div class="batch-result-item" style="border-left-color: #ffc107;">
                    <div class="url">${escapeHtml(result.url || 'Unknown')}</div>
                    <span class="badge" style="background: #fff3cd; color: #856404;">Error</span>
                </div>
            `;
            continue;
        }

        const isPhishing = result.is_phishing;
        const className = isPhishing ? 'phishing' : 'legitimate';
        const badgeClass = isPhishing ? 'badge-phishing' : 'badge-legitimate';
        const badgeText = isPhishing ? '⚠️ Phishing' : '✓ Legitimate';
        const confidence = (result.confidence * 100).toFixed(2);
        const finalScore = result.final_score !== undefined ? (result.final_score * 100).toFixed(2) : '0.00';

        html += `
            <div class="batch-result-item ${className}">
                <div class="url">
                    ${escapeHtml(result.url)}<br>
                    <small style="color: #6c757d;">Confidence: ${confidence}% • Final Score: ${finalScore}%</small>
                </div>
                <span class="badge ${badgeClass}">${badgeText}</span>
            </div>
        `;
    }

    resultsList.innerHTML = html;
    saveBatchHistory(batchData);
}

/**
 * Export batch results as CSV
 */
function exportBatchResults() {
    if (!batchData || batchData.length === 0) {
        alert('No batch results available to export.');
        return;
    }

    const rows = [
        ['URL', 'Prediction', 'ML Confidence', 'Rule Score', 'Final Score', 'Error']
    ];

    batchData.forEach(item => {
        rows.push([
            item.url || '',
            item.prediction_text || '',
            item.confidence !== undefined ? (item.confidence * 100).toFixed(2) : '',
            item.rule_score !== undefined ? (item.rule_score * 100).toFixed(2) : '',
            item.final_score !== undefined ? (item.final_score * 100).toFixed(2) : '',
            item.error || ''
        ]);
    });

    const csvContent = rows.map(row => row.map(value => `"${String(value).replace(/"/g, '""')}"`).join(',')).join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'batch-results.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

/**
 * Copy the displayed result text to clipboard
 */
function copyResult() {
    const text = buildResultText();
    if (!navigator.clipboard) {
        alert('Copy not supported in this browser.');
        return;
    }

    navigator.clipboard.writeText(text).then(() => {
        const feedback = document.getElementById('copy-feedback');
        feedback.textContent = 'Copied!';
        setTimeout(() => feedback.textContent = '', 2000);
    }).catch(() => {
        alert('Unable to copy result.');
    });
}

/**
 * Build text for clipboard copy
 */
function buildResultText() {
    const url = document.getElementById('url-input').value.trim();
    const predictionText = document.querySelector('#result-details p:nth-child(2)')?.textContent || '';
    const ruleScore = document.querySelector('.score-rule strong')?.textContent || '';
    const mlConfidence = document.querySelector('.score-ml strong')?.textContent || '';
    const finalScore = document.querySelector('.score-final strong')?.textContent || '';

    return `URL: ${url}\n${predictionText}\nML Confidence: ${mlConfidence}\nRule Score: ${ruleScore}\nFinal Score: ${finalScore}`;
}

/**
 * Fill the example URL into the input field and analyze it
 */
function fillExample(url) {
    const urlInput = document.getElementById('url-input');
    urlInput.value = url;
    validateUrlInput();
    // Automatically analyze the URL
    checkUrl();
}

/**
 * Save a single URL result to history
 */
function saveRecentCheck(result) {
    const history = loadHistory();
    const item = {
        url: result.url || '',
        prediction: result.prediction_text || '',
        final_score: result.final_score !== undefined ? (result.final_score * 100).toFixed(2) : '0.00',
        timestamp: new Date().toISOString()
    };
    history.unshift(item);
    if (history.length > 10) {
        history.pop();
    }
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    renderHistory();
    renderSummaryCounts();
}

/**
 * Save batch results into recent history
 */
function saveBatchHistory(results) {
    if (!Array.isArray(results)) return;
    const history = loadHistory();
    results.forEach(result => {
        if (result.error) return;
        const item = {
            url: result.url || '',
            prediction: result.prediction_text || '',
            final_score: result.final_score !== undefined ? (result.final_score * 100).toFixed(2) : '0.00',
            timestamp: new Date().toISOString()
        };
        history.unshift(item);
    });
    history.splice(10);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history));
    renderHistory();
    renderSummaryCounts();
}

/**
 * Load history from localStorage
 */
function loadHistory() {
    try {
        const stored = localStorage.getItem(HISTORY_KEY);
        return stored ? JSON.parse(stored) : [];
    } catch (error) {
        return [];
    }
}

/**
 * Render history list
 */
function renderHistory() {
    const history = loadHistory();
    const historyList = document.getElementById('history-list');
    if (!historyList) return;

    if (history.length === 0) {
        historyList.innerHTML = '<li>No recent checks yet.</li>';
        return;
    }

    historyList.innerHTML = history.map(item => `
        <li>
            <span>${escapeHtml(item.url)}</span>
            <button type="button" onclick="fillExample('${escapeHtml(item.url)}')">Use</button>
        </li>
    `).join('');
}

/**
 * Clear URL history
 */
function clearHistory() {
    localStorage.removeItem(HISTORY_KEY);
    renderHistory();
    renderSummaryCounts();
}

/**
 * Validate URL input live and show helper text
 */
function validateUrlInput() {
    const urlInput = document.getElementById('url-input');
    const helper = document.getElementById('url-validation');
    const url = urlInput.value.trim();

    if (!url) {
        helper.textContent = 'Enter a website address to analyze.';
        return;
    }

    helper.textContent = isValidUrl(url)
        ? 'Looks good — ready to analyze.'
        : 'URL looks invalid. Examples: example.com, https://example.com';
}

/**
 * Update the summary counters from history
 */
function renderSummaryCounts() {
    const history = loadHistory();
    const total = history.length;
    const phishing = history.filter(item => item.prediction && item.prediction.toLowerCase().includes('phishing')).length;
    const safe = total - phishing;

    document.getElementById('summary-total').textContent = total;
    document.getElementById('summary-phishing').textContent = phishing;
    document.getElementById('summary-safe').textContent = safe;
}

/**
 * Toggle dark/light theme
 */
function toggleTheme() {
    const body = document.body;
    body.classList.toggle('dark-mode');
    const isDark = body.classList.contains('dark-mode');
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.textContent = isDark ? 'Light Mode' : 'Dark Mode';
    }
    localStorage.setItem(THEME_KEY, isDark ? 'dark' : 'light');
}

function loadTheme() {
    const stored = localStorage.getItem(THEME_KEY);
    if (stored === 'dark') {
        document.body.classList.add('dark-mode');
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.textContent = 'Light Mode';
        }
    }
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

window.addEventListener('DOMContentLoaded', function() {
    const urlInput = document.getElementById('url-input');
    const batchInput = document.getElementById('batch-input');
    const themeToggle = document.getElementById('theme-toggle');

    loadTheme();
    renderHistory();
    renderSummaryCounts();
    validateUrlInput();

    if (urlInput) {
        urlInput.addEventListener('input', function() {
            validateUrlInput();
            document.getElementById('single-result').style.display = 'none';
            document.getElementById('error-message').style.display = 'none';
        });
        urlInput.addEventListener('keypress', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                checkUrl();
            }
        });
    }

    if (batchInput) {
        batchInput.addEventListener('input', function() {
            document.getElementById('batch-result').style.display = 'none';
            document.getElementById('batch-error').style.display = 'none';
        });
        batchInput.addEventListener('keydown', function(event) {
            if (event.ctrlKey && event.key === 'Enter') {
                event.preventDefault();
                checkBatch();
            }
        });
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }
});
