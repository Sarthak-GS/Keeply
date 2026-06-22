let API = "https://keeply-liard.vercel.app";

const $ = (s) => document.getElementById(s);
const viewLogin = $("view-login");
const viewConnected = $("view-connected");
const statusDot = $("status-dot");
const credList = $("cred-list");
const toast = $("toast");

// ── Toast helper ────────────────────────────────────────────────────────────
function showToast(msg, isError = false) {
  toast.textContent = msg;
  toast.className = "toast show" + (isError ? " error" : "");
  setTimeout(() => (toast.className = "toast"), 2500);
}

// ── Init: decide which view to show ─────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get(["keeply_token", "keeply_server_url"], (res) => {
    if (res.keeply_server_url) {
      API = res.keeply_server_url;
      $("server-url").value = API;
    }
    if (res.keeply_token) {
      showConnected();
    } else {
      showLogin();
    }
  });
});

function showLogin() {
  viewLogin.style.display = "block";
  viewConnected.style.display = "none";
  statusDot.classList.remove("online");
}

function showConnected() {
  viewLogin.style.display = "none";
  viewConnected.style.display = "block";
  statusDot.classList.add("online");
  loadPending();
}

// ── Login ───────────────────────────────────────────────────────────────────
let isLoggingIn = false;
$("login-btn").addEventListener("click", async () => {
  if (isLoggingIn) return;
  const serverUrl = $("server-url").value.trim().replace(/\/$/, "");
  const email = $("email").value.trim();
  const pw = $("password").value;
  const errEl = $("login-error");
  errEl.style.display = "none";

  if (!serverUrl) {
    errEl.textContent = "Server URL is required.";
    errEl.style.display = "block";
    return;
  }
  if (!email || !pw) {
    errEl.textContent = "Both fields are required.";
    errEl.style.display = "block";
    return;
  }

  API = serverUrl;
  isLoggingIn = true;
  const btn = $("login-btn");
  const origText = btn.textContent;
  btn.textContent = "Linking...";
  btn.disabled = true;

  const body = new URLSearchParams();
  body.append("username", email);
  body.append("password", pw);

  try {
    const r = await fetch(`${API}/token`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });
    const data = await r.json();
    if (r.ok && data.access_token) {
      chrome.storage.local.set({ 
        keeply_token: data.access_token,
        keeply_server_url: API
      }, () => {
        showToast("Connected!");
        isLoggingIn = false;
        btn.textContent = origText;
        btn.disabled = false;
        showConnected();
      });
    } else {
      errEl.textContent = data.detail || "Authentication failed.";
      errEl.style.display = "block";
      isLoggingIn = false;
      btn.textContent = origText;
      btn.disabled = false;
    }
  } catch {
    errEl.textContent = "Cannot reach Keeply server.";
    errEl.style.display = "block";
    isLoggingIn = false;
    btn.textContent = origText;
    btn.disabled = false;
  }
});

// Allow pressing Enter in password field
$("password").addEventListener("keydown", (e) => {
  if (e.key === "Enter") $("login-btn").click();
});

// ── Logout ──────────────────────────────────────────────────────────────────
$("logout-btn").addEventListener("click", () => {
  chrome.storage.local.remove(["keeply_token"], () => {
    showToast("Disconnected");
    showLogin();
  });
});

// ── Pending credentials list ────────────────────────────────────────────────
function loadPending() {
  chrome.storage.local.get(["pending_creds"], (res) => {
    const list = res.pending_creds || [];
    credList.innerHTML = "";

    if (list.length === 0) {
      credList.innerHTML = `
        <div class="empty-state">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="#64748b"><path d="M12 2L4 6v5c0 5.55 3.84 10.74 8 12 4.16-1.26 8-6.45 8-12V6l-8-4z"/></svg>
          <div>No pending credentials.<br/>Submit a login form on any site to capture.</div>
        </div>`;
      return;
    }

    list.forEach((cred, idx) => {
      const card = document.createElement("div");
      card.className = "cred-card";
      card.innerHTML = `
        <div class="cred-site">${escHtml(cred.site || cred.title)}</div>
        <div class="cred-user">${escHtml(cred.username || "(no username)")}</div>
        <div class="cred-actions">
          <button class="btn btn-small btn-save" data-idx="${idx}">Save to Vault</button>
          <button class="btn btn-small btn-dismiss" data-idx="${idx}">Dismiss</button>
        </div>`;
      credList.appendChild(card);
    });

    // Attach event listeners
    credList.querySelectorAll(".btn-save").forEach((btn) => {
      btn.addEventListener("click", () => saveCred(parseInt(btn.dataset.idx), btn));
    });
    credList.querySelectorAll(".btn-dismiss").forEach((btn) => {
      btn.addEventListener("click", () => dismissCred(parseInt(btn.dataset.idx)));
    });
  });
}

// ── Save a credential to the vault ──────────────────────────────────────────
async function saveCred(idx, btn) {
  if (btn.disabled) return;
  const res = await new Promise((r) =>
    chrome.storage.local.get(["keeply_token", "pending_creds"], r)
  );
  const token = res.keeply_token;
  const list = res.pending_creds || [];
  const cred = list[idx];
  if (!token || !cred) return;

  btn.disabled = true;
  const origText = btn.textContent;
  btn.textContent = "Saving...";

  try {
    const r = await fetch(`${API}/vault/new`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        title: cred.title || cred.site,
        username: cred.username,
        password: cred.password,
        url: cred.url,
        notes: "Saved via Keeply extension",
        folder_id: null,
      }),
    });

    if (r.ok) {
      showToast("Saved to vault!");
      list.splice(idx, 1);
      chrome.storage.local.set({ pending_creds: list }, loadPending);
    } else {
      btn.disabled = false;
      btn.textContent = origText;
      if (r.status === 401) {
        showToast("Session expired — reconnect.", true);
        chrome.storage.local.remove(["keeply_token"]);
        showLogin();
      } else {
        showToast("Save failed.", true);
      }
    }
  } catch {
    btn.disabled = false;
    btn.textContent = origText;
    showToast("Cannot reach server.", true);
  }
}

// ── Dismiss a pending credential ────────────────────────────────────────────
function dismissCred(idx) {
  chrome.storage.local.get(["pending_creds"], (res) => {
    const list = res.pending_creds || [];
    list.splice(idx, 1);
    chrome.storage.local.set({ pending_creds: list }, loadPending);
  });
}

// ── Escape HTML to prevent XSS in credential display ────────────────────────
function escHtml(str) {
  const d = document.createElement("div");
  d.textContent = str;
  return d.innerHTML;
}
