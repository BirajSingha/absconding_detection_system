"use client";

import React, { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import QuestionPanel from "@/components/interview/QuestionPanel";
import LiveAnalysis from "@/components/interview/LiveAnalysis";
import { api } from "@/lib/api";
import { INTERVIEW_QUESTIONS } from "@/lib/questions";
import { useHeader } from "@/context/HeaderContext";

export default function InterviewPage() {
  const { setHeaderContent } = useHeader();
  const searchParams = useSearchParams();
  const candidateIdParam = searchParams.get("candidateId");

  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [score, setScore] = useState(0);
  const [alerts, setAlerts] = useState<string[]>([]);
  const [chartData, setChartData] = useState<
    { time: string; confidence: number; sentiment: number }[]
  >([{ time: "00:00", confidence: 50, sentiment: 50 }]);
  const [sessionComplete, setSessionComplete] = useState(false);

  // Generate candidateId only on client to avoid hydration mismatch
  const [candidateId, setCandidateId] = useState(candidateIdParam || "");

  useEffect(() => {
    if (!candidateIdParam) {
      setCandidateId("C_SESSION_" + Math.floor(Math.random() * 1000));
    }
  }, [candidateIdParam]);

  // Analyze individual answer
  const analyzeAnswer = async (
    questionId: string,
    answer: string,
    allAnswers: Record<string, string>
  ) => {
    if (!answer.trim()) return;

    try {
      // Find question text
      const question = INTERVIEW_QUESTIONS.find((q) => q.id === questionId);
      const formattedText = `Q: ${question?.text}\nA: ${answer}`;

      // Update transcript
      setTranscript((prev) => {
        const newTranscript = prev + "\n\n" + formattedText;
        return newTranscript.slice(-2000); // Keep last 2000 chars
      });

      // OPTIMIZATION: Skip per-answer analysis to save API validation quota.
      // Only running final analysis at the end.
      /* 
      const result = await api.analysis.analyze(candidateId, formattedText);

      if (result) {
        // Update score
        setScore(Math.round(result.fit_score || 0));

        // Update chart
        setChartData((prev) => {
          const newData = [
            ...prev,
            {
              time: new Date().toLocaleTimeString(),
              confidence: (result.tone_analysis?.confidence || 5) * 10,
              sentiment: (result.tone_analysis?.professionalism || 5) * 10,
            },
          ];
          if (newData.length > 20) newData.shift();
          return newData;
        });

        // Check for alerts
        const newAlerts: string[] = [];
        if (result.tone_analysis?.nervousness > 6) {
          newAlerts.push("High Nervousness Detected");
        }
        if (result.tone_analysis?.tone_label === "Hesitant") {
          newAlerts.push("Hesitant Response Pattern");
        }
        if (result.fit_category === "LOW") {
          newAlerts.push("⚠️ High Absconding Risk");
        }

        // Check for risk indicators in answer
        const riskIndicators = question?.riskIndicators || [];
        const answerLower = answer.toLowerCase();
        riskIndicators.forEach((indicator) => {
          if (answerLower.includes(indicator.toLowerCase())) {
            newAlerts.push(`Risk indicator: "${indicator}"`);
          }
        });

        if (newAlerts.length > 0) {
          setAlerts((prev) => [...newAlerts, ...prev].slice(0, 10));
        }
      }
      */
    } catch (error) {
      console.error("Analysis failed:", error);
    }
  };

  // Handle session complete
  const handleSessionComplete = async (allAnswers: Record<string, string>) => {
    setSessionComplete(true);

    // Build full transcript
    const fullTranscript = INTERVIEW_QUESTIONS.map((q) => {
      const answer = allAnswers[q.id] || "No answer";
      return `Q: ${q.text}\nA: ${answer}`;
    }).join("\n\n");

    // Final analysis with full transcript
    try {
      const result = await api.analysis.analyze(candidateId, fullTranscript);
      if (result) {
        setScore(Math.round(result.fit_score || 0));

        // Update chart with final overall metrics
        setChartData((prev) => [
          ...prev,
          {
            time: "Final",
            confidence: (result.tone_analysis?.confidence || 5) * 10,
            sentiment: (result.tone_analysis?.professionalism || 5) * 10,
          },
        ]);

        // Final alerts
        const finalAlerts: string[] = [];

        if (result.fit_category === "LOW") {
          finalAlerts.push("🚨 HIGH ABSCONDING RISK - HR Review Required");
        } else if (result.fit_category === "MEDIUM") {
          finalAlerts.push("⚠️ Moderate Risk - Monitor closely");
        }

        if (result.tone_analysis?.nervousness > 6) {
          finalAlerts.push("High Nervousness Detected");
        }
        if (result.tone_analysis?.tone_label === "Hesitant") {
          finalAlerts.push("Hesitant Response Pattern");
        }

        // Scan for specific high-risk keywords in answers
        INTERVIEW_QUESTIONS.forEach((q) => {
          const answer = allAnswers[q.id]?.toLowerCase() || "";
          if (!answer) return;

          q.riskIndicators.forEach((indicator) => {
            if (answer.includes(indicator.toLowerCase())) {
              finalAlerts.push(`Risk indicator detected: "${indicator}"`);
            }
          });
        });

        // Deduplicate
        const uniqueAlerts = Array.from(new Set(finalAlerts));

        if (uniqueAlerts.length > 0) {
          setAlerts((prev) => [...uniqueAlerts, ...prev]);
        }
      }
    } catch (error) {
      console.error("Final analysis failed:", error);
    }
  };

  const startSession = () => {
    setIsAnalyzing(true);
  };

  const stopSession = () => {
    setIsAnalyzing(false);
  };

  // Sync Header Content
  useEffect(() => {
    setHeaderContent(
      <div className="flex justify-between items-center w-full">
        <div>
          <h1 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-cyan-600">
            Absconding Risk Interview
          </h1>
          <p className="text-slate-500 text-xs flex items-center gap-2 font-mono mt-1">
            <span className="text-indigo-600">ID:</span> {candidateId}
          </p>
        </div>
        <div className="flex gap-4">
          {!isAnalyzing ? (
            <button
              onClick={startSession}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-medium text-sm transition-all shadow-lg shadow-indigo-500/20"
            >
              Start Interview
            </button>
          ) : (
            <button
              onClick={stopSession}
              className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded-lg font-medium text-sm transition-all shadow-lg shadow-red-500/20"
            >
              End Interview
            </button>
          )}
        </div>
      </div>
    );
    return () => setHeaderContent(null);
  }, [setHeaderContent, candidateId, isAnalyzing]); // Re-run when UI needs to change

  return (
    <main className="flex h-screen w-full bg-slate-950 text-slate-100 overflow-hidden font-sans selection:bg-indigo-500/30">
      {/* Left Panel: Q&A Interview */}
      <div className="w-2/3 h-full p-6 flex flex-col gap-6 transition-all duration-300">
        {/* Header moved to Portal */}

        <section className="flex-1 relative">
          {isAnalyzing ? (
            <QuestionPanel
              onAnswerSubmit={analyzeAnswer}
              onSessionComplete={handleSessionComplete}
              isAnalyzing={isAnalyzing}
            />
          ) : (
            <div className="w-full h-full bg-slate-900 rounded-2xl border border-slate-700 flex items-center justify-center">
              <div className="text-center p-8">
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-indigo-500/20 flex items-center justify-center">
                  <svg
                    className="w-8 h-8 text-indigo-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                </div>
                <h2 className="text-xl font-semibold text-white mb-2">
                  Ready to Begin
                </h2>
                <p className="text-slate-400 text-sm mb-4">
                  {INTERVIEW_QUESTIONS.length} questions to assess candidate
                  risk
                </p>
                <p className="text-slate-500 text-xs">
                  Click "Start Interview" to begin the assessment
                </p>
              </div>
            </div>
          )}
        </section>
      </div>

      {/* Right Panel: Analysis */}
      <div className="w-1/3 h-full p-6 pl-0 bg-slate-950">
        <LiveAnalysis
          transcript={transcript}
          analysisData={chartData}
          score={score}
          alerts={alerts}
        />
      </div>
    </main>
  );
}
