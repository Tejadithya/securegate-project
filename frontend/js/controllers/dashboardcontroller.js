import { getUsers, getRoles, assignRole } from "../services/userService.js";
import { getAuditLogs } from "../services/auditservice.js";
import { logout, checkAuth } from "../utils/authutils.js";

document.getElementById("logoutBtn").addEventListener("click", logout);

window.addEventListener("DOMContentLoaded", async () => {
    checkAuth();
    await loadDashboard();
});

async function loadDashboard() {
    const users = await getUsers();
    const roles = await getRoles();
    const logs = await getAuditLogs();

    renderUsers(users, roles);
    renderLogs(logs);
}

function renderUsers(users, roles) {
    const table = document.getElementById("userTable");
    table.innerHTML = "";

    users.forEach(user => {
        const row = document.createElement("tr");

        const roleOptions = roles.map(role =>
            `<option value="${role.id}">${role.name}</option>`
        ).join("");

        row.innerHTML = `
            <td>${user.username}</td>
            <td>${user.roles.join(", ")}</td>
            <td>
                <div class="d-flex gap-2">
                    <select class="form-select form-select-sm" id="role-${user.id}">
                        ${roleOptions}
                    </select>
                    <button class="btn btn-sm btn-primary"
                        onclick="assignUserRole(${user.id})">
                        Assign
                    </button>
                </div>
            </td>
        `;

        table.appendChild(row);
    });
}

function renderLogs(logs) {
    const list = document.getElementById("auditLogList");
    list.innerHTML = "";

    logs.slice(0, 5).forEach(log => {
        const item = document.createElement("li");
        item.className = "list-group-item";
        item.innerText = `User ${log.user_id} | ${log.action} | ${log.status} | ${log.timestamp}`;
        list.appendChild(item);
    });
}

window.assignUserRole = async function (userId) {
    const roleId = document.getElementById(`role-${userId}`).value;
    await assignRole(userId, roleId);
    await loadDashboard();
};
