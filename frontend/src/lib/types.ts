export interface Candidate {
  id: number;
  candidate_id: string;
  name: string;
  email: string;
  phone?: string | null;
  position_applied: string;
  department: string;
  interview_date: string;
  status: "PENDING" | "INTERVIEWED" | "HIRED" | "REJECTED";
  fit_score: number;
  fit_category: "LOW" | "MEDIUM" | "HIGH" | "EXCELLENT";
}

export interface InterviewAnalysis {
  id: number;
  candidate_id: string;
  fit_score: number;
  fit_category: "LOW" | "MEDIUM" | "HIGH" | "EXCELLENT";
  confidence_score: number;
  tone_analysis: {
    confidence: number;
    nervousness: number;
    professionalism: number;
    tone_label: string;
  };
  behavioral_traits: Record<string, number>;
  ai_summary: string;
  recommendations: string[];
  created_at: string;
}

export interface AnalyticsData {
  risk_distribution: { name: string; value: number; color: string }[]; // Keeping for now, maybe rename to 'fit_distribution' later
  department_risk: { name: string; high_risk_count: number }[];
  top_risk_employees: Candidate[]; // TODO: Rename on backend to top_candidates
  recent_alerts: InterviewAnalysis[];
}

export interface AlertSummary {
  total_candidates: number;
  total_interviews: number;
  pending_interviews: number;
  completed_interviews: number;
  average_fit_score: number;
  status_breakdown: Record<string, number>;
  trends: {
    candidates: number;
    fit_score: number;
    resolved?: number;
    at_risk?: number;
  };
}
