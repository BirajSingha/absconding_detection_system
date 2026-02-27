"use client";

import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { useEffect, useState } from "react";

export default function Home() {
  const { isAuthenticated, user } = useAuth();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Determine redirect path
  // If not mounted yet (SSR), default to login to avoid mismatch
  // If authenticated:
  //   - If admin -> /admin (optional, but good practice)
  //   - Else -> /chat
  // If not authenticated -> /login
  const getDestination = () => {
    if (!mounted) return "/login";
    if (isAuthenticated) {
      // Can check role if available, for now default to /chat
      return "/chat";
    }
    return "/login";
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24 bg-gradient-to-b from-slate-50 to-slate-100">
      <div className="text-center max-w-2xl">
        <h1 className="text-5xl font-extrabold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600 pb-2 leading-tight">
          Absconding Detection System
        </h1>
        <p className="text-xl text-slate-600 mb-8 leading-relaxed">
          Detailed HR Analytics and Employee Retention Dashboard.
        </p>
        <Link
          href={getDestination()}
          className="inline-flex items-center px-8 py-4 text-base font-medium text-white bg-indigo-600 rounded-full hover:bg-indigo-700 transition-colors shadow-lg hover:shadow-indigo-500/30"
        >
          {mounted && isAuthenticated ? "Go to Dashboard" : "Get Started"}
          <svg
            className="ml-2 w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M13 7l5 5m0 0l-5 5m5-5H6"
            />
          </svg>
        </Link>
      </div>
    </div>
  );
}
