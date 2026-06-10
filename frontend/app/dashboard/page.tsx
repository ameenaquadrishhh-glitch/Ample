"use client";
import { useEffect, useState } from "react";
import { Shield, AlertTriangle, CheckCircle, Activity } from "lucide-react";

const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

interface Stats {
  total: number;
  violence_detected: number;
  critical: number;
  high: number;
  medium: number;
  low: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${BACKEND}/api/v1/incidents/stats/summary`)
      .then(r => r.json())
      .then(setStats)
      .catch(() => setStats({ total: 0, violence_detected: 0, critical: 0, high: 0, medium: 0, low: 0 }))
      .finally(() => setLoading(false));
  }, []);

  const cards = stats ? [
    { label: "Total Incidents", value: stats.total, icon: Activity, color: "text-blue-400" },
    { label: "Violence Detected", value: stats.violence_detected, icon: AlertTriangle, color: "text-red-400" },
    { label: "Critical Threats", value: stats.critical, icon: Shield, color: "text-red-500" },
    { label: "Safe Incidents", value: stats.low, icon: CheckCircle, color: "text-green-400" },
  ] : [];

  return (
    <main className="min-h-screen bg-[#0a0f1e] p-8">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-2">Command Center</h1>
        <p className="text-gray-400 mb-8">Real-time security operations overview</p>

        {loading ? (
          <p className="text-gray-500">Loading stats...</p>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {cards.map((c) => (
              <div key={c.label} className="bg-[#111827] border border-[#1f2937] rounded-2xl p-5">
                <c.icon className={`w-6 h-6 ${c.color} mb-3`} />
                <p className="text-3xl font-bold text-white">{c.value}</p>
                <p className="text-gray-400 text-sm mt-1">{c.label}</p>
              </div>
            ))}
          </div>
        )}

        {stats && (
          <div className="mt-6 bg-[#111827] border border-[#1f2937] rounded-2xl p-5">
            <h2 className="text-white font-semibold mb-4">Threat Level Breakdown</h2>
            <div className="flex gap-3 flex-wrap">
              {[
                { level: "CRITICAL", count: stats.critical, cls: "threat-CRITICAL" },
                { level: "HIGH", count: stats.high, cls: "threat-HIGH" },
                { level: "MEDIUM", count: stats.medium, cls: "threat-MEDIUM" },
                { level: "LOW", count: stats.low, cls: "threat-LOW" },
              ].map(t => (
                <span key={t.level} className={`px-3 py-1 rounded-full text-sm font-medium border ${t.cls}`}>
                  {t.level}: {t.count}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
