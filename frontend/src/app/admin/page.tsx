"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { candidatesService } from "@/services/api";

interface Candidate {
  id: number;
  candidate_id: string;
  name: string;
  position_applied: string;
  status: string;
  fit_score: number;
  fit_category: string;
  updated_at: string;
}

export default function AdminDashboard() {
  const router = useRouter();
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCandidates = async () => {
      try {
        const data = await candidatesService.getAll();
        // Filter only candidates who have been analyzed (used the chatbot)
        const analyzedCandidates = data.filter(
          (c: Candidate) => c.fit_category !== "UNKNOWN",
        );
        setCandidates(analyzedCandidates);
      } catch (err) {
        console.error("Failed to fetch candidates", err);
      } finally {
        setLoading(false);
      }
    };

    fetchCandidates();
  }, []);

  if (loading)
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-white">
        Loading Dashboard...
      </div>
    );

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 p-8 font-sans">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8 border-b border-slate-800 pb-6">
          <div>
            <h1 className="text-3xl font-bold text-white">
              Candidate Dashboard
            </h1>
            <p className="text-slate-400 mt-1">Review AI-analyzed interviews</p>
          </div>
          <div className="bg-slate-900 px-4 py-2 rounded-lg border border-slate-800">
            <span className="text-slate-400 text-sm">Total Analyzed:</span>
            <span className="ml-2 text-xl font-bold text-white">
              {candidates.length}
            </span>
          </div>
        </div>

        {candidates.length === 0 ? (
          <div className="text-center py-20 bg-slate-900 rounded-xl border border-slate-800 border-dashed">
            <p className="text-slate-500 text-lg">
              No candidates have completed the interview yet.
            </p>
          </div>
        ) : (
          <div className="bg-slate-900 rounded-xl border border-slate-800 overflow-hidden shadow-xl">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-950/50 text-slate-400 text-sm uppercase tracking-wider border-b border-slate-800">
                  <th className="p-6 font-medium">Candidate</th>
                  <th className="p-6 font-medium">Role</th>
                  <th className="p-6 font-medium">Status</th>
                  <th className="p-6 font-medium">Fit Score</th>
                  <th className="p-6 font-medium text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {candidates.map((candidate) => (
                  <tr
                    key={candidate.id}
                    className="hover:bg-slate-800/50 transition-colors cursor-pointer group"
                    onClick={() =>
                      router.push(`/analysis?id=${candidate.candidate_id}`)
                    }
                  >
                    <td className="p-6">
                      <div className="font-semibold text-white group-hover:text-blue-400 transition-colors">
                        {candidate.name}
                      </div>
                      <div className="text-xs text-slate-500 font-mono mt-1">
                        {candidate.candidate_id}
                      </div>
                    </td>
                    <td className="p-6 text-slate-300">
                      {candidate.position_applied}
                    </td>
                    <td className="p-6">
                      <span className="px-3 py-1 bg-slate-800 rounded-full text-xs font-medium text-slate-300 border border-slate-700">
                        {candidate.status}
                      </span>
                    </td>
                    <td className="p-6">
                      <div className="flex items-center gap-3">
                        <div
                          className={`text-lg font-bold ${
                            candidate.fit_category === "HIGH"
                              ? "text-green-400"
                              : candidate.fit_category === "LOW"
                                ? "text-red-400"
                                : "text-yellow-400"
                          }`}
                        >
                          {Math.round(candidate.fit_score)}%
                        </div>
                        <div className="text-xs text-slate-500 uppercase">
                          {candidate.fit_category}
                        </div>
                      </div>
                    </td>
                    <td className="p-6 text-right">
                      <button
                        className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium rounded-lg transition-colors shadow-lg shadow-blue-900/20"
                        onClick={(e) => {
                          e.stopPropagation();
                          router.push(`/analysis?id=${candidate.candidate_id}`);
                        }}
                      >
                        View Report
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
