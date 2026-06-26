function showToast(message, isError = false) {
    const toast = document.getElementById('toast');
    if (!toast) return;

    toast.textContent = (isError ? '⚠️ ' : '') + message;
    toast.className = [
        'rounded-xl border px-5 py-3 text-sm font-medium shadow-glow backdrop-blur transition-all duration-300 text-center sm:text-left pointer-events-none',
        isError
            ? 'border-red-500/30 bg-slate-900 text-red-300'
            : 'border-emerald-500/30 bg-slate-900 text-emerald-300',
    ].join(' ');

    toast.classList.remove('hidden');
    // Force a reflow to make the opacity transition play
    toast.offsetHeight;

    toast.style.opacity = '1';
    toast.style.transform = 'translateY(0)';

    clearTimeout(toast._timer);
    clearTimeout(toast._hideTimer);
    toast._timer = setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(8px)';
        toast._hideTimer = setTimeout(() => {
            toast.classList.add('hidden');
        }, 300);
    }, 3500);
}

function copyToClipboard(text, label = 'Copied') {
    navigator.clipboard.writeText(text)
        .then(() => showToast(`${label}!`))
        .catch(() => showToast('Copy failed — check browser permissions.', true));
}

/**
 * Prevent double-submit on any button.
 * Usage: const release = guardButton(btn); ... release();
 * While guarded, the button is disabled and shows a spinner.
 */
function guardButton(btn) {
    if (!btn || btn.disabled) return null;
    btn.disabled = true;
    const original = btn.innerHTML;
    btn.innerHTML = '<span class="inline-block animate-spin mr-1">⏳</span> Wait…';
    btn.classList.add('opacity-60', 'pointer-events-none');

    return function release() {
        btn.disabled = false;
        btn.innerHTML = original;
        btn.classList.remove('opacity-60', 'pointer-events-none');
    };
}

document.addEventListener('DOMContentLoaded', () => {
    const banner = document.getElementById('flash-banner');
    if (banner) {
        setTimeout(() => {
            banner.style.transition = 'opacity 0.5s';
            banner.style.opacity = '0';
            setTimeout(() => banner.remove(), 500);
        }, 4000);
    }
});
