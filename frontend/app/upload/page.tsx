"use client";
import { useState, useRef } from "react";
import { Upload, Loader2, CheckCircle, AlertTriangle } from "lucide-react";

const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle"|"uploading"|"done"|"error">("idle");
  const [result, setResult] = useState<any>(null);
  const ref = useRef<HTMLInputElement>(null);

  const handleUpload = async () => {
    if (!file) return;
    setStatus("uploading");
    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch(`${BACKEND}/api/v1/video/upload`, { method: "POST", body: form });
      const data = await res.json();
      setResult(data);
      setStatus("done");
    } catch {
      setStatus("error");
    }
  };

  return (
    <main className="min-h-screen bg-[#0a0f1e] p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-2">Analyze Video</h1>
        <p className="text-gray-400 mb-8">Upload CCTV footage for AI-powered violence detection</p>

        {/* Drop zone */}
        <div
          onClick={() => ref.current?.click()}
          className="border-2 border-dashed border-[#1f2937] hover:border-blue-500 rounded-2xl p-12 text-center cursor-pointer transition-colors"
        >
          <Upload className="w-10 h-10 text-gray-500 mx-auto mb-3" />
          <p className="text-gray-400">{file ? file.name : "Click to select a video file"}</p>
          <p className="text-gray-600 text-sm mt-1">MP4, AVI, MOV supported</p>
          <input ref={ref} type="file" accept="video/*" className="hidden" onChange={e => setFile(e.target.files?.[0] || null)} />
        </div>

        {file && status === "idle" && (
          <button onClick={handleUpload} className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-xl transition-colors">
            Run Analysis
          </button>
        )}

        {status === "uploading" && (
          <div className="mt-4 flex items-center gap-2 text-blue-400">
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>Analyzing video... this may take a moment</span>
          </div>
        )}

        {status === "done" && result && (
          <div className="mt-6 bg-[#111827] border border-[#1f2937] rounded-2xl p-6 space-y-4">
            <div className="flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-green-400" />
              <span className="text-white font-semibold">Analysis Complete</span>
            </div>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div className="bg-[#0a0f1e] rounded-xl p-3">
                <p className="text-gray-400">Threat Level</p>
                <p className="text-white font-bold text-lg">{result.detection?.threat_level}</p>
              </div>
              <div className="bg-[#0a0f1e] rounded-xl p-3">
                <p className="text-gray-400">Confidence</p>
                <p className="text-white font-bold text-lg">{(result.detection?.confidence_score * 100).toFixed(1)}%</p>
              </div>
            </div>
            {result.report && (
              <div className="bg-[#0a0f1e] rounded-xl p-4">
                <p className="text-gray-400 text-sm mb-2">AI Incident Report</p>
                <p className="text-gray-300 text-sm whitespace-pre-wrap">{result.report}</p>
              </div>
            )}
          </div>
        )}

        {status === "error" && (
          <div className="mt-4 flex items-center gap-2 text-red-400">
            <AlertTriangle className="w-5 h-5" />
            <span>Analysis failed. Is the backend running?</span>
          </div>
        )}
      </div>
    </main>
  );
}
