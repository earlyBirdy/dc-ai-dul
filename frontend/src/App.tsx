import React, { useState } from "react";
import { Layout } from "./components/Layout";
import { OverviewTab } from "./components/OverviewTab";
import { FleetTab } from "./components/FleetTab";
import { DocsTab } from "./components/DocsTab";
import { SettingsTab } from "./components/SettingsTab";

type TabKey = "overview" | "fleet" | "docs" | "settings";

const App: React.FC = () => {
  const [tab, setTab] = useState<TabKey>("overview");

  let content: JSX.Element;
  switch (tab) {
    case "fleet":
      content = <FleetTab />;
      break;
    case "docs":
      content = <DocsTab />;
      break;
    case "settings":
      content = <SettingsTab />;
      break;
    case "overview":
    default:
      content = <OverviewTab />;
  }

  return <Layout active={tab} onChange={setTab}>{content}</Layout>;
};

export default App;
