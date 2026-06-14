/**
 * auth_finished.js
 * Client-side authentication and vault key management.
 * Token + DEK live in localStorage. A plain cookie mirrors the token
 * so that browser page navigations (link clicks, redirects) also
 * carry the token automatically — no server session involved.
 */

let userCache = null;

// ── Token Management ─────────────────────────────────────────────────────────

function setToken(token) {
    localStorage.setItem("access_token", token);
    // Mirror token as a plain browser cookie for page navigation
    document.cookie = `access_token=${token}; path=/; SameSite=Lax; max-age=3600`;
}

function getToken() {
    return localStorage.getItem("access_token");
}

function clearToken() {
    localStorage.removeItem("access_token");
    // Expire the cookie
    document.cookie = "access_token=; path=/; SameSite=Lax; max-age=0";
    userCache = null;
}

// ── DEK (Data Encryption Key) Management ─────────────────────────────────────

function setDek(dek) {
    localStorage.setItem("vault_dek", dek);
}

function getDek() {
    return localStorage.getItem("vault_dek");
}

function clearDek() {
    localStorage.removeItem("vault_dek");
}

// ── Auth Headers Builder ─────────────────────────────────────────────────────

function authHeaders(extra = {}) {
    const headers = { ...extra };
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
    const dek = getDek();
    if (dek) headers["X-Vault-Key"] = dek;
    return headers;
}

// ── Get Current User ─────────────────────────────────────────────────────────

function getCurrentUser() {
    return new Promise((resolve, reject) => {
        if (userCache) {
            resolve(userCache);
            return;
        }

        fetch("/api/auth/me", { headers: authHeaders() })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Authentication failed");
                }
                return response.json();
            })
            .then(user => {
                userCache = user;
                resolve(user);
            })
            .catch(err => {
                reject(err);
            });
    });
}

// ── Login ────────────────────────────────────────────────────────────────────

async function handleLogin(email, password) {
    const body = new URLSearchParams();
    body.append("username", email);    // OAuth2 spec uses "username"
    body.append("password", password);

    const response = await fetch("/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: body,
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.detail || "Login failed");
    }

    // Store token in localStorage + cookie, DEK in localStorage
    setToken(data.access_token);
    if (data.dek) {
        setDek(data.dek);
    }

    return data;
}

// ── Logout ───────────────────────────────────────────────────────────────────

function handleLogout() {
    clearToken();
    clearDek();
    window.location.href = "/login";
}

// ── Auth Guard (call on protected pages) ─────────────────────────────────────

function requireAuth() {
    if (!getToken()) {
        window.location.href = "/login";
        return false;
    }
    return true;
}
