"use client";
import { useEffect, useState } from "react";
import { Shield, Clock, Film } from "lucide-react";

const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

interface Incident {
  id: string;
  created_at: string;
  video_filename: string;
  threat_level: string;
  confidence_score: number;
  violence_detected: boolean;
  detection_summary: string;
}

export default function IncidentsPage() {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${BACKEND}/api/v1/incidents/`)
      .then(r => r.json())
      .then(d => setIncidents(d.incidents || []))
      .catch(() => setIncidents([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="min-h-screen bg-[#0a0f1e] p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-2">Incident History</h1>
        <p className="text-gray-400 mb-8">All recorded security incidents</p>

        {loading && <p className="text-gray-500">Loading incidents...</p>}

        {!loading && incidents.length === 0 && (
          <div className="bg-[#111827] border border-[#1f2937] rounded-2xl p-12 text-center">
            <Shield className="w-12 h-12 text-gray-600 mx-auto mb-3" />
            <p className="text-gray-400">No incidents recorded yet.</p>
            <p className="text-gray-600 text-sm mt-1">Upload a video to get started.</p>
          </div>
        )}

        <div className="space-y-3">
          {incidents.map(inc => (
            <div key={inc.id} className="bg-[#111827] border border-[#1f2937] rounded-2xl p-5 flex items-start gap-4">
              <div className={`px-2 py-1 rounded-lg text-xs font-bold border threat-${inc.threat_level}`}>
                {inc.threat_level}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <Film className="w-4 h-4 text-gray-500" />
                  <p className="text-white font-medium truncate">{inc.video_filename}</p>
                </div>
                <p className="text-gray-400 text-sm truncate">{inc.detection_summary}</p>
                <div className="flex items-center gap-3 mt-2 text-xs text-gray-500">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {new Date(inc.created_at).toLocaleString()}
                  </span>
                  <span>Confidence: {(inc.confidence_score * 100).toFixed(1)}%</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
