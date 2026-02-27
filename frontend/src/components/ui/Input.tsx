import React, { InputHTMLAttributes } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export function Input({ label, error, className = "", ...props }: InputProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-slate-700 mb-1">
          {label}
        </label>
      )}
      <input
        className={`
          w-full px-3 py-2 bg-white border rounded-lg text-sm text-slate-900 shadow-sm placeholder-slate-400
          focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500
          disabled:bg-slate-50 disabled:text-slate-500 disabled:border-slate-200 disabled:shadow-none
          ${error ? "border-red-500 focus:border-red-500 focus:ring-red-500" : "border-slate-300"}
          ${className}
        `}
        {...props}
      />
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  );
}
