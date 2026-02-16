import { request } from "../api/api.js";

export const getUsers = () => request("/admin/users");
export const getRoles = () => request("/admin/roles");

export const assignRole = (userId, roleId) =>
    request("/admin/assign-role", "POST", {
        user_id: userId,
        role_id: roleId
    });

export const removeRole = (userId, roleId) =>
    request("/admin/remove-role", "POST", {
        user_id: userId,
        role_id: roleId
    });
