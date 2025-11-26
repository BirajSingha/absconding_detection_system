"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Alert } from "@/lib/types";
import { AlertCard } from "@/components/dashboard/AlertCard";

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadAlerts = async () => {
      try {
        const data = await api.alerts.list();
        setAlerts(data || []);
      } catch (error) {
        console.error("Failed to load alerts:", error);
      } finally {
        setLoading(false);
      }
    };

    loadAlerts();
  }, []);

  const handleStatusUpdate = async (id: number, status: string) => {
    // Optimistic update
    setAlerts(
      alerts.map((a) => (a.id === id ? { ...a, status: status as any } : a))
    );
    try {
      await api.alerts.updateStatus(id, status);
    } catch (error) {
      console.error("Failed to update status:", error);
      // Revert on error
      // In a real app, we'd reload data or show a toast
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Risk Alerts</h1>

      {loading ? (
        <div className="flex h-64 items-center justify-center">
          Loading alerts...
        </div>
      ) : (
        <div className="space-y-4">
          {alerts.map((alert) => (
            <AlertCard
              key={alert.id}
              alert={alert}
              onStatusUpdate={handleStatusUpdate}
            />
          ))}
        </div>
      )}
    </div>
  );
}
