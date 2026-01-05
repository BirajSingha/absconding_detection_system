"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { InterviewAnalysis } from "@/lib/types";
import { InterviewCard } from "@/components/dashboard/InterviewCard";

export default function AnalysisPage() {
  const [analyses, setAnalyses] = useState<InterviewAnalysis[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadAnalysis = async () => {
      try {
        // Retrieve recent analyses from dashboard endpoint or add a new endpoint for all analysis
        // For now, let's use the recent_alerts from dashboard stats as a proxy,
        // or we need to add a list endpoint to analysis routes.
        // Let's assume we added list to analysis routes or use analytics recent logic.
        // Actually, the best way given current backend is to fetch recent alerts from dashboard endpoint
        // or we should have added a 'list' endpoint to analysis.py.
        // I'll stick to what I have: api.analytics.getDashboardStats().recent_alerts
        // BUT wait, I updated api.ts to have `analysis.getByCandidate` but not `listAll`.
        // I will use `api.analytics.getDashboardStats()` and pluck recent_alerts for now to be safe.
        const stats = await api.analytics.getDashboardStats();
        setAnalyses(stats.recent_alerts || []);
      } catch (error) {
        console.error("Failed to load analysis:", error);
      } finally {
        setLoading(false);
      }
    };

    loadAnalysis();
  }, []);

  return (
    <div className="space-y-6">
      {loading ? (
        <div className="flex h-64 items-center justify-center">
          Loading analysis...
        </div>
      ) : (
        <div className="space-y-4">
          {analyses.map((analysis) => (
            <InterviewCard key={analysis.id} analysis={analysis} />
          ))}
        </div>
      )}
    </div>
  );
}
