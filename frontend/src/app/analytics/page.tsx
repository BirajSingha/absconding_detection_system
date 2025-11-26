"use client";

import { useEffect, useState } from "react";
import { AnalyticsData } from "@/lib/types";
import { RiskDistribution } from "@/components/charts/RiskDistribution";
import { TrendsChart } from "@/components/charts/TrendsChart";
import { api } from "@/lib/api";

export default function AnalyticsPage() {
  const [stats, setStats] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [trendData, setTrendData] = useState<any[]>([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [dashboardData, trendsData] = await Promise.all([
        api.analytics.getDashboardStats().catch(() => null),
        api.analytics.getAlertTrends().catch(() => ({ data: [] })),
      ]);

      if (dashboardData) {
        setStats(dashboardData);
      }

      if (trendsData && trendsData.data) {
        setTrendData(trendsData.data);
      }
    } catch (error) {
      console.error("Failed to load dashboard data:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        Loading analytics...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-slate-900">Analytics Dashboard</h1>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-slate-900">
            Risk Distribution
          </h3>
          {stats && <RiskDistribution data={stats.risk_distribution} />}
        </div>

        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-slate-900">
            Alert Trends (Last 30 Days)
          </h3>
          <TrendsChart data={trendData} />
        </div>
      </div>
    </div>
  );
}
