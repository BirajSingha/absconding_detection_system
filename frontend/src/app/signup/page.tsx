"use client";

import React, { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { authService } from "@/services/api";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import Link from "next/link";

export default function SignupPage() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    dob: "",
    current_role: "",
    total_experience: "",
    password: "",
    position_applied: "Software Engineer", // Default or Selectable
    department: "Engineering", // Default or Selectable
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const { login } = useAuth();

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
  ) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const data = await authService.signup(formData);
      login(data.token, data.user);
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.error || "Signup failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-4">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40rem] h-[40rem] bg-indigo-500/10 rounded-full blur-3xl" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40rem] h-[40rem] bg-purple-500/10 rounded-full blur-3xl" />
      </div>

      <Card className="w-full max-w-2xl bg-white/95 backdrop-blur-xl border-slate-200/50 shadow-2xl relative z-10 my-8">
        <CardHeader className="text-center pb-2">
          <CardTitle className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
            Create Account
          </CardTitle>
          <p className="text-slate-500 text-sm mt-2">
            Please enter your details to create an account
          </p>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && (
              <div className="p-3 rounded-lg bg-red-50 border border-red-100 text-red-600 text-sm">
                {error}
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Input
                name="name"
                label="Full Name"
                placeholder="John Doe"
                value={formData.name}
                onChange={handleChange}
                required
              />

              <Input
                name="email"
                type="email"
                label="Email Address"
                placeholder="john@example.com"
                value={formData.email}
                onChange={handleChange}
                required
              />

              <Input
                name="phone"
                label="Phone Number (Optional)"
                placeholder="+1 234 567 890"
                value={formData.phone}
                onChange={handleChange}
              />

              <Input
                name="dob"
                type="date"
                label="Date of Birth"
                value={formData.dob}
                onChange={handleChange}
              />

              <Input
                name="current_role"
                label="Current Role"
                placeholder="e.g. Frontend Developer"
                value={formData.current_role}
                onChange={handleChange}
              />

              <Input
                name="total_experience"
                label="Total Experience"
                placeholder="e.g. 5 years"
                value={formData.total_experience}
                onChange={handleChange}
              />
            </div>

            <Input
              name="password"
              type="password"
              label="Password"
              placeholder="Create a strong password"
              value={formData.password}
              onChange={handleChange}
              required
            />

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="w-full">
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Position Applied
                </label>
                <select
                  name="position_applied"
                  className="w-full px-3 py-2 bg-white border border-slate-300 rounded-lg text-sm text-slate-900 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
                  value={formData.position_applied}
                  onChange={handleChange}
                >
                  <option value="Software Engineer">Software Engineer</option>
                  <option value="Product Manager">Product Manager</option>
                  <option value="Data Scientist">Data Scientist</option>
                  <option value="Designer">Designer</option>
                </select>
              </div>

              <div className="w-full">
                <label className="block text-sm font-medium text-slate-700 mb-1">
                  Department
                </label>
                <select
                  name="department"
                  className="w-full px-3 py-2 bg-white border border-slate-300 rounded-lg text-sm text-slate-900 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500"
                  value={formData.department}
                  onChange={handleChange}
                >
                  <option value="Engineering">Engineering</option>
                  <option value="Product">Product</option>
                  <option value="Data">Data</option>
                  <option value="Design">Design</option>
                </select>
              </div>
            </div>

            <Button
              type="submit"
              className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white mt-6"
              size="lg"
              isLoading={loading}
            >
              Sign Up
            </Button>

            <p className="text-center text-sm text-slate-500 mt-4">
              Already have an account?{" "}
              <Link
                href="/login"
                className="text-indigo-600 hover:text-indigo-700 font-medium"
              >
                Sign in
              </Link>
            </p>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
