interface Props {
  title: string;
  steps: string[];
  variant?: "how" | "next";
}

export default function GuidePanel({ title, steps, variant = "how" }: Props) {
  if (!steps.length) return null;

  return (
    <div className={`guide-panel guide-${variant}`}>
      <h4 className="guide-title">{title}</h4>
      <ol className="guide-list">
        {steps.map((step, i) => (
          <li key={i}>{step}</li>
        ))}
      </ol>
      <style>{`
        .guide-panel {
          padding: 1rem 1.25rem;
          border-radius: 10px;
          margin-bottom: 1rem;
          border: 1px solid var(--border);
        }
        .guide-how {
          background: var(--surface);
        }
        .guide-next {
          background: linear-gradient(135deg, #ff6b2c14, #ff6b2c08);
          border-color: #ff6b2c44;
        }
        .guide-title {
          font-size: 0.8rem;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          margin-bottom: 0.6rem;
          font-weight: 600;
        }
        .guide-how .guide-title { color: var(--muted); }
        .guide-next .guide-title { color: var(--accent); }
        .guide-list {
          padding-left: 1.25rem;
          font-size: 0.9rem;
          line-height: 1.55;
        }
        .guide-list li { margin-bottom: 0.35rem; }
        .guide-list li:last-child { margin-bottom: 0; }
      `}</style>
    </div>
  );
}