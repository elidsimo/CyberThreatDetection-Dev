interface PulseHeaderProps {
  lastUpdated: Date | null;
}

function PulseHeader({ lastUpdated }: PulseHeaderProps) {
  return (
    <header className="mb-10">
      <div className="flex items-end justify-between flex-wrap gap-4">
        <div>
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-signal mb-2">
            CMRPI · Espace Maroc Cyberconfiance
          </p>
          <h1 className="font-display text-3xl font-semibold text-text-primary tracking-tight">
            CyberThreat Detection
          </h1>
          <p className="font-body text-sm text-text-muted mt-1">
            Détection et alerte précoce des cybermenaces ciblant les PME
          </p>
        </div>
        <div className="flex flex-col items-end gap-2">
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-safe animate-pulse" />
            <span className="font-mono text-xs uppercase tracking-widest text-text-muted">
              Surveillance active
            </span>
          </div>
          {lastUpdated && (
            <span className="font-mono text-xs text-text-muted">
              Maj {lastUpdated.toLocaleTimeString("fr-FR")}
            </span>
          )}
        </div>
      </div>
      <div className="signal-bar h-px w-full mt-6" />
    </header>
  );
}

export default PulseHeader;