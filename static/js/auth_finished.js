/**
 * auth_finished.js
 * Client-side session and authentication helpers.
 */

let userCache = null;

function setToken(token) {
    localStorage.setItem("access_token", token);
}

function getToken() {
    return localStorage.getItem("access_token");
}

function clearToken() {
    localStorage.removeItem("access_token");
    userCache = null;
}

/**
 * Returns a Promise containing the authenticated user object.
 * Caches the response in userCache to avoid redundant API requests.
 */
function getCurrentUser() {
    return new Promise((resolve, reject) => {
        if (userCache) {
            resolve(userCache);
            return;
        }

        // Send token via standard Authorization header (compatible with OAuth2PasswordBearer)
        const token = getToken();
        const headers = {};
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }

        fetch("/api/auth/me", { headers })
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

function handleLogout() {
    clearToken();
    window.location.href = "/login";
}

