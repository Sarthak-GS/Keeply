function showToast(message, isError = false) {
    const toast = document.getElementById('toast');
    if (!toast) return;

    toast.textContent = (isError ? '⚠️ ' : '') + message;
    toast.className = [
        'fixed bottom-6 right-6 z-50 rounded-xl border px-5 py-3 text-sm font-medium shadow-glow backdrop-blur transition-all duration-300',
        isError
            ? 'border-red-500/30 bg-slate-900 text-red-300'
            : 'border-emerald-500/30 bg-slate-900 text-emerald-300',
    ].join(' ');

    toast.style.opacity = '1';
    toast.style.transform = 'translateY(0)';

    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(8px)';
    }, 3500);
}

function copyToClipboard(text, label = 'Copied') {
    navigator.clipboard.writeText(text)
        .then(() => showToast(`${label}!`))
        .catch(() => showToast('Copy failed — check browser permissions.', true));
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
