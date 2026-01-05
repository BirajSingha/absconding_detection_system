/**
 * Absconding Risk Detection Interview Questions
 * Designed to identify candidates with high flight risk
 */

export interface InterviewQuestion {
  id: string;
  text: string;
  category:
    | "job_stability"
    | "commitment"
    | "exit_intent"
    | "behavioral"
    | "situational";
  followUp?: string;
  riskIndicators: string[]; // Keywords that indicate potential risk
}

export const INTERVIEW_QUESTIONS: InterviewQuestion[] = [
  // Job Stability Questions
  {
    id: "q1",
    text: "Why did you leave your last position?",
    category: "job_stability",
    followUp: "How long were you in that role?",
    riskIndicators: [
      "conflict",
      "fired",
      "bored",
      "unhappy",
      "toxic",
      "underpaid",
    ],
  },
  {
    id: "q2",
    text: "How many jobs have you had in the last 5 years?",
    category: "job_stability",
    riskIndicators: ["many", "several", "few months", "short term"],
  },

  // Commitment Questions
  {
    id: "q3",
    text: "Where do you see yourself in 2 years?",
    category: "commitment",
    riskIndicators: [
      "not sure",
      "depends",
      "maybe",
      "different company",
      "own business",
    ],
  },
  {
    id: "q4",
    text: "What are your long-term career goals?",
    category: "commitment",
    riskIndicators: ["uncertain", "exploring", "haven't decided", "freelance"],
  },

  // Exit Intent Questions
  {
    id: "q5",
    text: "What would make you leave this role within the first year?",
    category: "exit_intent",
    riskIndicators: [
      "better offer",
      "salary",
      "remote",
      "boring",
      "management",
    ],
  },
  {
    id: "q6",
    text: "What are the top 3 things you look for in an employer?",
    category: "exit_intent",
    riskIndicators: ["flexibility", "freedom", "quick growth", "easy"],
  },

  // Behavioral Questions
  {
    id: "q7",
    text: "How do you handle workplace conflicts?",
    category: "behavioral",
    riskIndicators: ["avoid", "leave", "quit", "ignore", "confront"],
  },
  {
    id: "q8",
    text: "Describe a time you felt undervalued at work. How did you respond?",
    category: "behavioral",
    riskIndicators: ["quit", "left", "frustrated", "angry", "resigned"],
  },

  // Situational Questions
  {
    id: "q9",
    text: "If you received a better offer during your probation period here, what would you do?",
    category: "situational",
    riskIndicators: ["consider", "take it", "depends on salary", "maybe"],
  },
  {
    id: "q10",
    text: "What concerns, if any, do you have about this position?",
    category: "situational",
    riskIndicators: ["workload", "hours", "travel", "pressure", "not sure"],
  },
];

export const CATEGORY_LABELS: Record<InterviewQuestion["category"], string> = {
  job_stability: "Job Stability",
  commitment: "Commitment",
  exit_intent: "Exit Intent",
  behavioral: "Behavioral",
  situational: "Situational",
};

export const CATEGORY_DESCRIPTIONS: Record<
  InterviewQuestion["category"],
  string
> = {
  job_stability: "Assesses past job tenure and reasons for leaving",
  commitment: "Evaluates long-term career intentions",
  exit_intent: "Identifies potential reasons for early departure",
  behavioral: "Reveals how candidate handles workplace challenges",
  situational: "Tests decision-making in hypothetical scenarios",
};
