import type { Metadata } from "next";
import "./globals.css";
import { AppLayout } from "@/components/layout/AppLayout";

export const metadata: Metadata = {
  title: "Absconding Detection System",
  description: "HR Dashboard for Employee Retention",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-50 text-slate-900 font-sans">
        <AppLayout>{children}</AppLayout>
      </body>
    </html>
  );
}
