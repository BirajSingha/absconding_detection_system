"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { analysisService } from "@/services/api";

export default function AnalysisPage() {
  const searchParams = useSearchParams();
  const candidateId = searchParams.get("id");

  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!candidateId) {
      setError("No candidate ID provided");
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      try {
        const data = await analysisService.getCandidateAnalysis(candidateId);
        if (data && data.length > 0) {
          setAnalysis(data[0]); // Get latest analysis
        } else {
          setError("No analysis found for this candidate");
        }
      } catch (err) {
        console.error(err);
        setError("Failed to load analysis report");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [candidateId]);

  if (loading)
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-white">
        Loading Report...
      </div>
    );
  if (error)
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-red-400">
        {error}
      </div>
    );
  if (!analysis)
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-white">
        No data available
      </div>
    );

  // Parse Risk Data
  const riskData = analysis.behavioral_traits?.absconding_risk || {
    exit_probability: 0,
    risk_level: "UNKNOWN",
    key_indicators: [],
  };

  // Determine color based on risk
  const riskColor =
    riskData.risk_level === "HIGH"
      ? "text-red-500"
      : riskData.risk_level === "MEDIUM"
        ? "text-yellow-500"
        : "text-green-500";

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 p-8 font-sans">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex justify-between items-end border-b border-slate-800 pb-6">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">
              Interview Analysis Report
            </h1>
            <p className="text-slate-400">
              Candidate ID:{" "}
              <span className="text-slate-200">{analysis.candidate_id}</span>
            </p>
          </div>
          <div className="text-right">
            <div className="text-sm text-slate-500">Analysis Date</div>
            <div className="text-slate-300">
              {new Date(analysis.created_at).toLocaleDateString()}
            </div>
          </div>
        </div>

        {/* Score Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Fit Score */}
          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800 relative overflow-hidden">
            <h3 className="text-sm uppercase tracking-wider text-slate-500 mb-2">
              Fit Score
            </h3>
            <div className="text-4xl font-bold text-white">
              {Math.round(analysis.fit_score)}%
            </div>
            <div
              className={`text-sm mt-1 font-medium ${
                analysis.fit_category === "HIGH"
                  ? "text-green-400"
                  : analysis.fit_category === "LOW"
                    ? "text-red-400"
                    : "text-yellow-400"
              }`}
            >
              {analysis.fit_category} FIT
            </div>
          </div>

          {/* Exit Probability */}
          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
            <h3 className="text-sm uppercase tracking-wider text-slate-500 mb-2">
              Absconding Risk
            </h3>
            <div className="text-4xl font-bold text-white">
              {riskData.exit_probability}%
            </div>
            <div className={`text-sm mt-1 font-medium ${riskColor}`}>
              {riskData.risk_level} RISK
            </div>
          </div>

          {/* Overall Confidence */}
          <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
            <h3 className="text-sm uppercase tracking-wider text-slate-500 mb-2">
              AI Confidence
            </h3>
            <div className="text-4xl font-bold text-white">
              {analysis.tone_analysis?.confidence
                ? Math.round(analysis.tone_analysis.confidence * 10)
                : 85}
              %
            </div>
            <div className="text-sm mt-1 text-slate-400 font-medium">
              Based on Tone Analysis
            </div>
          </div>
        </div>

        {/* AI Summary */}
        <div className="bg-slate-900 p-8 rounded-xl border border-slate-800 shadow-xl shadow-black/20">
          <h2 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
            <span className="w-1 h-6 bg-blue-500 rounded-full"></span>
            AI Executive Summary
          </h2>
          <p className="text-slate-300 leading-relaxed text-lg">
            {analysis.ai_summary}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Risk Indicators */}
          <div className="bg-slate-900/50 p-6 rounded-xl border border-slate-800">
            <h3 className="text-lg font-semibold text-red-400 mb-4">
              Risk Indicators
            </h3>
            {riskData.key_indicators?.length > 0 ? (
              <ul className="space-y-3">
                {riskData.key_indicators.map((indicator: string, i: number) => (
                  <li
                    key={i}
                    className="flex items-start gap-3 bg-red-950/20 p-3 rounded-lg border border-red-900/10"
                  >
                    <span className="text-red-500 mt-1">⚠</span>
                    <span className="text-slate-300">
                      {indicator.replace(/_/g, " ")}
                    </span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-slate-500 italic">
                No significant risk indicators detected.
              </p>
            )}
          </div>

          {/* Recommendations */}
          <div className="bg-slate-900/50 p-6 rounded-xl border border-slate-800">
            <h3 className="text-lg font-semibold text-blue-400 mb-4">
              Recommendations
            </h3>
            {analysis.recommendations?.length > 0 ? (
              <ul className="space-y-3">
                {analysis.recommendations.map((rec: string, i: number) => (
                  <li
                    key={i}
                    className="flex items-start gap-3 bg-blue-950/20 p-3 rounded-lg border border-blue-900/10"
                  >
                    <span className="text-blue-500 mt-1">✓</span>
                    <span className="text-slate-300">{rec}</span>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-slate-500 italic">
                No recommendations available.
              </p>
            )}
          </div>
        </div>

        {/* Behavioral Traits */}
        <div className="bg-slate-900 p-6 rounded-xl border border-slate-800">
          <h3 className="text-lg font-semibold text-white mb-6">
            Behavioral Traits
          </h3>
          <div className="flex flex-wrap gap-3">
            {Object.entries(analysis.behavioral_traits || {})
              .filter(([key]) => key !== "absconding_risk") // Filter out our injected data
              .map(([trait, value], i) => (
                <div
                  key={i}
                  className="px-4 py-2 bg-slate-800 rounded-full border border-slate-700 text-slate-300 text-sm"
                >
                  <span className="font-medium text-slate-100 capitalize">
                    {trait.replace(/_/g, " ")}
                  </span>
                  : {String(value)}
                </div>
              ))}
          </div>
        </div>
      </div>
    </div>
  );
}
