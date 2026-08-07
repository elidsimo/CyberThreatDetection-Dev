export interface StatsSummary {
  total_indicators: number;
  by_source: Record<string, number>;
  by_type: Record<string, number>;
}

export interface ThreatIndicator {
  indicator_type: string;
  indicator_value: string;
  source: string;
  severity_score: number;
  detected_at: string;
  description: string;
  country: string;
  status: string;
}

export interface IndicatorsResponse {
  count: number;
  results: ThreatIndicator[];
}

export interface PhishingPrediction {
  url: string;
  prediction: "phishing" | "legitime";
  confidence: number;
  features_used: Record<string, number>;
}