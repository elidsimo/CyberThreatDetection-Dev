import { useState } from "react";
import type { FormEvent } from "react";
import { predictPhishingUrl } from "../api";
import type { PhishingPrediction } from "../types";

function UrlScanner() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<PhishingPrediction | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await predictPhishingUrl(url.trim());
      setResult(data);
    } catch (err) {
      setError("Analyse impossible. Vérifiez que l'API est démarrée.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const isPhishing = result?.prediction === "phishing";

  return (
    <div className="bg-surface border border-border-subtle rounded-xl p-5 h-full flex flex-col">
      <p className="font-mono text-[11px] uppercase tracking-[0.15em] text-text-muted mb-4">
        Scanner une URL
      </p>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://exemple.com/page"
          className="flex-1 bg-bg-deep border border-border-subtle rounded-lg px-3 py-2 text-sm text-text-primary font-mono placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-signal"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-signal text-bg-deep font-semibold text-sm rounded-lg px-4 py-2 disabled:opacity-50 transition-opacity"
        >
          {loading ? "..." : "Scanner"}
        </button>
      </form>

      {error && <p className="text-critical text-xs mt-3 font-body">{error}</p>}

      <div className="flex-1 flex items-center justify-center mt-4">
        {result && (
          <div
            className={`w-full rounded-lg border p-4 text-center ${
              isPhishing ? "border-critical/40 bg-critical/10" : "border-safe/40 bg-safe/10"
            }`}
          >
            <p className={`font-display font-semibold text-lg ${isPhishing ? "text-critical" : "text-safe"}`}>
              {isPhishing ? "Phishing détecté" : "URL légitime"}
            </p>
            <p className="font-mono text-xs text-text-muted mt-1">
              Confiance : {(result.confidence * 100).toFixed(1)}%
            </p>
          </div>
        )}
        {!result && !error && (
          <p className="font-body text-xs text-text-muted text-center">
            Entrez une URL pour lancer une analyse en direct via le modèle de détection (Étape 8bis).
          </p>
        )}
      </div>
    </div>
  );
}

export default UrlScanner;