"use client";

import { cn } from "@/lib/utils";

interface RiskMeterProps {
  score: number;
  size?: "sm" | "md" | "lg";
}

export function RiskMeter({ score, size = "md" }: RiskMeterProps) {
  const percentage = Math.min(Math.max(score, 0), 100);

  const getColor = (s: number) => {
    if (s >= 80) return "text-red-600";
    if (s >= 60) return "text-orange-500";
    if (s >= 40) return "text-yellow-500";
    return "text-green-500";
  };

  const sizes = {
    sm: "h-16 w-16 text-xs",
    md: "h-24 w-24 text-sm",
    lg: "h-32 w-32 text-base",
  };

  const strokeWidth = size === "sm" ? 8 : 10;
  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (percentage / 100) * circumference;

  return (
    <div className="relative flex flex-col items-center justify-center">
      <svg
        className={cn("transform -rotate-90", sizes[size])}
        viewBox="0 0 100 100"
      >
        {/* Background circle */}
        <circle
          className="text-slate-200"
          strokeWidth={strokeWidth}
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx="50"
          cy="50"
        />
        {/* Progress circle */}
        <circle
          className={getColor(score)}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          stroke="currentColor"
          fill="transparent"
          r={radius}
          cx="50"
          cy="50"
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className={cn("font-bold", getColor(score))}>{score}</span>
      </div>
    </div>
  );
}
