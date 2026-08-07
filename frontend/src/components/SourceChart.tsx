import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import type { StatsSummary } from "../types";

interface SourceChartProps {
  stats: StatsSummary | null;
}

function SourceChart({ stats }: SourceChartProps) {
  if (!stats) return null;

  const data = Object.entries(stats.by_source).map(([source, count]) => ({ source, count }));

  return (
    <div className="bg-surface border border-border-subtle rounded-xl p-5 h-full">
      <p className="font-mono text-[11px] uppercase tracking-[0.15em] text-text-muted mb-4">
        Répartition par source
      </p>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1F2A40" vertical={false} />
          <XAxis dataKey="source" stroke="#7C8AA3" fontSize={12} tickLine={false} axisLine={{ stroke: "#1F2A40" }} />
          <YAxis stroke="#7C8AA3" fontSize={12} tickLine={false} axisLine={false} />
          <Tooltip
            cursor={{ fill: "#1F2A40", opacity: 0.4 }}
            contentStyle={{ backgroundColor: "#121B2E", border: "1px solid #1F2A40", borderRadius: 8, fontSize: 12 }}
            labelStyle={{ color: "#E4EAF2" }}
          />
          <Bar dataKey="count" fill="#2AC9B5" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default SourceChart;