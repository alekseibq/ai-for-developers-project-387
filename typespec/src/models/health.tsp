model HealthResponse {
  status: "ok" | "degraded";
  version: string;
  database: "connected" | "disconnected";
  uptime: float64;
}
