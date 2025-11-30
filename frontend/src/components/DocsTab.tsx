import React, { useEffect, useState } from "react";
import { fetchJson } from "../api";

interface DocSection {
  title: string;
  body: string;
}

export const DocsTab: React.FC = () => {
  const [sections, setSections] = useState<DocSection[]>([]);

  useEffect(() => {
    fetchJson("/api/docs/summary")
      .then((res) => setSections(res.sections))
      .catch(console.error);
  }, []);

  return (
    <div>
      <h1 style={{ marginBottom: 16 }}>Docs</h1>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        {sections.map((s, idx) => (
          <div
            key={idx}
            style={{
              background: "white",
              padding: 16,
              borderRadius: 8,
              boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
            }}
          >
            <h2 style={{ marginBottom: 8 }}>{s.title}</h2>
            <p style={{ fontSize: 14, color: "#374151", whiteSpace: "pre-wrap" }}>{s.body}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
