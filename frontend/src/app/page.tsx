"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Alert, AnalyticsData, AlertSummary } from "@/lib/types";
import { AlertCard } from "@/components/dashboard/AlertCard";
import { RiskDistribution } from "@/components/charts/RiskDistribution";
import { Users, AlertTriangle, TrendingUp, Activity } from "lucide-react";

export default function Dashboard() {
  const [stats, setStats] = useState<AnalyticsData | null>(null);
  const [summary, setSummary] = useState<AlertSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [dashboardData, summaryData] = await Promise.all([
          api.analytics.getDashboardStats().catch(() => null),
          api.analytics.getAlertSummary().catch(() => null),
        ]);

        if (dashboardData) {
          setStats(dashboardData);
        }

        if (summaryData) {
          setSummary(summaryData);
        }
      } catch (error) {
        console.error("Failed to load dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        Loading dashboard...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total Employees"
          value={summary?.total_employees.toString() || "0"}
          icon={Users}
          trend={`${
            summary?.trends?.employees && summary.trends.employees > 0
              ? "+"
              : ""
          }${summary?.trends?.employees || 0}%`}
          trendUp={(summary?.trends?.employees || 0) >= 0}
        />
        <StatCard
          title="At Risk Employees"
          value={summary?.open_alerts.toString() || "0"}
          icon={AlertTriangle}
          trend={`${
            summary?.trends?.at_risk && summary.trends.at_risk > 0 ? "+" : ""
          }${summary?.trends?.at_risk || 0}%`}
          trendUp={(summary?.trends?.at_risk || 0) <= 0} // Lower is better for risk
          alert={summary?.open_alerts && summary.open_alerts > 0}
        />
        <StatCard
          title="Resolved Alerts"
          value={summary?.resolved_alerts.toString() || "0"}
          icon={Activity}
          trend={`${
            summary?.trends?.resolved && summary.trends.resolved > 0 ? "+" : ""
          }${summary?.trends?.resolved || 0}%`}
          trendUp={(summary?.trends?.resolved || 0) >= 0}
        />
        <StatCard
          title="Avg Risk Score"
          value={summary?.average_risk_score.toFixed(1) || "0"}
          icon={TrendingUp}
          trend={`${
            summary?.trends?.risk_score && summary.trends.risk_score > 0
              ? "+"
              : ""
          }${summary?.trends?.risk_score || 0}%`}
          trendUp={(summary?.trends?.risk_score || 0) <= 0} // Lower is better for risk score
        />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-slate-900">
            Risk Distribution
          </h3>
          {stats && <RiskDistribution data={stats.risk_distribution} />}
        </div>

        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-slate-900">
            Recent High Risk Alerts
          </h3>
          <div className="space-y-4">
            {stats?.recent_alerts.map((alert) => (
              <AlertCard key={alert.id} alert={alert} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon: Icon, trend, trendUp, alert }: any) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">{title}</p>
          <p
            className={`mt-2 text-3xl font-bold ${
              alert ? "text-red-600" : "text-slate-900"
            }`}
          >
            {value}
          </p>
        </div>
        <div
          className={`rounded-full p-3 ${
            alert ? "bg-red-50 text-red-600" : "bg-indigo-50 text-indigo-600"
          }`}
        >
          <Icon className="h-6 w-6" />
        </div>
      </div>
      <div className="mt-4 flex items-center text-sm">
        <span className={trendUp ? "text-green-600" : "text-red-600"}>
          {trend}
        </span>
        <span className="ml-2 text-slate-500">from last month</span>
      </div>
    </div>
  );
}
