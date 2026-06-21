// Intercept form submissions that contain a password field
document.addEventListener("submit", (e) => {
  const form = e.target;
  const passwordInput = form.querySelector('input[type="password"]');
  if (!passwordInput || !passwordInput.value) return;

  // Walk backwards from password input to find the username/email field
  const inputs = Array.from(form.querySelectorAll("input"));
  const passIdx = inputs.indexOf(passwordInput);
  let usernameVal = "";

  for (let i = passIdx - 1; i >= 0; i--) {
    const t = (inputs[i].getAttribute("type") || "text").toLowerCase();
    if (["text", "email", "tel"].includes(t)) {
      usernameVal = inputs[i].value;
      break;
    }
  }

  // Also check by common name/id attributes if walk-back didn't find it
  if (!usernameVal) {
    const sel = form.querySelector(
      'input[name*="user"], input[name*="email"], input[name*="login"], ' +
      'input[id*="user"], input[id*="email"], input[id*="login"]'
    );
    if (sel && sel !== passwordInput) usernameVal = sel.value;
  }

  const cred = {
    title: document.title || window.location.hostname,
    site: window.location.hostname,
    username: usernameVal,
    password: passwordInput.value,
    url: window.location.origin,
    capturedAt: Date.now(),
  };

  chrome.storage.local.get(["pending_creds"], (res) => {
    const list = res.pending_creds || [];
    // Avoid duplicates for the same site+username
    const exists = list.some(
      (c) => c.url === cred.url && c.username === cred.username
    );
    if (!exists) {
      list.push(cred);
      chrome.storage.local.set({ pending_creds: list });
    }
  });
});
