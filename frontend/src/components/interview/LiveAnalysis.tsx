"use client";

import React from "react";
import { AlertTriangle, CheckCircle, Brain } from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface AnalysisData {
  time: string;
  confidence: number;
  sentiment: number;
}

interface LiveAnalysisProps {
  transcript: string;
  analysisData: AnalysisData[];
  score: number;
  alerts: string[];
}

export default function LiveAnalysis({
  transcript,
  analysisData,
  score,
  alerts,
}: LiveAnalysisProps) {
  return (
    <div className="h-full flex flex-col gap-4 bg-slate-900/50 p-4 rounded-2xl border border-slate-800 backdrop-blur-xl">
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <Brain className="w-5 h-5 text-indigo-400" />
          <h2 className="text-lg font-semibold text-white">
            AI Behavioral Analysis
          </h2>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-sm text-slate-400">Analysis Status:</span>
          {score > 0 ? (
            <span
              className={`text-xl font-bold ${
                score >= 70
                  ? "text-green-400"
                  : score >= 50
                  ? "text-yellow-400"
                  : "text-red-400"
              }`}
            >
              {score}/100
            </span>
          ) : (
            <span className="text-sm font-medium text-slate-500 bg-slate-800 px-2 py-1 rounded">
              Pending Final Review
            </span>
          )}
        </div>
      </div>

      {/* Real-time Transcription */}
      <div className="bg-slate-950/50 rounded-xl p-4 border border-slate-800 h-64 overflow-hidden flex flex-col">
        <span className="text-xs text-slate-500 uppercase font-bold tracking-wider mb-2">
          Candidate Responses
        </span>
        <div className="overflow-y-auto flex-1 scrollbar-hide">
          <p className="text-slate-300 text-sm leading-relaxed whitespace-pre-wrap">
            {transcript || "No responses yet..."}
          </p>
        </div>
      </div>

      {/* Charts */}
      <div className="flex-1 min-h-0 flex flex-col gap-4">
        <div className="bg-slate-950/50 rounded-xl p-4 border border-slate-800 flex-1 min-h-[150px]">
          <span className="text-xs text-slate-500 uppercase font-bold tracking-wider mb-2 block">
            Sentiment & Confidence Flow
          </span>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={analysisData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="time" hide />
              <YAxis domain={[0, 100]} hide />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#0f172a",
                  borderColor: "#334155",
                  color: "#f8fafc",
                }}
                itemStyle={{ fontSize: "12px" }}
              />
              <Line
                type="monotone"
                dataKey="confidence"
                stroke="#818cf8"
                strokeWidth={2}
                dot={false}
                animationDuration={300}
                name="Confidence"
              />
              <Line
                type="monotone"
                dataKey="sentiment"
                stroke="#34d399"
                strokeWidth={2}
                dot={false}
                animationDuration={300}
                name="Sentiment"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Live Alerts */}
        <div className="bg-slate-950/50 rounded-xl p-4 border border-slate-800 h-32 overflow-hidden flex flex-col">
          <span className="text-xs text-slate-500 uppercase font-bold tracking-wider mb-2 flex items-center justify-between">
            <span>Behavioral Anomalies</span>
            {alerts.length > 0 && (
              <span className="text-red-400 animate-pulse text-[10px]">
                ● Activity Detected
              </span>
            )}
          </span>
          <div className="space-y-2 overflow-y-auto">
            {alerts.length === 0 ? (
              <div className="flex items-center gap-2 text-slate-500 text-sm italic">
                {score === 0 ? (
                  <>
                    <Brain className="w-4 h-4 animate-pulse" />
                    <span>Analysis pending completion...</span>
                  </>
                ) : (
                  <>
                    <CheckCircle className="w-4 h-4" />
                    <span>No anomalies detected.</span>
                  </>
                )}
              </div>
            ) : (
              alerts.map((alert, idx) => (
                <div
                  key={idx}
                  className="flex items-center gap-2 p-2 rounded bg-red-500/10 border border-red-500/20 text-red-200 text-xs"
                >
                  <AlertTriangle className="w-3 h-3 text-red-400 shrink-0" />
                  <span>{alert}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
