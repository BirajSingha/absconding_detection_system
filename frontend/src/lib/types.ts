export interface Employee {
  employee_id: string;
  name: string;
  email: string;
  role: string;
  department: string;
  tenure_years: number;
  risk_score: number;
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  attendance_percentage: number;
  productivity_score: number;
  performance_rating: number;
  employment_status: string;
}

export interface Alert {
  id: number;
  employee_id: string;
  employee_name: string;
  risk_score: number;
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  status: "OPEN" | "ACKNOWLEDGED" | "RESOLVED";
  created_at: string;
  behavioral_indicators: (
    | string
    | { description: string; [key: string]: any }
  )[];
  sentiment_analysis: any;
}

export interface AnalyticsData {
  risk_distribution: { name: string; value: number; color: string }[];
  department_risk: { name: string; high_risk_count: number }[];
  top_risk_employees: Employee[];
  recent_alerts: Alert[];
}

export interface AlertSummary {
  total_employees: number;
  total_alerts: number;
  open_alerts: number;
  resolved_alerts: number;
  average_risk_score: number;
  status_breakdown: Record<string, number>;
  trends: {
    employees: number;
    at_risk: number;
    resolved: number;
    risk_score: number;
  };
}
