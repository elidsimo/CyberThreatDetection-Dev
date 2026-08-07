import axios from "axios";
import type { StatsSummary, IndicatorsResponse, PhishingPrediction } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const getStatsSummary = () =>
  api.get<StatsSummary>("/stats/summary").then((res) => res.data);

export const getIndicators = (params: Record<string, string | number> = {}) =>
  api.get<IndicatorsResponse>("/indicators", { params }).then((res) => res.data);

export const predictPhishingUrl = (url: string) =>
  api.post<PhishingPrediction>("/predict/phishing-url", { url }).then((res) => res.data);

export default api;