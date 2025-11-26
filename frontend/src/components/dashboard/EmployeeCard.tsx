"use client";

import { Employee } from "@/lib/types";
import { RiskMeter } from "./RiskMeter";
import { MoreVertical } from "lucide-react";

interface EmployeeCardProps {
  employee: Employee;
}

export function EmployeeCard({ employee }: EmployeeCardProps) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md">
      <div className="flex items-start justify-between">
        <div className="flex items-center space-x-3">
          <div className="h-10 w-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 font-semibold">
            {employee.name.charAt(0)}
          </div>
          <div>
            <h3 className="font-medium text-slate-900">{employee.name}</h3>
            <p className="text-sm text-slate-500">{employee.role}</p>
          </div>
        </div>
        <button className="text-slate-400 hover:text-slate-600">
          <MoreVertical className="h-5 w-5" />
        </button>
      </div>

      <div className="mt-4 flex items-center justify-between border-t border-slate-100 pt-4">
        <div className="text-sm">
          <p className="text-slate-500">Department</p>
          <p className="font-medium text-slate-900">{employee.department}</p>
        </div>
        <div className="flex items-center space-x-2">
          <div className="text-right">
            <p className="text-xs text-slate-500">Risk Score</p>
            <p
              className={`font-bold ${
                employee.risk_score >= 60 ? "text-red-600" : "text-green-600"
              }`}
            >
              {employee.risk_score}/100
            </p>
          </div>
          <RiskMeter score={employee.risk_score} size="sm" />
        </div>
      </div>
    </div>
  );
}
