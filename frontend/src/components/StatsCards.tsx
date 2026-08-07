import type { StatsSummary } from "../types";

interface StatsCardsProps {
  stats: StatsSummary | null;
}

const accentClass: Record<string, string> = {
  signal: "after:bg-signal",
  safe: "after:bg-safe",
  warning: "after:bg-warning",
};

function StatsCards({ stats }: StatsCardsProps) {
  if (!stats) return null;

  const cards = [
    { label: "Indicateurs totaux", value: stats.total_indicators, accent: "signal" },
    { label: "Sources actives", value: Object.keys(stats.by_source).length, accent: "safe" },
    { label: "Types de menaces", value: Object.keys(stats.by_type).length, accent: "warning" },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
      {cards.map((card) => (
        <div
          key={card.label}
          className={`relative bg-surface border border-border-subtle rounded-xl p-5 overflow-hidden after:absolute after:bottom-0 after:left-0 after:h-0.5 after:w-full ${accentClass[card.accent]}`}
        >
          <p className="font-mono text-[11px] uppercase tracking-[0.15em] text-text-muted mb-2">
            {card.label}
          </p>
          <p className="font-mono text-3xl font-semibold text-text-primary">{card.value}</p>
        </div>
      ))}
    </div>
  );
}

export default StatsCards;