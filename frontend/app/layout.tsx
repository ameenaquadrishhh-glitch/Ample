import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AMPLE — Security Operations Platform",
  description: "Agentic Monitoring and Proactive Law Enforcement Engine",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
