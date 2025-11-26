# Absconding Detection System - Frontend Dashboard

This is the frontend dashboard for the Absconding Detection System, built with **Next.js 14**, **TypeScript**, and **Tailwind CSS**.

## 🚀 Quick Start

1.  **Install dependencies**:

    ```bash
    npm install
    ```

2.  **Run the development server**:

    ```bash
    npm run dev
    ```

3.  **Open the dashboard**:
    Navigate to [http://localhost:3000](http://localhost:3000)

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Charts**: Recharts
- **Utilities**: clsx, tailwind-merge, date-fns

## 📂 Project Structure

```
src/
├── app/                 # App Router pages
│   ├── page.tsx         # Dashboard Home
│   ├── employees/       # Employee List
│   ├── alerts/          # Risk Alerts
│   └── analytics/       # Analytics Dashboard
├── components/
│   ├── layout/          # Sidebar, Header
│   ├── dashboard/       # AlertCard, EmployeeCard, RiskMeter
│   └── charts/          # Recharts components
├── lib/
│   ├── api.ts           # API integration service
│   └── types.ts         # TypeScript interfaces
```

## 🔌 API Integration

The frontend connects to the Flask backend at `http://localhost:5000/api`.
Ensure the backend server is running before using the dashboard.

## 📱 Features

- **Real-time Dashboard**: View key metrics and recent alerts.
- **Employee Monitoring**: List of all employees with risk scores.
- **Risk Visualization**: Interactive charts and color-coded risk meters.
- **Alert Management**: View and manage high-risk alerts.
