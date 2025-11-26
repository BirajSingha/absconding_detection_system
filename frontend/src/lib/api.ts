import { Alert, AnalyticsData, Employee, AlertSummary } from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api";

async function fetchAPI<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    cache: "no-store",
    ...options,
  });
  if (!res.ok) {
    throw new Error(`API Error: ${res.statusText}`);
  }
  return res.json();
}

export const api = {
  employees: {
    list: async () => {
      const res = await fetchAPI<{ employees: Employee[] }>("/employees");
      return res.employees;
    },
    get: (id: string) => fetchAPI<Employee>(`/employees/${id}`),
  },
  alerts: {
    list: async (status?: string) => {
      const res = await fetchAPI<{ alerts: Alert[] }>(
        `/alerts${status ? `?status=${status}` : ""}`
      );
      return res.alerts;
    },
    get: (id: number) => fetchAPI<Alert>(`/alerts/${id}`),
    updateStatus: (id: number, status: string) =>
      fetchAPI<Alert>(`/alerts/${id}/status`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status }),
      }),
  },
  analytics: {
    getDashboardStats: () => fetchAPI<AnalyticsData>("/analytics/dashboard"),
    getAlertTrends: () =>
      fetchAPI<{ data: { date: string; count: number }[] }>(
        "/analytics/alert-trends"
      ),
    getAlertSummary: () => fetchAPI<AlertSummary>("/analytics/alert-summary"),
  },
};
