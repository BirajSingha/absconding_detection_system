import axios from "axios";

const API_URL = "http://localhost:5000/api";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const authService = {
  login: async (email: string, password: string) => {
    const response = await api.post("/auth/login", { email, password });
    return response.data;
  },

  signup: async (data: any) => {
    const response = await api.post("/auth/signup", data);
    return response.data;
  },
};

export const chatService = {
  sendMessage: async (message: string, history: any[] = []) => {
    const response = await api.post("/chat/message", { message, history });
    return response.data;
  },
};

export const analysisService = {
  async getCandidateAnalysis(candidateId: string) {
    const response = await api.get(`/analysis/candidate/${candidateId}`);
    return response.data;
  },

  async analyzeInterview(
    candidateId: string,
    candidateName: string,
    transcript: string,
    position: string = "Software Engineer",
  ) {
    const response = await api.post("/analysis/analyze-interview", {
      candidate_id: candidateId,
      candidate_name: candidateName,
      transcript_text: transcript,
      position: position,
    });
    return response.data;
  },
};

export const candidatesService = {
  async getAll() {
    const response = await api.get("/candidates/");
    return response.data;
  },
};

export default api;
