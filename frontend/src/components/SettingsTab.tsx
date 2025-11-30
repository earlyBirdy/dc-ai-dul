import React from "react";

export const SettingsTab: React.FC = () => {
  return (
    <div>
      <h1 style={{ marginBottom: 16 }}>Settings</h1>
      <p style={{ fontSize: 14, color: "#374151" }}>
        This is a placeholder for configuring data sources, thresholds, and DUL model options.
      </p>
      <ul>
        <li>Configure DB connection</li>
        <li>Toggle offline / online mode</li>
        <li>Risk thresholds (red / orange / green)</li>
        <li>Model selection (GBR / LSTM / CoxPH)</li>
      </ul>
    </div>
  );
};
