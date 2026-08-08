import { useEffect, useState } from "react";
import { Routes, Route } from "react-router-dom";
import { getStatsSummary } from "./api";
import type { StatsSummary } from "./types";
import PulseHeader from "./components/PulseHeader";
import NavBar from "./components/NavBar";
import DashboardPage from "./pages/DashboardPage";
import IndicatorsPage from "./pages/IndicatorsPage";
import AlertsPage from "./pages/AlertsPage";

const REFRESH_INTERVAL_MS = 20000;

function App() {
  const [stats, setStats] = useState<StatsSummary | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await getStatsSummary();
        setStats(data);
        setLastUpdated(new Date());
      } catch (err) {
        console.error("Erreur de récupération des statistiques :", err);
      }
    };
    fetchStats();
    const interval = setInterval(fetchStats, REFRESH_INTERVAL_MS);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-bg-deep font-body">
      <div className="max-w-6xl mx-auto px-6 py-10">
        <PulseHeader lastUpdated={lastUpdated} />
        <NavBar />
        <Routes>
          <Route path="/" element={<DashboardPage stats={stats} />} />
          <Route path="/indicators" element={<IndicatorsPage />} />
          <Route path="/alerts" element={<AlertsPage />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;