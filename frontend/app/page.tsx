import Link from "next/link";
import { Shield, Upload, History, Activity } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#0a0f1e] flex flex-col items-center justify-center p-8">
      {/* Header */}
      <div className="flex items-center gap-3 mb-2">
        <Shield className="w-10 h-10 text-blue-500" />
        <h1 className="text-4xl font-bold tracking-tight text-white">AMPLE</h1>
      </div>
      <p className="text-gray-400 text-sm mb-12 tracking-widest uppercase">
        Agentic Monitoring & Proactive Law Enforcement Engine
      </p>

      {/* Nav Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-3xl">
        <Link href="/dashboard" className="group bg-[#111827] border border-[#1f2937] hover:border-blue-500 rounded-2xl p-6 transition-all">
          <Activity className="w-8 h-8 text-blue-400 mb-3 group-hover:scale-110 transition-transform" />
          <h2 className="text-white font-semibold text-lg mb-1">Dashboard</h2>
          <p className="text-gray-400 text-sm">Live threat stats & system overview</p>
        </Link>

        <Link href="/upload" className="group bg-[#111827] border border-[#1f2937] hover:border-blue-500 rounded-2xl p-6 transition-all">
          <Upload className="w-8 h-8 text-blue-400 mb-3 group-hover:scale-110 transition-transform" />
          <h2 className="text-white font-semibold text-lg mb-1">Analyze Video</h2>
          <p className="text-gray-400 text-sm">Upload CCTV footage for analysis</p>
        </Link>

        <Link href="/incidents" className="group bg-[#111827] border border-[#1f2937] hover:border-blue-500 rounded-2xl p-6 transition-all">
          <History className="w-8 h-8 text-blue-400 mb-3 group-hover:scale-110 transition-transform" />
          <h2 className="text-white font-semibold text-lg mb-1">Incident History</h2>
          <p className="text-gray-400 text-sm">View all past detections & reports</p>
        </Link>
      </div>

      <p className="text-gray-600 text-xs mt-16">
        AMPLE v1.0 • Built for NVIDIA Agentic AI Hackathon
      </p>
    </main>
  );
}
