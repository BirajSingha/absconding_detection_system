"use client";

import { useEffect, useState, useMemo } from "react";
import { api } from "@/lib/api";
import { Candidate } from "@/lib/types";
import { CandidateCard } from "@/components/dashboard/CandidateCard";
import { Search, Filter } from "lucide-react";
import { useHeader } from "@/context/HeaderContext";

// Define outside to remain stable
const CandidatesHeader = ({
  onSearch,
  onFilter,
}: {
  onSearch: (term: string) => void;
  onFilter: (filter: string) => void;
}) => (
  <div className="flex justify-between items-center w-full">
    <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-cyan-600">
      Candidates
    </h1>

    <div className="flex w-full flex-col space-y-4 md:w-auto md:flex-row md:space-x-4 md:space-y-0 text-sm">
      <div className="relative w-full md:w-56">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
        <input
          type="text"
          placeholder="Search..."
          className="h-9 w-full rounded-md border border-slate-200 bg-slate-50 pl-9 pr-4 text-slate-900 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          // Uncontrolled input to prevent focus loss during context updates
          onChange={(e) => onSearch(e.target.value)}
        />
      </div>

      <div className="relative w-full md:w-48">
        <Filter className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
        <select
          className="h-9 w-full rounded-md border border-slate-200 bg-slate-50 pl-9 pr-8 text-slate-900 focus:border-indigo-500 focus:outline-none appearance-none focus:ring-1 focus:ring-indigo-500"
          defaultValue="ALL"
          onChange={(e) => onFilter(e.target.value)}
        >
          <option value="ALL" className="bg-white text-slate-900">
            All Categories
          </option>
          <option value="EXCELLENT" className="bg-white text-slate-900">
            Excellent Fit
          </option>
          <option value="HIGH" className="bg-white text-slate-900">
            High Fit
          </option>
          <option value="MEDIUM" className="bg-white text-slate-900">
            Medium Fit
          </option>
          <option value="LOW" className="bg-white text-slate-900">
            Low Fit
          </option>
        </select>
      </div>
    </div>
  </div>
);

export default function CandidatesPage() {
  const { setHeaderContent } = useHeader();
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [filter, setFilter] = useState("ALL");

  // Memoize header to prevent re-renders and focus loss
  const headerElement = useMemo(
    () => <CandidatesHeader onSearch={setSearchTerm} onFilter={setFilter} />,
    []
  );

  useEffect(() => {
    setHeaderContent(headerElement);
    return () => setHeaderContent(null);
  }, [setHeaderContent, headerElement]);

  useEffect(() => {
    const loadCandidates = async () => {
      try {
        const data = await api.candidates.list();
        setCandidates(data || []);
      } catch (error) {
        console.error("Failed to load candidates:", error);
      } finally {
        setLoading(false);
      }
    };

    loadCandidates();
  }, []);

  const filteredCandidates = candidates.filter((cand) => {
    const matchesSearch =
      cand.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      cand.position_applied.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filter === "ALL" || cand.fit_category === filter;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="space-y-6">
      {/* Header moved to Portal */}

      {loading ? (
        <div className="flex h-64 items-center justify-center">
          Loading candidates...
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {filteredCandidates.map((candidate) => (
            <CandidateCard key={candidate.candidate_id} candidate={candidate} />
          ))}
        </div>
      )}
    </div>
  );
}
