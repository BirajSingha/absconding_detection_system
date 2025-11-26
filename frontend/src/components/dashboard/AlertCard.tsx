"use client";

import { Alert } from "@/lib/types";
import { AlertTriangle, CheckCircle, Clock } from "lucide-react";
import { cn } from "@/lib/utils";

interface AlertCardProps {
  alert: Alert;
  onStatusUpdate?: (id: number, status: string) => void;
}

export function AlertCard({ alert, onStatusUpdate }: AlertCardProps) {
  const riskColors = {
    CRITICAL: "bg-red-50 border-red-200 text-red-700",
    HIGH: "bg-orange-50 border-orange-200 text-orange-700",
    MEDIUM: "bg-yellow-50 border-yellow-200 text-yellow-700",
    LOW: "bg-green-50 border-green-200 text-green-700",
  };

  const statusColors = {
    OPEN: "bg-red-100 text-red-800",
    ACKNOWLEDGED: "bg-yellow-100 text-yellow-800",
    RESOLVED: "bg-green-100 text-green-800",
  };

  return (
    <div
      className={cn(
        "rounded-lg border p-4 shadow-sm",
        riskColors[alert.risk_level]
      )}
    >
      <div className="flex items-start justify-between">
        <div className="flex items-center space-x-3">
          <AlertTriangle className="h-5 w-5" />
          <div>
            <h3 className="font-semibold">{alert.employee_name}</h3>
            <p className="text-sm opacity-90">
              Risk Score: {alert.risk_score}/100
            </p>
          </div>
        </div>
        <span
          className={cn(
            "rounded-full px-2 py-1 text-xs font-medium",
            statusColors[alert.status]
          )}
        >
          {alert.status}
        </span>
      </div>

      <div className="mt-3">
        <p className="text-sm font-medium">Indicators:</p>
        <ul className="mt-1 list-inside list-disc text-sm opacity-80">
          {alert.behavioral_indicators.slice(0, 2).map((indicator, idx) => (
            <li key={idx}>
              {typeof indicator === "string"
                ? indicator
                : indicator.description}
            </li>
          ))}
        </ul>
      </div>

      <div className="mt-4 flex justify-end space-x-2">
        {alert.status === "OPEN" && (
          <button
            onClick={() => onStatusUpdate?.(alert.id, "ACKNOWLEDGED")}
            className="flex items-center rounded-md bg-white px-3 py-1 text-xs font-medium shadow-sm hover:bg-gray-50"
          >
            <Clock className="mr-1 h-3 w-3" /> Acknowledge
          </button>
        )}
        {alert.status !== "RESOLVED" && (
          <button
            onClick={() => onStatusUpdate?.(alert.id, "RESOLVED")}
            className="flex items-center rounded-md bg-white px-3 py-1 text-xs font-medium shadow-sm hover:bg-gray-50"
          >
            <CheckCircle className="mr-1 h-3 w-3" /> Resolve
          </button>
        )}
      </div>
    </div>
  );
}
