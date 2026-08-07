import { useEffect, useState } from "react";
import { getStatsSummary } from "./api";
import type { StatsSummary } from "./types";
import PulseHeader from "./components/PulseHeader";
import StatsCards from "./components/StatsCards";
import SourceChart from "./components/SourceChart";
import UrlScanner from "./components/UrlScanner";
import IndicatorsTable from "./components/IndicatorsTable";

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
        <StatsCards stats={stats} />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-4">
          <div className="lg:col-span-2">
            <SourceChart stats={stats} />
          </div>
          <UrlScanner />
        </div>
        <IndicatorsTable />
      </div>
    </div>
  );
}

export default App;