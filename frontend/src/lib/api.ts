import {
  InterviewAnalysis,
  AnalyticsData,
  Candidate,
  AlertSummary,
} from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api";

async function fetchAPI<T>(
  endpoint: string,
  options?: RequestInit,
): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    cache: "no-store",
    ...options,
  });
  if (!res.ok) {
    throw new Error(`API Error: ${res.statusText}`);
  }
  return res.json();
}

export const api = {
  candidates: {
    list: async () => {
      const res = await fetchAPI<Candidate[]>("/candidates");
      return res; // Candidates endpoint now returns array directly
    },
    get: (id: string) => fetchAPI<Candidate>(`/candidates/${id}`),
    create: (data: any) =>
      fetchAPI<Candidate>("/candidates", {
        method: "POST",
        body: JSON.stringify(data),
        headers: { "Content-Type": "application/json" },
      }),
  },
  analysis: {
    analyze: (
      candidateId: string,
      transcript: string,
      candidateName?: string,
    ) =>
      fetchAPI<InterviewAnalysis>("/analysis/analyze-interview", {
        method: "POST",
        body: JSON.stringify({
          candidate_id: candidateId,
          transcript_text: transcript,
          candidate_name: candidateName,
        }),
        headers: { "Content-Type": "application/json" },
      }),
    getByCandidate: (candidateId: string) =>
      fetchAPI<InterviewAnalysis[]>(`/analysis/candidate/${candidateId}`),
  },
  analytics: {
    getDashboardStats: () => fetchAPI<AnalyticsData>("/analytics/dashboard"),
    getAlertSummary: async () => {
      const res = await fetchAPI<AlertSummary>("/analytics/alert-summary");
      return res;
    },
  },
};
