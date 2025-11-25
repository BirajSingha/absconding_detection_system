# Absconding Detection System - Frontend

A modern, responsive web application built with **Next.js 14**, **TypeScript**, and **Tailwind CSS** for real-time employee attrition risk monitoring and HR analytics.

---

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Add your backend API URL

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) - Frontend  
Backend API: [http://localhost:5000](http://localhost:5000)

---

## 🛠️ Tech Stack

### Core

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Context + SWR for data fetching
- **Charts**: Recharts / Chart.js
- **Icons**: Lucide React / Heroicons

### UI Components

- **shadcn/ui** - Accessible component library
- **Radix UI** - Headless UI primitives
- **React Hook Form** - Form handling
- **Zod** - Schema validation

### Additional Tools

- **Axios** - HTTP client
- **date-fns** - Date manipulation
- **clsx** - Conditional classnames
- **tailwind-merge** - Merge Tailwind classes

---

## 📁 Project Structure

```
frontend/
├── app/                          # Next.js App Router
│   ├── (auth)/                   # Auth routes
│   │   ├── login/
│   │   └── layout.tsx
│   ├── (dashboard)/              # Protected routes
│   │   ├── dashboard/            # Main dashboard
│   │   ├── employees/            # Employee management
│   │   │   ├── page.tsx          # List view
│   │   │   ├── [id]/             # Detail view
│   │   │   └── new/              # Create new
│   │   ├── alerts/               # Alert management
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   ├── analytics/            # Analytics & reports
│   │   └── layout.tsx
│   ├── api/                      # API routes (optional proxy)
│   ├── layout.tsx                # Root layout
│   ├── page.tsx                  # Landing page
│   └── globals.css               # Global styles
├── components/
│   ├── ui/                       # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   ├── table.tsx
│   │   └── ...
│   ├── dashboard/                # Dashboard components
│   │   ├── RiskDistributionChart.tsx
│   │   ├── AlertTrendChart.tsx
│   │   ├── DepartmentStats.tsx
│   │   └── TopAtRiskTable.tsx
│   ├── employees/                # Employee components
│   │   ├── EmployeeList.tsx
│   │   ├── EmployeeCard.tsx
│   │   ├── EmployeeForm.tsx
│   │   └── EmployeeMetrics.tsx
│   ├── alerts/                   # Alert components
│   │   ├── AlertList.tsx
│   │   ├── AlertCard.tsx
│   │   ├── RiskBadge.tsx
│   │   └── AlertFilters.tsx
│   └── layouts/                  # Layout components
│       ├── Header.tsx
│       ├── Sidebar.tsx
│       └── Footer.tsx
├── lib/
│   ├── api/                      # API client
│   │   ├── client.ts             # Axios instance
│   │   ├── employees.ts          # Employee endpoints
│   │   ├── alerts.ts             # Alert endpoints
│   │   └── analytics.ts          # Analytics endpoints
│   ├── hooks/                    # Custom hooks
│   │   ├── useEmployees.ts
│   │   ├── useAlerts.ts
│   │   └── useAnalytics.ts
│   ├── utils/                    # Utility functions
│   │   ├── cn.ts                 # classnames helper
│   │   ├── formatters.ts         # Data formatters
│   │   └── validators.ts         # Validation schemas
│   └── types/                    # TypeScript types
│       ├── employee.ts
│       ├── alert.ts
│       └── analytics.ts
├── public/                       # Static assets
│   ├── images/
│   └── icons/
├── .env.example                  # Environment variables template
├── .env.local                    # Local environment variables
├── next.config.js                # Next.js configuration
├── tailwind.config.ts            # Tailwind configuration
├── tsconfig.json                 # TypeScript configuration
└── package.json
```

---

## 🎯 Core Features

### 1. Dashboard (Main View)

- **Real-time risk overview** with live stats
- **Risk distribution chart** (CRITICAL/HIGH/MEDIUM/LOW)
- **Alert trend visualization** (line chart over time)
- **Top at-risk employees** table
- **Department statistics** comparison
- **Quick action buttons** (Analyze, View Details)

### 2. Employee Management

- **Employee list** with search and filters
- **Employee detail view** with full profile
- **Performance metrics** (productivity, attendance, rating)
- **Alert history** timeline
- **Edit metrics** modal/form
- **Create new employee** form
- **Risk indicator** badges

### 3. Alert Management

- **Alert list** with status filters
- **Risk level filtering** (HIGH/CRITICAL only, etc.)
- **Alert detail view** with:
  - Employee information
  - Behavioral indicators
  - Sentiment analysis results
  - AI-generated insights
  - Recommendations
  - Timeline estimate
- **Update alert status** (Acknowledge, In Progress, Resolved)
- **Record intervention outcome**

### 4. Analytics & Reports

- **Department comparison** charts
- **Alert trends** over customizable periods
- **Risk distribution** pie/donut charts
- **Employee alert history** graphs
- **Export to PDF/CSV** functionality
- **Date range selector**

### 5. Employees Module

- **CRUD operations** for employees
- **Bulk import** via CSV
- **Performance metrics tracking**
- **Department/role filtering**
- **Sort by risk score**

---

## 🎨 Design System

### Color Palette (Tailwind)

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eff6ff",
          500: "#3b82f6",
          600: "#2563eb",
        },
        success: "#10b981",
        warning: "#f59e0b",
        danger: "#ef4444",
        critical: "#dc2626",
        risk: {
          low: "#10b981", // green
          medium: "#f59e0b", // orange
          high: "#ef4444", // red
          critical: "#dc2626", // dark red
        },
      },
    },
  },
};
```

### Component Patterns

**Risk Badge Component**:

```typescript
interface RiskBadgeProps {
  level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  score?: number;
}

export function RiskBadge({ level, score }: RiskBadgeProps) {
  const variants = {
    LOW: "bg-green-100 text-green-800 border-green-200",
    MEDIUM: "bg-yellow-100 text-yellow-800 border-yellow-200",
    HIGH: "bg-red-100 text-red-800 border-red-200",
    CRITICAL: "bg-red-200 text-red-900 border-red-300",
  };

  return (
    <span
      className={cn(
        "px-3 py-1 rounded-full text-sm font-medium border",
        variants[level]
      )}
    >
      {level} {score && `(${score.toFixed(1)})`}
    </span>
  );
}
```

---

## 🔌 API Integration

### Environment Variables

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:5000/api
NEXT_PUBLIC_WS_URL=ws://localhost:5000  # For real-time updates (optional)
```

### API Client Setup

```typescript
// lib/api/client.ts
import axios from "axios";

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor (add auth token if needed)
apiClient.interceptors.request.use((config) => {
  // Add auth token here if implementing authentication
  return config;
});

// Response interceptor (handle errors)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error);
    return Promise.reject(error);
  }
);

export default apiClient;
```

### API Service Example

```typescript
// lib/api/employees.ts
import apiClient from "./client";
import { Employee } from "@/lib/types/employee";

export const employeeService = {
  getAll: async () => {
    const { data } = await apiClient.get<Employee[]>("/employees");
    return data;
  },

  getById: async (id: string) => {
    const { data } = await apiClient.get<Employee>(`/employees/${id}`);
    return data;
  },

  create: async (employee: Partial<Employee>) => {
    const { data } = await apiClient.post<Employee>("/employees", employee);
    return data;
  },

  update: async (id: string, employee: Partial<Employee>) => {
    const { data } = await apiClient.put<Employee>(
      `/employees/${id}`,
      employee
    );
    return data;
  },

  updateMetrics: async (
    id: string,
    metrics: {
      productivity_score?: number;
      attendance_percentage?: number;
      performance_rating?: number;
    }
  ) => {
    const { data } = await apiClient.put(`/employees/${id}/metrics`, metrics);
    return data;
  },

  delete: async (id: string) => {
    await apiClient.delete(`/employees/${id}`);
  },
};
```

### Custom Hook with SWR

```typescript
// lib/hooks/useEmployees.ts
import useSWR from "swr";
import { employeeService } from "@/lib/api/employees";

export function useEmployees() {
  const { data, error, mutate } = useSWR("employees", employeeService.getAll, {
    refreshInterval: 30000, // Refresh every 30s
  });

  return {
    employees: data,
    isLoading: !error && !data,
    isError: error,
    mutate,
  };
}
```

---

## 📊 Dashboard Components

### Risk Distribution Chart

```typescript
// components/dashboard/RiskDistributionChart.tsx
"use client";

import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from "recharts";
import { useAnalytics } from "@/lib/hooks/useAnalytics";

const COLORS = {
  CRITICAL: "#dc2626",
  HIGH: "#ef4444",
  MEDIUM: "#f59e0b",
  LOW: "#10b981",
};

export function RiskDistributionChart() {
  const { riskDistribution } = useAnalytics();

  const data = Object.entries(riskDistribution || {}).map(([name, value]) => ({
    name,
    value,
  }));

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Risk Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) =>
              `${name}: ${(percent * 100).toFixed(0)}%`
            }
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry) => (
              <Cell key={entry.name} fill={COLORS[entry.name]} />
            ))}
          </Pie>
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
```

---

## 🎭 TypeScript Types

```typescript
// lib/types/employee.ts
export interface Employee {
  id: number;
  employee_id: string;
  name: string;
  email: string;
  phone?: string;
  role: string;
  department: string;
  tenure_years: number;
  manager_id?: string;
  manager_name?: string;
  employment_status: "ACTIVE" | "INACTIVE" | "RESIGNED";
  productivity_score: number;
  attendance_percentage: number;
  performance_rating: number;
  created_at: string;
  updated_at: string;
}

// lib/types/alert.ts
export type RiskLevel = "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
export type AlertStatus = "OPEN" | "ACKNOWLEDGED" | "IN_PROGRESS" | "RESOLVED";

export interface Alert {
  id: number;
  employee_id: string;
  risk_score: number;
  risk_level: RiskLevel;
  confidence_score: number;
  behavioral_indicators: BehavioralIndicator[];
  sentiment_indicators: SentimentIndicator;
  ai_summary: string;
  timeline_estimate: string;
  recommendations: string[];
  status: AlertStatus;
  created_at: string;
  updated_at: string;
}

export interface BehavioralIndicator {
  type: string;
  severity: number;
  value: number;
  threshold: number;
  description: string;
}

export interface SentimentIndicator {
  overall_sentiment: string;
  positive_count: number;
  negative_count: number;
  neutral_count: number;
  average_score: number;
  exit_intent_score: number;
  exit_keywords_found: string[];
}
```

---

## 🚦 Routing

### App Router Structure

```
app/
├── page.tsx                    # Landing / Login
├── (dashboard)/
│   ├── layout.tsx              # Dashboard layout with sidebar
│   ├── dashboard/
│   │   └── page.tsx            # Main dashboard
│   ├── employees/
│   │   ├── page.tsx            # GET /api/employees
│   │   ├── [id]/
│   │   │   └── page.tsx        # GET /api/employees/:id
│   │   └── new/
│   │       └── page.tsx        # POST /api/employees
│   ├── alerts/
│   │   ├── page.tsx            # GET /api/alerts
│   │   └── [id]/
│   │       └── page.tsx        # GET /api/alerts/:id
│   └── analytics/
│       └── page.tsx            # Analytics dashboard
```

### Protected Routes (Middleware)

```typescript
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  // Add authentication check here
  const isAuthenticated = true; // Replace with actual auth check

  if (!isAuthenticated && !request.nextUrl.pathname.startsWith("/login")) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
```

---

## 🎨 Styling Guide

### Tailwind Best Practices

```typescript
// Use cn utility for conditional classes
import { cn } from '@/lib/utils/cn';

<div className={cn(
  'px-4 py-2 rounded-lg',
  isActive && 'bg-blue-500 text-white',
  isDisabled && 'opacity-50 cursor-not-allowed'
)} />

// Responsive design
<div className="
  grid grid-cols-1           // Mobile
  md:grid-cols-2            // Tablet
  lg:grid-cols-3            // Desktop
  gap-4
" />

// Dark mode support (if needed)
<div className="bg-white dark:bg-gray-800" />
```

### Component Styling Patterns

```typescript
// Card Component
<div
  className="
  bg-white 
  rounded-lg 
  shadow-md 
  hover:shadow-lg 
  transition-shadow 
  p-6
"
>
  Content
</div>;

// Button Variants
const buttonVariants = {
  primary: "bg-blue-600 hover:bg-blue-700 text-white",
  danger: "bg-red-600 hover:bg-red-700 text-white",
  outline: "border-2 border-blue-600 text-blue-600 hover:bg-blue-50",
};
```

---

## 📱 Responsive Design

### Breakpoints (Tailwind default)

- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

### Mobile-First Approach

```typescript
// Dashboard grid - stacks on mobile, grid on desktop
<div
  className="
  grid 
  grid-cols-1           // 1 column on mobile
  md:grid-cols-2        // 2 columns on tablet
  lg:grid-cols-4        // 4 columns on desktop
  gap-4
"
>
  <StatCard />
  <StatCard />
  <StatCard />
  <StatCard />
</div>
```

---

## 🧪 Testing

```bash
# Unit tests
npm run test

# E2E tests
npm run test:e2e

# Type checking
npm run type-check

# Linting
npm run lint
```

---

## 🚀 Deployment

### Build for Production

```bash
npm run build
npm run start
```

### Environment Variables (Production)

```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com/api
```

### Deployment Platforms

- **Vercel** (Recommended for Next.js)
- **Netlify**
- **AWS Amplify**
- **Docker** (with nginx)

---

## 📦 Installation & Setup

### 1. Create Next.js App

```bash
npx create-next-app@latest frontend --typescript --tailwind --app
cd frontend
```

### 2. Install Dependencies

```bash
# UI Components
npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu
npm install lucide-react clsx tailwind-merge

# Data Fetching & State
npm install swr axios

# Charts
npm install recharts

# Forms
npm install react-hook-form @hookform/resolvers zod

# Date handling
npm install date-fns

# shadcn/ui (optional but recommended)
npx shadcn-ui@latest init
```

### 3. Configure Environment

```bash
cp .env.example .env.local
```

Edit `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:5000/api
```

### 4. Run Development Server

```bash
npm run dev
```

---

## 🔐 Authentication (Future Enhancement)

```typescript
// lib/context/AuthContext.tsx
"use client";

import { createContext, useContext, useState } from "react";

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);

  const login = async (email: string, password: string) => {
    // Implement login logic
  };

  const logout = () => {
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
};
```

---

## 📈 Performance Optimization

- ✅ Use Next.js Image component for optimized images
- ✅ Implement code splitting with dynamic imports
- ✅ Use SWR for client-side caching
- ✅ Lazy load charts and heavy components
- ✅ Optimize Tailwind CSS (purge unused styles)
- ✅ Use React.memo for expensive components
- ✅ Implement virtual scrolling for large lists

---

## 🐛 Troubleshooting

### CORS Issues

Add CORS middleware to backend or use Next.js API routes as proxy.

### Build Errors

```bash
# Clear cache and rebuild
rm -rf .next node_modules
npm install
npm run build
```

### TypeScript Errors

```bash
npm run type-check
```

---

## 📚 Resources

- **Next.js Documentation**: https://nextjs.org/docs
- **Tailwind CSS**: https://tailwindcss.com/docs
- **shadcn/ui**: https://ui.shadcn.com
- **SWR**: https://swr.vercel.app
- **TypeScript**: https://www.typescriptlang.org/docs

---

## 🤝 Contributing

1. Follow TypeScript best practices
2. Use Tailwind CSS for all styling
3. Follow Next.js App Router conventions
4. Write type-safe code
5. Create reusable components

---

**Built with ⚡ Next.js + TypeScript + Tailwind CSS**
