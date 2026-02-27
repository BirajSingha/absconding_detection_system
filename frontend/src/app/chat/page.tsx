"use client";

import React, { useEffect, useState, useRef } from "react";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { chatService, analysisService } from "@/services/api";
import { Send, LogOut, User as UserIcon, Bot } from "lucide-react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export default function ChatInterface() {
  const { user, logout, isAuthenticated } = useAuth();
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "Hello! I am your AI Chat Support. How can I help you regarding your offer or company policies today?",
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
    }
  }, [router]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      // Prepare history for RAG context (simple list of dicts)
      const history = messages.map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const response = await chatService.sendMessage(
        userMessage.content,
        history,
      );

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content:
          response.response ||
          "I apologize, but I couldn't generate a response.",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content:
          "Sorry, I encountered an error connecting to the server. Please try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleDisconnect = async () => {
    const hasUserMessages = messages.some((m) => m.role === "user");
    if (!hasUserMessages) {
      // Chat is empty from candidate side
      console.log("No user messages, aborting analysis.");
      logout();
      return;
    }

    setIsAnalyzing(true);
    try {
      // Format transcript
      const transcript = messages
        .filter((m) => m.id !== "welcome")
        .map(
          (m) =>
            `${m.role === "user" ? "Candidate" : "Interviewer (AI)"}: ${m.content}`,
        )
        .join("\n");

      // Trigger Analysis
      // Note: In a real app we might get candidateId from context or user profile
      // For now, using a resilient fallback or the user ID if available
      const candidateId = user?.id ? String(user.id) : `GUEST_${Date.now()}`;

      await analysisService.analyzeInterview(
        candidateId,
        user?.name || "Guest Candidate",
        transcript,
      );
    } catch (error) {
      console.error("Analysis failed:", error);
      // We log out anyway, analysis failure shouldn't trap the user
    } finally {
      setIsAnalyzing(false);
      logout();
    }
  };

  if (!user && !isAuthenticated) {
    return null;
  }

  return (
    <div className="flex flex-col h-screen bg-slate-950">
      {/* Header */}
      <header className="bg-slate-900 border-b border-slate-800 px-6 py-4 flex justify-between items-center shadow-sm z-10">
        <div className="flex items-center gap-3">
          <div className="bg-indigo-600 p-2 rounded-lg">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">AI Chat Support</h1>
            <p className="text-xs text-slate-400">Online | AI Powered</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right hidden sm:block">
            <p className="text-sm font-medium text-white">{user?.name}</p>
            <p className="text-xs text-slate-400">{user?.email}</p>
          </div>
          <Button
            variant="outline"
            onClick={handleDisconnect}
            size="sm"
            disabled={loading || isAnalyzing}
            className="flex items-center gap-2 border-slate-700 hover:border-red-500 text-slate-300 hover:bg-slate-800 hover:text-red-500 hover:animate-pulse"
          >
            <LogOut className="w-4 h-4" />
            <span className="hidden sm:inline">
              {isAnalyzing ? "Saving..." : "Disconnect"}
            </span>
          </Button>
        </div>
      </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`flex max-w-[80%] sm:max-w-[70%] gap-3 ${msg.role === "user" ? "flex-row-reverse" : "flex-row"}`}
            >
              {/* Avatar */}
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                  msg.role === "user"
                    ? "bg-indigo-500/20 text-indigo-400"
                    : "bg-emerald-500/20 text-emerald-400"
                }`}
              >
                {msg.role === "user" ? (
                  <UserIcon size={16} />
                ) : (
                  <Bot size={16} />
                )}
              </div>

              {/* Message Bubble */}
              <div
                className={`p-4 rounded-2xl shadow-sm text-sm leading-relaxed ${
                  msg.role === "user"
                    ? "bg-indigo-600 text-white rounded-tr-none"
                    : "bg-slate-800 text-slate-100 border border-slate-700 rounded-tl-none"
                }`}
              >
                {msg.content}
                <div
                  className={`text-[10px] mt-2 opacity-70 ${msg.role === "user" ? "text-indigo-100" : "text-slate-400"}`}
                >
                  {msg.timestamp.toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </div>
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="flex max-w-[80%] gap-3">
              <div className="w-8 h-8 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center flex-shrink-0">
                <Bot size={16} />
              </div>
              <div className="bg-slate-800 p-4 rounded-2xl rounded-tl-none border border-slate-700 shadow-sm">
                <div className="flex space-x-2">
                  <div
                    className="w-2 h-2 bg-slate-500 rounded-full animate-bounce"
                    style={{ animationDelay: "0ms" }}
                  />
                  <div
                    className="w-2 h-2 bg-slate-500 rounded-full animate-bounce"
                    style={{ animationDelay: "150ms" }}
                  />
                  <div
                    className="w-2 h-2 bg-slate-500 rounded-full animate-bounce"
                    style={{ animationDelay: "300ms" }}
                  />
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </main>

      {/* Input Area */}
      <footer className="bg-slate-900 border-t border-slate-800 p-4">
        <div className="max-w-4xl mx-auto relative">
          <form onSubmit={handleSend} className="flex gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 py-3 shadow-none bg-slate-800 border-slate-700 text-slate-100 placeholder-slate-400 focus:border-indigo-500 focus:ring-indigo-500/20"
              disabled={loading}
            />
            <Button
              type="submit"
              disabled={!input.trim() || loading}
              className="px-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md transition-all"
            >
              <Send size={18} />
              <span className="sr-only sm:not-sr-only sm:ml-2">Send</span>
            </Button>
          </form>
          <p className="text-center text-xs text-slate-500 mt-2">
            AI can make mistakes. Please verify important information.
          </p>
        </div>
      </footer>
    </div>
  );
}
