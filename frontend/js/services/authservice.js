import { request } from "../api/api.js";

export async function login(username, password) {
    return request("/auth/login", "POST", { username, password });
}
