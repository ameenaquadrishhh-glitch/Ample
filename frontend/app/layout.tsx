import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Link from "next/link";
import { Shield, Activity, Upload, History } from "lucide-react";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AMPLE - Security Operations Platform",
  description: "Agentic Monitoring and Proactive Law Enforcement Engine",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="fixed top-0 left-0 right-0 z-50 bg-[#0a0f1e]/80 backdrop-blur border-b border-[#1f2937]">
          <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
            <Link href="/" className="flex items-center gap-2">
              <Shield className="w-5 h-5 text-blue-500" />
              <span className="text-white font-bold tracking-tight">AMPLE</span>
              <span className="text-[10px] text-gray-500 uppercase tracking-widest ml-1 hidden sm:block">Security Ops</span>
            </Link>
            <div className="flex items-center gap-1">
              <Link href="/dashboard" className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-[#1f2937] transition-all text-sm">
                <Activity className="w-4 h-4" />
                <span className="hidden sm:block">Dashboard</span>
              </Link>
              <Link href="/upload" className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-[#1f2937] transition-all text-sm">
                <Upload className="w-4 h-4" />
                <span className="hidden sm:block">Analyze</span>
              </Link>
              <Link href="/incidents" className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-[#1f2937] transition-all text-sm">
                <History className="w-4 h-4" />
                <span className="hidden sm:block">Incidents</span>
              </Link>
            </div>
          </div>
        </nav>
        <div className="pt-14">{children}</div>
      </body>
    </html>
  );
}