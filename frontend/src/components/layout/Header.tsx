"use client";

import { Bell, Menu } from "lucide-react";

interface HeaderProps {
  onMenuClick?: () => void;
}

export function Header({ onMenuClick }: HeaderProps) {
  return (
    <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-4 shadow-sm sm:px-6">
      <div className="flex items-center gap-4">
        <button
          onClick={onMenuClick}
          className="rounded-md p-1 text-slate-500 hover:bg-slate-100 hover:text-slate-700 md:hidden"
        >
          <Menu className="h-6 w-6" />
        </button>
        <h2 className="text-lg font-semibold text-slate-800">HR Dashboard</h2>
      </div>

      <div className="flex items-center space-x-4">
        <button className="relative rounded-full p-1 text-slate-500 hover:bg-slate-100 hover:text-slate-700">
          <Bell className="h-6 w-6" />
          <span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-red-500"></span>
        </button>

        <div className="flex items-center space-x-3 border-l border-slate-200 pl-4">
          <div className="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-bold">
            HR
          </div>
          <div className="hidden md:block">
            <p className="text-sm font-medium text-slate-700">HR Manager</p>
            <p className="text-xs text-slate-500">Admin</p>
          </div>
        </div>
      </div>
    </header>
  );
}
