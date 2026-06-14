let userCache = null;

function setToken(token) {
    localStorage.setItem("access_token", token);
    document.cookie = `access_token=${token}; path=/; SameSite=Lax; max-age=3600`;
}

function getToken() {
    return localStorage.getItem("access_token");
}

function clearToken() {
    localStorage.removeItem("access_token");
    document.cookie = "access_token=; path=/; SameSite=Lax; max-age=0";
    userCache = null;
}

function authHeaders(extra = {}) {
    const headers = { ...extra };
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
    return headers;
}

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

async function handleLogin(email, password) {
    const body = new URLSearchParams();
    body.append("username", email);
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

    setToken(data.access_token);
    return data;
}

function handleLogout() {
    clearToken();
    window.location.href = "/login";
}

function requireAuth() {
    if (!getToken()) {
        window.location.href = "/login";
        return false;
    }
    return true;
}
