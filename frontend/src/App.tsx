import { useCallback, useEffect, useState } from "react";
import GuidePanel from "./components/GuidePanel";
import ImageUpload from "./components/ImageUpload";
import Onboarding from "./components/Onboarding";
import ResultView from "./components/ResultView";
import {
  AgentMeta,
  RunResponse,
  fetchAgents,
  fetchHealth,
  runAgent,
} from "./lib/api";

const CATEGORIES: Record<string, string> = {
  dev: "Dev & Code",
  career: "Carrière",
  product: "Produit",
  ai: "IA / ML",
  content: "Contenu",
  security: "Sécurité",
  vision: "Vision · Gemma 4 31B",
};

const MODEL_LABELS: Record<string, string> = {
  "zai-glm-4.7": "GLM 4.7",
  "gpt-oss-120b": "GPT OSS 120B",
  "gemma-4-31b": "Gemma 4 31B",
};

export default function App() {
  const [agents, setAgents] = useState<AgentMeta[]>([]);
  const [selected, setSelected] = useState<string>("review");
  const [input, setInput] = useState("");
  const [images, setImages] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<RunResponse | null>(null);
  const [health, setHealth] = useState({ ok: false, cerebras_key: false, next_available_in_sec: 0 });
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [booting, setBooting] = useState(true);

  const current = agents.find((a) => a.id === selected);

  const refreshHealth = useCallback(async () => {
    try {
      const h = await fetchHealth();
      setHealth(h);
    } catch {
      setHealth({ ok: false, next_available_in_sec: 0 } as never);
    }
  }, []);

  useEffect(() => {
    fetchAgents().then((list) => {
      setAgents(list);
      if (list.length) setSelected(list[0].id);
    });
    void refreshHealth().finally(() => setBooting(false));
    const t = setInterval(refreshHealth, 2000);
    return () => clearInterval(t);
  }, [refreshHealth]);

  useEffect(() => {
    if (booting) return;
    const done = localStorage.getItem("flash-onboarding-v1");
    if (!health.cerebras_key || !done) setShowOnboarding(true);
  }, [booting, health.cerebras_key]);

  const canRun =
    current &&
    !loading &&
    health.ok &&
    (current.requires_image ? images.length > 0 : input.trim().length >= 3);

  async function handleRun() {
    if (!canRun) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await runAgent(selected, input, images);
      setResult(res);
      refreshHealth();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Erreur inconnue");
    } finally {
      setLoading(false);
    }
  }

  const grouped = agents.reduce<Record<string, AgentMeta[]>>((acc, a) => {
    (acc[a.category] ??= []).push(a);
    return acc;
  }, {});

  if (booting) {
    return (
      <div className="boot">
        <span>⚡ Flash Agents</span>
        <style>{`.boot { min-height:100vh; display:flex; align-items:center; justify-content:center; color:var(--muted); }`}</style>
      </div>
    );
  }

  return (
    <div className="app">
      {showOnboarding && (
        <Onboarding
          hasKey={health.cerebras_key}
          onComplete={() => {
            setShowOnboarding(false);
            localStorage.setItem("flash-onboarding-v1", "1");
            void refreshHealth();
          }}
        />
      )}
      <header className="header">
        <div className="header-left">
          <h1>
            <span className="logo">⚡</span> Flash Agents
          </h1>
          <p className="subtitle">Agents ultra-rapides propulsés par Cerebras Inference</p>
        </div>
        <div className="header-right">
          <span className={`status ${health.ok ? "on" : "off"}`}>
            {health.ok ? "● Cerebras connecté" : "○ Clé API manquante"}
          </span>
          {health.next_available_in_sec > 0 && (
            <span className="cooldown">
              Prochain appel dans {Math.ceil(health.next_available_in_sec)}s
            </span>
          )}
          <button
            type="button"
            className="settings-link"
            onClick={() => setShowOnboarding(true)}
          >
            Clé API / aide
          </button>
        </div>
      </header>

      <div className="layout">
        <aside className="sidebar">
          {Object.entries(grouped).map(([cat, list]) => (
            <div key={cat} className="cat-group">
              <h2 className="cat-label">{CATEGORIES[cat] ?? cat}</h2>
              {list.map((a) => (
                <button
                  key={a.id}
                  className={`agent-btn ${selected === a.id ? "active" : ""}`}
                  onClick={() => {
                    setSelected(a.id);
                    setResult(null);
                    setError(null);
                    setImages([]);
                  }}
                >
                  <span className="agent-icon">{a.icon}</span>
                  <span className="agent-info">
                    <span className="agent-name">{a.name}</span>
                    <span className="agent-model">{MODEL_LABELS[a.model] ?? a.model}</span>
                  </span>
                </button>
              ))}
            </div>
          ))}
        </aside>

        <main className="main">
          {current && (
            <>
              <div className="agent-header">
                <h2>
                  {current.icon} {current.name}
                </h2>
                <p>{current.tagline}</p>
                <span className="model-badge">{MODEL_LABELS[current.model]}</span>
              </div>

              <GuidePanel
                title="Comment l'utiliser"
                steps={current.how_to ?? []}
                variant="how"
              />

              {current.requires_image && (
                <ImageUpload
                  images={images}
                  maxImages={current.max_images ?? 5}
                  onChange={setImages}
                />
              )}

              <textarea
                className="input"
                placeholder={current.placeholder}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                rows={current.requires_image ? 4 : 10}
              />

              <button
                className="run-btn"
                onClick={handleRun}
                disabled={!canRun}
              >
                {loading ? "Inférence en cours…" : "Lancer ⚡"}
              </button>

              {error && <div className="error">{error}</div>}

              {result && (
                <div className="output">
                  <div className="metrics">
                    <span className="metric highlight">
                      {result.latency_ms} ms
                    </span>
                    <span className="metric">modèle {result.model}</span>
                    {result.queue_wait_ms > 0 && (
                      <span className="metric">file {result.queue_wait_ms} ms</span>
                    )}
                  </div>
                  <ResultView data={result.result} />
                  <GuidePanel
                    title="Et ensuite ?"
                    steps={result.next_steps}
                    variant="next"
                  />
                </div>
              )}
            </>
          )}
        </main>
      </div>

      <footer className="footer">
        Open source ·{" "}
        <a href="https://inference-docs.cerebras.ai" target="_blank" rel="noreferrer">
          Cerebras Inference
        </a>
        {" · "}1 tâche = 1 appel · Rate-safe
      </footer>

      <style>{`
        .app { display: flex; flex-direction: column; min-height: 100vh; }
        .header {
          display: flex; justify-content: space-between; align-items: flex-start;
          padding: 1.5rem 2rem; border-bottom: 1px solid var(--border);
          background: var(--surface);
        }
        .header h1 { font-size: 1.5rem; font-weight: 700; display: flex; align-items: center; gap: 0.5rem; }
        .logo { color: var(--accent); }
        .subtitle { color: var(--muted); font-size: 0.875rem; margin-top: 0.25rem; }
        .header-right { display: flex; flex-direction: column; align-items: flex-end; gap: 0.25rem; font-size: 0.8rem; }
        .status.on { color: var(--green); }
        .status.off { color: var(--red); }
        .cooldown { color: var(--yellow); font-family: var(--mono); }
        .settings-link {
          margin-top: 0.35rem; background: none; border: none; color: var(--muted);
          font-size: 0.75rem; cursor: pointer; text-decoration: underline;
        }
        .settings-link:hover { color: var(--accent); }

        .layout { display: flex; flex: 1; }
        .sidebar {
          width: 280px; flex-shrink: 0; border-right: 1px solid var(--border);
          padding: 1rem 0.75rem; overflow-y: auto; background: var(--surface);
        }
        .cat-group { margin-bottom: 1.25rem; }
        .cat-label {
          font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.08em;
          color: var(--muted); padding: 0 0.5rem; margin-bottom: 0.5rem;
        }
        .agent-btn {
          display: flex; align-items: center; gap: 0.75rem; width: 100%;
          padding: 0.6rem 0.75rem; border: none; border-radius: 8px;
          background: transparent; color: var(--text); cursor: pointer;
          text-align: left; transition: background 0.15s;
        }
        .agent-btn:hover { background: var(--surface-2); }
        .agent-btn.active { background: var(--accent-dim); border: 1px solid var(--accent); }
        .agent-icon { font-size: 1.25rem; }
        .agent-info { display: flex; flex-direction: column; }
        .agent-name { font-size: 0.875rem; font-weight: 600; }
        .agent-model { font-size: 0.7rem; color: var(--muted); font-family: var(--mono); }

        .main { flex: 1; padding: 1.5rem 2rem; overflow-y: auto; max-width: 900px; }
        .agent-header { margin-bottom: 1.25rem; }
        .agent-header h2 { font-size: 1.25rem; margin-bottom: 0.25rem; }
        .agent-header p { color: var(--muted); font-size: 0.9rem; }
        .model-badge {
          display: inline-block; margin-top: 0.5rem; padding: 0.2rem 0.6rem;
          background: var(--accent-dim); color: var(--accent); border-radius: 4px;
          font-size: 0.75rem; font-family: var(--mono); font-weight: 500;
        }

        .input {
          width: 100%; padding: 1rem; border-radius: 10px;
          border: 1px solid var(--border); background: var(--surface);
          color: var(--text); font-family: var(--mono); font-size: 0.85rem;
          resize: vertical; line-height: 1.6;
        }
        .input:focus { outline: none; border-color: var(--accent); }

        .run-btn {
          margin-top: 1rem; padding: 0.75rem 2rem; border: none; border-radius: 8px;
          background: var(--accent); color: #fff; font-weight: 600; font-size: 1rem;
          cursor: pointer; transition: opacity 0.15s;
        }
        .run-btn:hover:not(:disabled) { opacity: 0.9; }
        .run-btn:disabled { opacity: 0.4; cursor: not-allowed; }

        .error {
          margin-top: 1rem; padding: 0.75rem 1rem; border-radius: 8px;
          background: #ff5c5c22; border: 1px solid var(--red); color: var(--red);
          font-size: 0.85rem;
        }

        .output { margin-top: 2rem; }
        .metrics {
          display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap;
        }
        .metric {
          font-family: var(--mono); font-size: 0.8rem; color: var(--muted);
          padding: 0.35rem 0.75rem; background: var(--surface); border-radius: 6px;
          border: 1px solid var(--border);
        }
        .metric.highlight {
          color: var(--accent); font-weight: 600; font-size: 1.1rem;
          border-color: var(--accent);
        }

        .results { display: flex; flex-direction: column; gap: 1.25rem; }
        .result-section {
          padding: 1rem 1.25rem; background: var(--surface); border-radius: 10px;
          border: 1px solid var(--border);
        }
        .result-key {
          font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em;
          color: var(--accent); margin-bottom: 0.5rem; font-family: var(--mono);
        }
        .result-val { font-size: 0.95rem; }
        .list { padding-left: 1.25rem; }
        .list li { margin-bottom: 0.35rem; }
        .nested { display: flex; flex-direction: column; gap: 0.5rem; }
        .nested-card {
          padding: 0.75rem; background: var(--surface-2); border-radius: 6px;
        }
        .row { display: flex; gap: 0.75rem; margin-bottom: 0.35rem; flex-wrap: wrap; }
        .key {
          font-family: var(--mono); font-size: 0.8rem; color: var(--muted);
          min-width: 120px; flex-shrink: 0;
        }
        .val { flex: 1; }
        .code-block {
          font-family: var(--mono); font-size: 0.8rem; white-space: pre-wrap;
          background: var(--bg); padding: 0.75rem; border-radius: 6px; margin-top: 0.25rem;
        }
        .muted { color: var(--muted); }
        .ok { color: var(--green); }
        .warn { color: var(--yellow); }
        .num { color: var(--accent); font-family: var(--mono); }

        .footer {
          padding: 1rem 2rem; border-top: 1px solid var(--border);
          font-size: 0.8rem; color: var(--muted); text-align: center;
        }
        .footer a { color: var(--accent); text-decoration: none; }
      `}</style>
    </div>
  );
}