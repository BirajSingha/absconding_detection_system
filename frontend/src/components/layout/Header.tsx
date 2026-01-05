"use client";

import { Bell, Menu, Search } from "lucide-react";
import { usePathname } from "next/navigation";
import { useHeader } from "@/context/HeaderContext";

interface HeaderProps {
  onMenuClick?: () => void;
}

export function Header({ onMenuClick }: HeaderProps) {
  const pathname = usePathname();
  const { headerContent } = useHeader();

  const getPageTitle = (path: string) => {
    if (path === "/") return "Recruitment Dashboard";
    if (path.includes("/interview")) return "Live Interview Session";
    if (path.includes("/candidates")) return "Candidate Management";
    if (path.includes("/analysis")) return "Analysis Reports";
    return "HR Portal";
  };

  return (
    <header className="flex h-16 items-center justify-between border-b border-slate-800 bg-slate-950 px-4 shadow-sm sm:px-6 text-slate-100">
      <div className="flex items-center gap-4 flex-1">
        <button
          onClick={onMenuClick}
          className="rounded-md p-1 text-slate-400 hover:bg-slate-800 hover:text-white md:hidden"
        >
          <Menu className="h-6 w-6" />
        </button>

        {headerContent ? (
          <div className="flex-1">{headerContent}</div>
        ) : (
          <h2 className="text-lg font-semibold bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-cyan-400">
            {getPageTitle(pathname)}
          </h2>
        )}
      </div>

      {/* <div className="flex items-center space-x-4">
        <button className="relative rounded-full p-1 text-slate-400 hover:bg-slate-800 hover:text-indigo-400 transition-colors">
          <Bell className="h-5 w-5" />
          <span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-red-500 animate-pulse"></span>
        </button>

        <div className="flex items-center space-x-3 border-l border-slate-800 pl-4">
          <div className="hidden md:block text-right">
            <p className="text-sm font-medium text-slate-200">Sarah Jenkins</p>
            <p className="text-xs text-slate-500">Senior HR Manager</p>
          </div>
          <div className="h-9 w-9 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold shadow-lg shadow-indigo-500/20 ring-2 ring-slate-800">
            SJ
          </div>
        </div>
      </div> */}
    </header>
  );
}
