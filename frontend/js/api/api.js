const BASE_URL = "http://localhost:8001";

export async function request(endpoint, method = "GET", body = null) {
    const token = localStorage.getItem("token");

    const options = {
        method,
        headers: {
            "Content-Type": "application/json",
        }
    };

    if (token) {
        options.headers["Authorization"] = `Bearer ${token}`;
    }

    if (body) {
        options.body = JSON.stringify(body);
    }

    const response = await fetch(`${BASE_URL}${endpoint}`, options);

    if (!response.ok) {
        throw new Error("Request failed");
    }

    return response.json();
}
