import { useState } from "react";
import { saveApiKey } from "../lib/api";

interface Props {
  onComplete: () => void;
  hasKey?: boolean;
}

const STEPS = ["welcome", "how", "key", "done"] as const;
type Step = (typeof STEPS)[number];

export default function Onboarding({ onComplete, hasKey = false }: Props) {
  const [step, setStep] = useState<Step>("welcome");
  const [apiKey, setApiKey] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [keySavedNow, setKeySavedNow] = useState(false);

  const idx = STEPS.indexOf(step);

  async function handleSaveKey() {
    setLoading(true);
    setError(null);
    try {
      await saveApiKey(apiKey);
      setKeySavedNow(true);
      setStep("done");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Erreur lors de l'enregistrement");
    } finally {
      setLoading(false);
    }
  }

  function finish() {
    localStorage.setItem("flash-onboarding-v1", "1");
    onComplete();
  }

  return (
    <div className="onboarding-overlay">
      <div className="onboarding-card">
        <div className="ob-progress">
          {STEPS.map((s, i) => (
            <span key={s} className={`ob-dot ${i <= idx ? "active" : ""}`} />
          ))}
        </div>

        {step === "welcome" && (
          <>
            <h1>⚡ Bienvenue dans Flash Agents</h1>
            <p className="ob-lead">
              Une suite de <strong>40 agents one-shot</strong> propulsés par{" "}
              <a href="https://inference-docs.cerebras.ai" target="_blank" rel="noreferrer">
                Cerebras Inference
              </a>
              . Chaque agent fait une tâche précise en moins d'une seconde.
            </p>
            <ul className="ob-list">
              <li>Texte → GLM 4.7 & GPT OSS 120B</li>
              <li>Images → Gemma 4 31B (vision)</li>
              <li>1 tâche = 1 appel · rate-safe · 100 % local</li>
            </ul>
            <button className="ob-btn primary" onClick={() => setStep("how")}>
              Continuer →
            </button>
          </>
        )}

        {step === "how" && (
          <>
            <h1>Comment ça marche</h1>
            <div className="ob-steps-grid">
              <div className="ob-step-card">
                <span className="ob-num">1</span>
                <strong>Choisis un agent</strong>
                <p>Review, MVP, OCR, JD… 40 spécialistes.</p>
              </div>
              <div className="ob-step-card">
                <span className="ob-num">2</span>
                <strong>Colle ton input</strong>
                <p>Texte, diff, ou image selon l'agent.</p>
              </div>
              <div className="ob-step-card">
                <span className="ob-num">3</span>
                <strong>Lance ⚡</strong>
                <p>Résultat JSON + chrono ms + « Et ensuite ? »</p>
              </div>
            </div>
            <p className="ob-note">
              Free tier Cerebras ≈ 5 req/min — un délai de 15 s entre chaque run est appliqué
              automatiquement pour éviter les 429.
            </p>
            <div className="ob-nav">
              <button className="ob-btn ghost" onClick={() => setStep("welcome")}>
                ← Retour
              </button>
              <button
                className="ob-btn primary"
                onClick={() => (hasKey ? setStep("done") : setStep("key"))}
              >
                {hasKey ? "C'est bon, j'ai compris →" : "Configurer la clé API →"}
              </button>
            </div>
          </>
        )}

        {step === "key" && hasKey && (
          <>
            <h1>Clé déjà configurée</h1>
            <p className="ob-lead">
              Une clé Cerebras est déjà présente dans ton <code>.env</code> local. Tu peux
              la remplacer ci-dessous ou continuer.
            </p>
            <button className="ob-btn primary" onClick={() => setStep("done")} style={{ marginBottom: "1rem" }}>
              Continuer sans changer →
            </button>
            <hr style={{ border: "none", borderTop: "1px solid var(--border)", margin: "1rem 0" }} />
          </>
        )}

        {step === "key" && (
          <>
            <h1>{hasKey ? "Remplacer la clé API" : "Ta clé API Cerebras"}</h1>
            <p className="ob-lead">
              Flash Agents a besoin d'une clé pour appeler l'API Cerebras. Elle reste{" "}
              <strong>sur ton Mac uniquement</strong>.
            </p>

            <div className="ob-security">
              <h3>Où est stockée la clé ?</h3>
              <ul>
                <li>
                  Fichier <code>projects/flash-agents/.env</code> (gitignoré, permissions 600)
                </li>
                <li>
                  <strong>Pas</strong> dans <code>.venv</code> — ce dossier c'est les paquets Python,
                  pas les secrets
                </li>
                <li>
                  Texte en clair (pas de chiffrement) — seul ton compte macOS peut lire le fichier
                  grâce aux permissions <code>600</code>
                </li>
                <li>Jamais exposée au navigateur après enregistrement</li>
                <li>Le backend proxyfie tous les appels — la clé ne part pas côté client</li>
              </ul>
            </div>

            <p className="ob-link">
              Pas encore de clé ?{" "}
              <a href="https://cloud.cerebras.ai" target="_blank" rel="noreferrer">
                Crée-en une gratuitement sur cloud.cerebras.ai →
              </a>
            </p>

            <label className="ob-label">CEREBRAS_API_KEY</label>
            <input
              className="ob-input"
              type="password"
              placeholder="csk-..."
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              autoComplete="off"
            />

            {error && <div className="ob-error">{error}</div>}

            <div className="ob-nav">
              <button className="ob-btn ghost" onClick={() => setStep("how")}>
                ← Retour
              </button>
              <button
                className="ob-btn primary"
                disabled={apiKey.length < 20 || loading}
                onClick={handleSaveKey}
              >
                {loading ? "Vérification…" : "Enregistrer & valider"}
              </button>
            </div>
          </>
        )}

        {step === "done" && (
          <>
            <h1>✓ C'est prêt</h1>
            <p className="ob-lead">
              {keySavedNow ? (
                <>
                  Ta clé est enregistrée dans <code>projects/flash-agents/.env</code> et validée
                  par Cerebras. Tu peux lancer tes premiers agents.
                </>
              ) : (
                <>
                  Ta clé est déjà dans <code>projects/flash-agents/.env</code>. Tu peux lancer
                  tes premiers agents — ou la remplacer via « Clé API / aide » dans le header.
                </>
              )}
            </p>
            <p className="ob-tip">
              Commence par <strong>Flash Review</strong> (dev) ou{" "}
              <strong>Flash UI Review</strong> (vision + screenshot).
            </p>
            <button className="ob-btn primary" onClick={finish}>
              Entrer dans Flash Agents →
            </button>
          </>
        )}
      </div>

      <style>{`
        .onboarding-overlay {
          position: fixed; inset: 0; z-index: 100;
          background: rgba(5, 5, 8, 0.92);
          display: flex; align-items: center; justify-content: center;
          padding: 1.5rem; overflow-y: auto;
        }
        .onboarding-card {
          max-width: 560px; width: 100%;
          background: var(--surface); border: 1px solid var(--border);
          border-radius: 16px; padding: 2rem;
          box-shadow: 0 24px 80px rgba(0,0,0,0.5);
        }
        .onboarding-card h1 { font-size: 1.5rem; margin-bottom: 0.75rem; }
        .ob-lead { color: var(--muted); line-height: 1.6; margin-bottom: 1.25rem; }
        .ob-lead a { color: var(--accent); }
        .ob-list { padding-left: 1.25rem; margin-bottom: 1.5rem; line-height: 1.8; }
        .ob-progress { display: flex; gap: 0.5rem; margin-bottom: 1.5rem; }
        .ob-dot {
          width: 8px; height: 8px; border-radius: 50%;
          background: var(--border); transition: background 0.2s;
        }
        .ob-dot.active { background: var(--accent); }
        .ob-steps-grid {
          display: grid; gap: 0.75rem; margin-bottom: 1.25rem;
        }
        .ob-step-card {
          padding: 1rem; background: var(--surface-2); border-radius: 10px;
          border: 1px solid var(--border);
        }
        .ob-num {
          display: inline-block; width: 24px; height: 24px; border-radius: 50%;
          background: var(--accent); color: #fff; text-align: center;
          font-size: 0.75rem; font-weight: 700; line-height: 24px; margin-bottom: 0.5rem;
        }
        .ob-step-card p { font-size: 0.85rem; color: var(--muted); margin-top: 0.25rem; }
        .ob-note {
          font-size: 0.8rem; color: var(--yellow); background: #f5c54215;
          padding: 0.75rem 1rem; border-radius: 8px; margin-bottom: 1.25rem;
        }
        .ob-security {
          background: var(--bg); border-radius: 10px; padding: 1rem;
          margin-bottom: 1rem; font-size: 0.85rem;
        }
        .ob-security h3 { font-size: 0.8rem; color: var(--accent); margin-bottom: 0.5rem; }
        .ob-security ul { padding-left: 1.25rem; line-height: 1.7; color: var(--muted); }
        .ob-security code { font-family: var(--mono); font-size: 0.8rem; color: var(--text); }
        .ob-link { font-size: 0.9rem; margin-bottom: 1rem; }
        .ob-link a { color: var(--accent); }
        .ob-label {
          display: block; font-size: 0.75rem; font-family: var(--mono);
          color: var(--muted); margin-bottom: 0.35rem; text-transform: uppercase;
        }
        .ob-input {
          width: 100%; padding: 0.75rem 1rem; border-radius: 8px;
          border: 1px solid var(--border); background: var(--bg);
          color: var(--text); font-family: var(--mono); font-size: 0.9rem;
          margin-bottom: 1rem;
        }
        .ob-input:focus { outline: none; border-color: var(--accent); }
        .ob-error {
          padding: 0.75rem; border-radius: 8px; background: #ff5c5c22;
          border: 1px solid var(--red); color: var(--red); font-size: 0.85rem;
          margin-bottom: 1rem;
        }
        .ob-nav { display: flex; gap: 0.75rem; justify-content: space-between; }
        .ob-btn {
          padding: 0.7rem 1.25rem; border-radius: 8px; font-weight: 600;
          cursor: pointer; border: none; font-size: 0.95rem;
        }
        .ob-btn.primary { background: var(--accent); color: #fff; }
        .ob-btn.primary:disabled { opacity: 0.4; cursor: not-allowed; }
        .ob-btn.ghost {
          background: transparent; color: var(--muted);
          border: 1px solid var(--border);
        }
        .ob-tip { color: var(--muted); margin-bottom: 1.5rem; font-size: 0.9rem; }
      `}</style>
    </div>
  );
}