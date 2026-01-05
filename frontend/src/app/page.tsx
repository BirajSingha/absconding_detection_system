"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { AnalyticsData, AlertSummary } from "@/lib/types";
import { InterviewCard } from "@/components/dashboard/InterviewCard";
import { RiskDistribution } from "@/components/charts/RiskDistribution";
import Link from "next/link";
import { useHeader } from "@/context/HeaderContext";
import {
  Users,
  AlertTriangle,
  TrendingUp,
  Activity,
  Video,
} from "lucide-react";

export default function Dashboard() {
  const { setHeaderContent } = useHeader();
  const [stats, setStats] = useState<AnalyticsData | null>(null);
  const [summary, setSummary] = useState<AlertSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setHeaderContent(
      <div className="flex justify-between items-center w-full">
        <h2 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-cyan-600">
          Recruitment Dashboard
        </h2>
        <Link
          href="/interview"
          className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md transition-colors font-medium text-sm"
        >
          <Video className="w-4 h-4" />
          <span>Start New Interview</span>
        </Link>
      </div>
    );
    return () => setHeaderContent(null);
  }, [setHeaderContent]);

  useEffect(() => {
    const loadData = async () => {
      // ... rest of loadData logic
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
      {/* Header moved to Portal */}

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total Candidates"
          value={summary?.total_candidates?.toString() || "0"}
          icon={Users}
          trend={`${
            summary?.trends?.candidates && summary.trends.candidates > 0
              ? "+"
              : ""
          }${summary?.trends?.candidates || 0}%`}
          trendUp={(summary?.trends?.candidates || 0) >= 0}
        />
        <StatCard
          title="Pending Interviews"
          value={summary?.pending_interviews?.toString() || "0"}
          icon={AlertTriangle}
          trend={`${
            summary?.trends?.at_risk && summary.trends.at_risk > 0 ? "+" : ""
          }${summary?.trends?.at_risk || 0}%`}
          trendUp={false} // Pending is just pending, neutral
          alert={(summary?.pending_interviews || 0) > 10}
        />
        <StatCard
          title="Completed Interviews"
          value={summary?.completed_interviews?.toString() || "0"}
          icon={Activity}
          trend={`${
            summary?.trends?.resolved && summary.trends.resolved > 0 ? "+" : ""
          }${summary?.trends?.resolved || 0}%`}
          trendUp={(summary?.trends?.resolved || 0) >= 0}
        />
        <StatCard
          title="Avg Fit Score"
          value={summary?.average_fit_score?.toFixed(1) || "0"}
          icon={TrendingUp}
          trend={`${
            summary?.trends?.fit_score && summary.trends.fit_score > 0
              ? "+"
              : ""
          }${summary?.trends?.fit_score || 0}%`}
          trendUp={(summary?.trends?.fit_score || 0) >= 0}
        />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-slate-900">
            Fit Distribution
          </h3>
          {stats && <RiskDistribution data={stats.risk_distribution} />}
        </div>

        <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h3 className="mb-4 text-lg font-semibold text-slate-900">
            Recent Analysis
          </h3>
          <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2">
            {stats?.recent_alerts.map((analysis) => (
              <InterviewCard key={analysis.id} analysis={analysis} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

interface StatCardProps {
  title: string;
  value: string;
  icon: React.ElementType; // Lucide icon type
  trend: string;
  trendUp: boolean;
  alert?: boolean;
}

function StatCard({
  title,
  value,
  icon: Icon,
  trend,
  trendUp,
  alert,
}: StatCardProps) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">{title}</p>
          <p
            className={`mt-2 text-3xl font-bold ${
              alert ? "text-amber-600" : "text-slate-900"
            }`}
          >
            {value}
          </p>
        </div>
        <div
          className={`rounded-full p-3 ${
            alert
              ? "bg-amber-50 text-amber-600"
              : "bg-indigo-50 text-indigo-600"
          }`}
        >
          <Icon className="h-6 w-6" />
        </div>
      </div>
      <div className="mt-4 flex items-center text-sm">
        <span className={trendUp ? "text-green-600" : "text-slate-500"}>
          {trend}
        </span>
        <span className="ml-2 text-slate-500">from last month</span>
      </div>
    </div>
  );
}
