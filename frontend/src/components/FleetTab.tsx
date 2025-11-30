import React, { useEffect, useState } from "react";
import { fetchJson } from "../api";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

interface HeatRow {
  rack: string;
  low: number;
  medium: number;
  high: number;
}

interface ReplacementItem {
  asset_id: string;
  component_id: string;
  component_type: string;
  risk_level: string;
  predicted_dul_days: number;
  replacement_date: string;
  capex_estimate: number;
}

export const FleetTab: React.FC = () => {
  const [heat, setHeat] = useState<HeatRow[]>([]);
  const [replacements, setReplacements] = useState<ReplacementItem[]>([]);

  useEffect(() => {
    fetchJson("/api/fleet/heatmap")
      .then((res) => setHeat(res.rows))
      .catch(console.error);
    fetchJson("/api/fleet/replacements")
      .then((res) => setReplacements(res.items))
      .catch(console.error);
  }, []);

  const labels = heat.map((h) => h.rack);
  const data = {
    labels,
    datasets: [
      { label: "Low", data: heat.map((h) => h.low), stack: "stack1" },
      { label: "Medium", data: heat.map((h) => h.medium), stack: "stack1" },
      { label: "High", data: heat.map((h) => h.high), stack: "stack1" },
    ],
  };

  return (
    <div>
      <h1 style={{ marginBottom: 16 }}>Fleet</h1>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1.2fr 1fr",
          gap: 16,
          alignItems: "flex-start",
        }}
      >
        <div
          style={{
            background: "white",
            padding: 16,
            borderRadius: 8,
            boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
          }}
        >
          <h2 style={{ marginBottom: 12 }}>Rack Risk Heatmap</h2>
          <Bar data={data} />
        </div>
        <div
          style={{
            background: "white",
            padding: 16,
            borderRadius: 8,
            boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
            maxHeight: 360,
            overflow: "auto",
          }}
        >
          <h2 style={{ marginBottom: 12 }}>Upcoming Replacements</h2>
          <table style={{ width: "100%", fontSize: 12, borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th align="left">Asset</th>
                <th align="left">Component</th>
                <th align="left">Type</th>
                <th align="left">Risk</th>
                <th align="right">DUL (days)</th>
                <th align="right">CapEx</th>
              </tr>
            </thead>
            <tbody>
              {replacements.map((r, idx) => (
                <tr key={idx}>
                  <td>{r.asset_id}</td>
                  <td>{r.component_id}</td>
                  <td>{r.component_type}</td>
                  <td>{r.risk_level}</td>
                  <td align="right">{r.predicted_dul_days}</td>
                  <td align="right">{r.capex_estimate.toFixed(0)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
