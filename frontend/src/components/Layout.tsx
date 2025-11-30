import React from "react";

type TabKey = "overview" | "fleet" | "docs" | "settings";

interface LayoutProps {
  active: TabKey;
  onChange(tab: TabKey): void;
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ active, onChange, children }) => {
  return (
    <div style={{ display: "flex", minHeight: "100vh", fontFamily: "system-ui, sans-serif" }}>
      <aside
        style={{
          width: 220,
          background: "#111827",
          color: "white",
          padding: "16px 0",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <div style={{ padding: "0 16px 16px", borderBottom: "1px solid #374151" }}>
          <div style={{ fontWeight: 700, fontSize: 18 }}>dc-ai-dul</div>
          <div style={{ fontSize: 12, color: "#9CA3AF" }}>DCIM-style DUL dashboard</div>
        </div>
        <nav style={{ marginTop: 8 }}>
          <NavItem label="Overview" tab="overview" active={active} onClick={onChange} />
          <NavItem label="Fleet" tab="fleet" active={active} onClick={onChange} />
          <NavItem label="Docs" tab="docs" active={active} onClick={onChange} />
          <NavItem label="Settings" tab="settings" active={active} onClick={onChange} />
        </nav>
      </aside>
      <main style={{ flex: 1, background: "#F3F4F6", padding: 24 }}>{children}</main>
    </div>
  );
};

interface NavItemProps {
  label: string;
  tab: TabKey;
  active: TabKey;
  onClick(tab: TabKey): void;
}

const NavItem: React.FC<NavItemProps> = ({ label, tab, active, onClick }) => {
  const isActive = active === tab;
  return (
    <button
      onClick={() => onClick(tab)}
      style={{
        width: "100%",
        textAlign: "left",
        padding: "10px 20px",
        border: "none",
        background: isActive ? "#1F2937" : "transparent",
        color: "white",
        cursor: "pointer",
        fontSize: 14,
      }}
    >
      {label}
    </button>
  );
};
