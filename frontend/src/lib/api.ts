export interface AgentMeta {
  id: string;
  name: string;
  tagline: string;
  model: string;
  category: string;
  icon: string;
  placeholder: string;
  requires_image: boolean;
  max_images: number;
  how_to: string[];
  next_steps: string[];
}

export interface RunResponse {
  agent_id: string;
  agent_name: string;
  model: string;
  result: Record<string, unknown>;
  latency_ms: number;
  queue_wait_ms: number;
  rate_headers: Record<string, string>;
  next_available_in_sec: number;
  how_to: string[];
  next_steps: string[];
}

export async function fetchAgents(): Promise<AgentMeta[]> {
  const r = await fetch("/api/agents");
  const data = await r.json();
  return data.agents;
}

export async function runAgent(
  agentId: string,
  input: string,
  images: string[] = []
): Promise<RunResponse> {
  const r = await fetch("/api/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ agent_id: agentId, input, images }),
  });
  if (!r.ok) {
    const err = await r.text();
    throw new Error(err || `HTTP ${r.status}`);
  }
  return r.json();
}

export async function fetchHealth(): Promise<{
  ok: boolean;
  cerebras_key: boolean;
  env_file?: string;
  next_available_in_sec: number;
  rate_interval_sec: number;
}> {
  const r = await fetch("/api/health");
  return r.json();
}

export async function saveApiKey(apiKey: string): Promise<void> {
  const r = await fetch("/api/setup/key", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ api_key: apiKey }),
  });
  if (!r.ok) {
    const data = await r.json().catch(() => ({}));
    const detail = data.detail;
    throw new Error(
      typeof detail === "string" ? detail : Array.isArray(detail) ? detail[0]?.msg : `HTTP ${r.status}`
    );
  }
}