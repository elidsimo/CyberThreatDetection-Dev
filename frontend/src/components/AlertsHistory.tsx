import { useEffect, useState } from "react";
import { getAlerts } from "../api";
import type { ThreatIndicator } from "../types";

function AlertsHistory() {
  const [alerts, setAlerts] = useState<ThreatIndicator[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const data = await getAlerts(20);
        setAlerts(data.results);
      } catch (err) {
        console.error("Erreur de récupération des alertes :", err);
      } finally {
        setLoading(false);
      }
    };
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 20000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-surface border border-border-subtle rounded-xl p-5">
      <div className="flex items-center justify-between mb-4">
        <p className="font-mono text-[11px] uppercase tracking-[0.15em] text-text-muted">
          Historique des alertes
        </p>
        <span className="font-mono text-[11px] text-text-muted">{alerts.length} notifiée(s)</span>
      </div>

      {loading ? (
        <p className="font-body text-sm text-text-muted py-6">Chargement...</p>
      ) : alerts.length === 0 ? (
        <p className="font-body text-sm text-text-muted py-6">Aucune alerte envoyée pour l'instant.</p>
      ) : (
        <ul className="divide-y divide-border-subtle/60">
          {alerts.map((item, index) => (
            <li key={index} className="py-3 flex items-center justify-between gap-4">
              <div className="flex items-center gap-3 min-w-0">
                <span className="h-2 w-2 rounded-full bg-critical shrink-0" />
                <div className="min-w-0">
                  <p className="font-mono text-sm text-text-primary truncate">{item.indicator_value}</p>
                  <p className="font-body text-xs text-text-muted">
                    {item.source} · score {item.severity_score}
                  </p>
                </div>
              </div>
              <span className="font-mono text-[11px] text-text-muted whitespace-nowrap">
                {new Date(item.detected_at).toLocaleString("fr-FR")}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default AlertsHistory;