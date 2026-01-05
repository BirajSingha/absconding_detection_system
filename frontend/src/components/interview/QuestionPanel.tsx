"use client";

import React, { useState } from "react";
import { ChevronRight, ChevronLeft, Send, CheckCircle } from "lucide-react";
import {
  INTERVIEW_QUESTIONS,
  CATEGORY_LABELS,
  InterviewQuestion,
} from "@/lib/questions";

interface QuestionPanelProps {
  onAnswerSubmit: (
    questionId: string,
    answer: string,
    allAnswers: Record<string, string>
  ) => void;
  onSessionComplete: (allAnswers: Record<string, string>) => void;
  isAnalyzing: boolean;
}

export default function QuestionPanel({
  onAnswerSubmit,
  onSessionComplete,
  isAnalyzing,
}: QuestionPanelProps) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [currentAnswer, setCurrentAnswer] = useState("");
  const [isComplete, setIsComplete] = useState(false);

  const currentQuestion = INTERVIEW_QUESTIONS[currentIndex];
  const progress = ((currentIndex + 1) / INTERVIEW_QUESTIONS.length) * 100;

  const handleSubmitAnswer = () => {
    if (!currentAnswer.trim()) return;

    const newAnswers = {
      ...answers,
      [currentQuestion.id]: currentAnswer,
    };
    setAnswers(newAnswers);

    // Submit for analysis
    onAnswerSubmit(currentQuestion.id, currentAnswer, newAnswers);

    // Move to next question or complete
    if (currentIndex < INTERVIEW_QUESTIONS.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setCurrentAnswer(
        answers[INTERVIEW_QUESTIONS[currentIndex + 1]?.id] || ""
      );
    } else {
      setIsComplete(true);
      onSessionComplete(newAnswers);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      // Save current answer
      if (currentAnswer.trim()) {
        setAnswers({ ...answers, [currentQuestion.id]: currentAnswer });
      }
      setCurrentIndex(currentIndex - 1);
      setCurrentAnswer(
        answers[INTERVIEW_QUESTIONS[currentIndex - 1]?.id] || ""
      );
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && e.ctrlKey) {
      handleSubmitAnswer();
    }
  };

  if (isComplete) {
    return (
      <div className="relative w-full h-full bg-slate-900 rounded-2xl overflow-hidden shadow-2xl border border-slate-700 flex items-center justify-center">
        <div className="text-center p-8">
          <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-green-500/20 flex items-center justify-center">
            <CheckCircle className="w-10 h-10 text-green-400" />
          </div>
          <h2 className="text-2xl font-bold text-white mb-2">
            Interview Complete
          </h2>
          <p className="text-slate-400 mb-4">
            All {INTERVIEW_QUESTIONS.length} questions answered
          </p>
          <p className="text-sm text-slate-500">
            Analysis is being processed...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative w-full h-full bg-slate-900 rounded-2xl overflow-hidden shadow-2xl border border-slate-700 flex flex-col">
      {/* Progress Bar */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-slate-800">
        <div
          className="h-full bg-gradient-to-r from-indigo-500 to-cyan-400 transition-all duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Header */}
      <div className="p-6 border-b border-slate-800">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-indigo-400">
            Question {currentIndex + 1} of {INTERVIEW_QUESTIONS.length}
          </span>
          <span className="px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300">
            {CATEGORY_LABELS[currentQuestion.category]}
          </span>
        </div>
        {isAnalyzing && (
          <div className="flex items-center gap-2 mt-2">
            <div className="w-2 h-2 rounded-full bg-indigo-500 animate-pulse" />
            <span className="text-xs text-indigo-300">Session In Progress</span>
          </div>
        )}
      </div>

      {/* Question */}
      <div className="flex-1 p-6 flex flex-col">
        <h2 className="text-xl font-semibold text-white mb-6 leading-relaxed">
          {currentQuestion.text}
        </h2>

        {/* Answer Input */}
        <div className="flex-1 relative">
          <textarea
            value={currentAnswer}
            onChange={(e) => setCurrentAnswer(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your answer here..."
            className="w-full h-full min-h-[300px] bg-slate-800/50 border border-slate-700 rounded-xl p-4 text-white placeholder-slate-500 resize-none focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all"
          />
          <span className="absolute bottom-3 right-3 text-xs text-slate-500">
            Ctrl+Enter to submit
          </span>
        </div>
      </div>

      {/* Navigation */}
      <div className="p-6 border-t border-slate-800 flex justify-between items-center">
        <button
          onClick={handlePrevious}
          disabled={currentIndex === 0}
          className="flex items-center gap-2 px-4 py-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-all disabled:opacity-30 disabled:cursor-not-allowed"
        >
          <ChevronLeft className="w-4 h-4" />
          Previous
        </button>

        <button
          onClick={handleSubmitAnswer}
          disabled={!currentAnswer.trim()}
          className="flex items-center gap-2 px-6 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg font-medium transition-all shadow-lg shadow-indigo-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {currentIndex === INTERVIEW_QUESTIONS.length - 1 ? (
            <>
              <Send className="w-4 h-4" />
              Complete
            </>
          ) : (
            <>
              Next
              <ChevronRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>
    </div>
  );
}
