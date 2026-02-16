export function logout() {
    localStorage.removeItem("token");
    window.location.href = "index.html";
}

export function checkAuth() {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "index.html";
    }
}
