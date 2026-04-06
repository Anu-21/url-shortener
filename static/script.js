/* ═══════════════════════════════════════════════════════════════════
   QuickURL — Client-Side Logic
   ═══════════════════════════════════════════════════════════════════ */

// ── DOM References ──────────────────────────────────────────────────
const $       = (sel) => document.querySelector(sel);
const longUrl     = $('#longUrl');
const shortenBtn  = $('#shortenBtn');
const btnLabel    = $('.btn-label');
const btnSpinner  = $('.btn-spinner');
const errorMsg    = $('#errorMsg');
const result      = $('#result');
const shortLink   = $('#shortLink');
const copyBtn     = $('#copyBtn');
const totalUrls   = $('#totalUrls');
const toast       = $('#toast');

// ── Init ────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    shortenBtn.addEventListener('click', handleShorten);
    copyBtn.addEventListener('click', handleCopy);

    // Trigger shorten on Enter key
    longUrl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleShorten();
        }
    });
});

// ── Shorten Handler ─────────────────────────────────────────────────
async function handleShorten() {
    const url = longUrl.value.trim();
    if (!url) {
        showError('Please enter a URL.');
        return;
    }

    setLoading(true);
    hideError();
    hideResult();

    try {
        const res = await fetch('/shorten', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ long_url: url }),
        });

        const data = await res.json();

        if (!res.ok) {
            showError(data.error || 'Something went wrong. Please try again.');
            return;
        }

        // Show result
        shortLink.textContent = data.short_url;
        shortLink.href = data.short_url;
        result.hidden = false;

        longUrl.value = '';

        // Refresh stats
        fetchStats();
    } catch (err) {
        showError('Network error. Please check your connection and try again.');
    } finally {
        setLoading(false);
    }
}

// ── Copy Handler ────────────────────────────────────────────────────
async function handleCopy() {
    const url = shortLink.textContent;
    if (!url) return;

    try {
        await navigator.clipboard.writeText(url);
        showToast();
    } catch {
        // Fallback: select text if clipboard API is unavailable
        const range = document.createRange();
        range.selectNodeContents(shortLink);
        const sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    }
}

// ── Fetch Stats ─────────────────────────────────────────────────────
async function fetchStats() {
    try {
        const res = await fetch('/stats');
        const data = await res.json();
        totalUrls.textContent = data.total_urls;
    } catch {
        totalUrls.textContent = '—';
    }
}

// ── UI Helpers ──────────────────────────────────────────────────────
function setLoading(on) {
    shortenBtn.disabled = on;
    btnLabel.hidden = on;
    btnSpinner.hidden = !on;
}

function showError(msg) {
    errorMsg.textContent = msg;
    errorMsg.hidden = false;
}

function hideError() {
    errorMsg.hidden = true;
}

function hideResult() {
    result.hidden = true;
}

function showToast() {
    toast.hidden = false;
    // Force reflow so the transition triggers even if called rapidly
    void toast.offsetWidth;
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => { toast.hidden = true; }, 300);
    }, 2000);
}
