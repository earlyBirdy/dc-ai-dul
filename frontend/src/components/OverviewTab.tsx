import React, { useEffect, useState } from "react";
import { fetchJson } from "../api";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Legend);

interface FleetSummary {
  generated_at: string;
  total_assets: number;
  total_components: number;
  avg_dul_days: number;
  risk_breakdown: { red: number; orange: number; green: number };
}

export const OverviewTab: React.FC = () => {
  const [summary, setSummary] = useState<FleetSummary | null>(null);
  const [labels, setLabels] = useState<string[]>([]);
  const [values, setValues] = useState<number[]>([]);

  useEffect(() => {
    fetchJson("/api/fleet/summary").then(setSummary).catch(console.error);
    fetchJson("/api/fleet/dul_trend")
      .then((res) => {
        setLabels(res.dates);
        setValues(res.avg_dul_days);
      })
      .catch(console.error);
  }, []);

  const chartData = {
    labels,
    datasets: [
      {
        label: "Average DUL (days)",
        data: values,
        borderWidth: 2,
        tension: 0.25,
      },
    ],
  };

  return (
    <div>
      <h1 style={{ marginBottom: 16 }}>Overview</h1>
      {summary && (
        <div style={{ display: "flex", gap: 16, marginBottom: 24 }}>
          <Card title="Assets">{summary.total_assets}</Card>
          <Card title="Components">{summary.total_components}</Card>
          <Card title="Avg DUL (days)">{summary.avg_dul_days.toFixed(1)}</Card>
          <Card title="Risk (R / O / G)">
            {summary.risk_breakdown.red} / {summary.risk_breakdown.orange} /{" "}
            {summary.risk_breakdown.green}
          </Card>
        </div>
      )}
      <div style={{ background: "white", padding: 16, borderRadius: 8, boxShadow: "0 1px 3px rgba(0,0,0,0.1)" }}>
        <h2 style={{ marginBottom: 12 }}>Fleet DUL Trend</h2>
        <Line data={chartData} />
      </div>
    </div>
  );
};

const Card: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => (
  <div
    style={{
      flex: 1,
      background: "white",
      borderRadius: 8,
      padding: 16,
      boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
    }}
  >
    <div style={{ fontSize: 12, color: "#6B7280" }}>{title}</div>
    <div style={{ fontSize: 20, fontWeight: 600, marginTop: 4 }}>{children}</div>
  </div>
);
