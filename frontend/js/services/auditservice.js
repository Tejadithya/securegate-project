import { request } from "../api/api.js";

export const getAuditLogs = () => request("/audit-logs");
