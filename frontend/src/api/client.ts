import type { Result, HealthResponse } from "@/types/generated";

const BASE = import.meta.env.VITE_API_BASE ?? "/api/v1";

async function request<T>(path: string): Promise<Result<T>> {
  const res = await fetch(`${BASE}${path}`);
  return res.json() as Promise<Result<T>>;
}

async function post<T>(path: string, body: unknown): Promise<Result<T>> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return res.json() as Promise<Result<T>>;
}

export function getHealth(): Promise<Result<HealthResponse>> {
  return request<HealthResponse>("/health");
}

export { request, post };
