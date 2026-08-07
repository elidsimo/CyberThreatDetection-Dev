import { useEffect, useState } from "react";
import { getIndicators } from "../api";
import type { ThreatIndicator } from "../types";

const badgeClass: Record<string, string> = {
  ip: "bg-signal/15 text-signal",
  hash: "bg-critical/15 text-critical",
  phishing_url: "bg-warning/15 text-warning",
};

function IndicatorsTable() {
  const [indicators, setIndicators] = useState<ThreatIndicator[]>([]);
  const [sourceFilter, setSourceFilter] = useState("");
  const [typeFilter, setTypeFilter] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchIndicators = async () => {
      setLoading(true);
      try {
        const params: Record<string, string | number> = { limit: 15 };
        if (sourceFilter) params.source = sourceFilter;
        if (typeFilter) params.indicator_type = typeFilter;
        const data = await getIndicators(params);
        setIndicators(data.results);
      } catch (err) {
        console.error("Erreur de récupération des indicateurs :", err);
      } finally {
        setLoading(false);
      }
    };
    fetchIndicators();
  }, [sourceFilter, typeFilter]);

  const selectClass =
    "bg-bg-deep border border-border-subtle rounded-lg px-3 py-1.5 text-xs text-text-primary font-mono focus:outline-none focus:ring-2 focus:ring-signal";

  return (
    <div className="bg-surface border border-border-subtle rounded-xl p-5">
      <div className="flex items-center justify-between mb-4 flex-wrap gap-3">
        <p className="font-mono text-[11px] uppercase tracking-[0.15em] text-text-muted">
          Derniers indicateurs
        </p>
        <div className="flex gap-2">
          <select value={sourceFilter} onChange={(e) => setSourceFilter(e.target.value)} className={selectClass}>
            <option value="">Toutes les sources</option>
            <option value="AbuseIPDB">AbuseIPDB</option>
            <option value="MalwareBazaar">MalwareBazaar</option>
            <option value="URLhaus">URLhaus</option>
            <option value="OpenPhish">OpenPhish</option>
          </select>
          <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)} className={selectClass}>
            <option value="">Tous les types</option>
            <option value="ip">IP</option>
            <option value="hash">Hash</option>
            <option value="phishing_url">URL de phishing</option>
          </select>
        </div>
      </div>

      {loading ? (
        <p className="font-body text-sm text-text-muted py-6">Chargement...</p>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-text-muted font-mono text-[11px] uppercase tracking-wider border-b border-border-subtle">
                <th className="pb-2 font-medium">Type</th>
                <th className="pb-2 font-medium">Valeur</th>
                <th className="pb-2 font-medium">Source</th>
                <th className="pb-2 font-medium">Score</th>
                <th className="pb-2 font-medium">Détecté le</th>
              </tr>
            </thead>
            <tbody>
              {indicators.map((item, index) => (
                <tr key={index} className="border-b border-border-subtle/60 last:border-0">
                  <td className="py-2">
                    <span
                      className={`px-2 py-0.5 rounded text-[11px] font-mono uppercase ${
                        badgeClass[item.indicator_type] ?? "bg-text-muted/15 text-text-muted"
                      }`}
                    >
                      {item.indicator_type}
                    </span>
                  </td>
                  <td className="py-2 font-mono text-text-primary">{item.indicator_value}</td>
                  <td className="py-2 text-text-muted">{item.source}</td>
                  <td className="py-2 font-mono text-text-primary">{item.severity_score}</td>
                  <td className="py-2 text-text-muted">
                    {new Date(item.detected_at).toLocaleString("fr-FR")}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default IndicatorsTable;