"use client";

import { InterviewAnalysis } from "@/lib/types";
import { ClipboardCheck, CheckCircle, Clock } from "lucide-react";
import { cn } from "@/lib/utils";

interface InterviewCardProps {
  analysis: InterviewAnalysis;
}

export function InterviewCard({ analysis }: InterviewCardProps) {
  const fitColors = {
    EXCELLENT: "bg-green-50 border-green-200 text-green-700",
    HIGH: "bg-teal-50 border-teal-200 text-teal-700",
    MEDIUM: "bg-yellow-50 border-yellow-200 text-yellow-700",
    LOW: "bg-red-50 border-red-200 text-red-700",
  };

  return (
    <div
      className={cn(
        "rounded-lg border p-4 shadow-sm",
        fitColors[analysis.fit_category]
      )}
    >
      <div className="flex items-start justify-between">
        <div className="flex items-center space-x-3">
          <ClipboardCheck className="h-5 w-5" />
          <div>
            <h3 className="font-semibold">
              Candidate: {analysis.candidate_id}
            </h3>
            <p className="text-sm opacity-90">
              Fit Score: {analysis.fit_score}/100
            </p>
          </div>
        </div>
        <span
          className={cn(
            "rounded-full px-2 py-1 text-xs font-medium bg-white/50"
          )}
        >
          {analysis.fit_category}
        </span>
      </div>

      <div className="mt-3">
        <p className="text-sm font-medium">Traits:</p>
        <div className="flex flex-wrap gap-2 mt-1">
          {Object.entries(analysis.behavioral_traits)
            .slice(0, 3)
            .map(([trait, score]) => (
              <span
                key={trait}
                className="text-xs bg-white/60 px-1.5 py-0.5 rounded"
              >
                {trait}: {score}
              </span>
            ))}
        </div>
      </div>

      <div className="mt-3">
        <p className="text-sm opacity-80 italic line-clamp-2">
          "{analysis.ai_summary}"
        </p>
      </div>
    </div>
  );
}
