import StatsCards from "../components/StatsCards";
import SourceChart from "../components/SourceChart";
import UrlScanner from "../components/UrlScanner";
import type { StatsSummary } from "../types";

interface DashboardPageProps {
  stats: StatsSummary | null;
}

function DashboardPage({ stats }: DashboardPageProps) {
  return (
    <>
      <StatsCards stats={stats} />
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2">
          <SourceChart stats={stats} />
        </div>
        <UrlScanner />
      </div>
    </>
  );
}

export default DashboardPage;