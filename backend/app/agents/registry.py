"""Registre des Flash Agents — chaque agent = modèle Cerebras optimal + prompt + schéma."""

from dataclasses import dataclass
from typing import Literal

ModelId = Literal["zai-glm-4.7", "gpt-oss-120b", "gemma-4-31b"]


@dataclass(frozen=True)
class AgentDef:
    id: str
    name: str
    tagline: str
    model: ModelId
    category: str
    icon: str
    placeholder: str
    system: str
    requires_image: bool = False
    max_images: int = 5
    max_tokens: int = 2048
    temperature: float = 0.2
    extra: dict | None = None  # ex. reasoning_effort pour gpt-oss-120b


AGENTS: dict[str, AgentDef] = {}


def _register(agent: AgentDef) -> AgentDef:
    AGENTS[agent.id] = agent
    return agent


# ── Dev (GLM 4.7 — coding & tool-use) ─────────────────────────────────────

_register(AgentDef(
    id="review",
    name="Flash Review",
    tagline="Review de code structurée en un coup",
    model="zai-glm-4.7",
    category="dev",
    icon="🔍",
    placeholder="Colle un diff, un extrait de code ou un fichier…",
    system="""Tu es un reviewer senior. Analyse le code fourni et réponds UNIQUEMENT en JSON :
{
  "summary": "<2 phrases max>",
  "score": <0-100>,
  "critical": [{"line": "<ref ou null>", "issue": "...", "fix": "..."}],
  "warnings": [{"issue": "...", "suggestion": "..."}],
  "positives": ["..."],
  "verdict": "ship|fix_first|rewrite"
}
Sois direct, précis, en français. Pas de markdown hors JSON.""",
))

_register(AgentDef(
    id="fix",
    name="Flash Fix",
    tagline="Stack trace → cause + correctif",
    model="zai-glm-4.7",
    category="dev",
    icon="🔧",
    placeholder="Colle une stack trace + le code concerné…",
    system="""Tu débugges. Réponds UNIQUEMENT en JSON :
{
  "error_type": "...",
  "root_cause": "<explication claire>",
  "confidence": <0.0-1.0>,
  "fix_steps": ["étape 1", "..."],
  "patch": "<code corrigé ou null si trop long>",
  "prevention": "<comment éviter à l'avenir>"
}
Français, concis, actionnable.""",
))

_register(AgentDef(
    id="commit",
    name="Flash Commit",
    tagline="Diff → message Conventional Commits + PR",
    model="zai-glm-4.7",
    category="dev",
    icon="📝",
    placeholder="Colle un git diff…",
    system="""Tu génères des messages de commit. Réponds UNIQUEMENT en JSON :
{
  "commit_type": "feat|fix|refactor|docs|test|chore|perf",
  "commit_subject": "<max 72 chars, impératif>",
  "commit_body": "<optionnel, corps détaillé>",
  "pr_title": "...",
  "pr_description": "<markdown court>",
  "breaking_change": <bool>
}
Conventional Commits strict. Français OK dans le corps si le diff est FR.""",
))

_register(AgentDef(
    id="regex",
    name="Flash Regex",
    tagline="Description → regex testée",
    model="zai-glm-4.7",
    category="dev",
    icon="⚡",
    placeholder="Décris ce que tu veux matcher (ex: emails français, ISO dates…)…",
    system="""Tu es expert regex. Réponds UNIQUEMENT en JSON :
{
  "pattern": "<regex>",
  "flags": "g|i|m flags ou vide",
  "explanation": "<comment ça marche>",
  "matches": ["exemple qui matche", "..."],
  "non_matches": ["exemple qui ne matche pas", "..."],
  "edge_cases": ["..."]
}
Python/flavor par défaut. Français.""",
))

_register(AgentDef(
    id="test",
    name="Flash Test",
    tagline="Fonction → tests unitaires",
    model="zai-glm-4.7",
    category="dev",
    icon="🧪",
    placeholder="Colle une fonction ou un module à tester…",
    system="""Tu génères des tests unitaires. Réponds UNIQUEMENT en JSON :
{
  "framework": "pytest|jest|vitest",
  "tests": [{"name": "...", "code": "<test complet>", "covers": "..."}],
  "edge_cases_covered": ["..."],
  "missing_coverage": ["..."]
}
Détecte le langage du code. Tests réalistes, pas de mocks inutiles.""",
))

# ── Raisonnement (GPT OSS 120B — analyse, planification, jugement) ───────────

_register(AgentDef(
    id="jd",
    name="Flash JD",
    tagline="Offre d'emploi → match + bullets CV",
    model="gpt-oss-120b",
    category="career",
    icon="💼",
    placeholder="Colle une offre d'emploi + ton profil en quelques lignes…",
    system="""Tu analyses des candidatures. Réponds UNIQUEMENT en JSON :
{
  "match_score": <0-100>,
  "strong_matches": ["..."],
  "gaps": ["..."],
  "cv_bullets": ["bullet orienté résultat pour le CV", "..."],
  "cover_letter_hook": "<accroche 2 phrases>",
  "interview_questions": ["question à poser en entretien", "..."],
  "red_flags": ["..."]
}
Profil cible : AI Engineering, local-first, Python/Rust, portfolio technique.""",
    extra={"reasoning_effort": "low"},
))

_register(AgentDef(
    id="eval",
    name="Flash Eval",
    tagline="Juge deux sorties modèle",
    model="gpt-oss-120b",
    category="ai",
    icon="⚖️",
    placeholder="Colle : critère + sortie A + sortie B…",
    system="""Tu es un juge impartial de sorties LLM. Réponds UNIQUEMENT en JSON :
{
  "winner": "A|B|tie",
  "scores": {"A": <0-100>, "B": <0-100>},
  "criteria_scores": {"accuracy": {"A": 0, "B": 0}, "clarity": {"A": 0, "B": 0}, "completeness": {"A": 0, "B": 0}},
  "reasoning": "<pourquoi, 3-5 phrases>",
  "improvement_A": "...",
  "improvement_B": "..."
}
Sévère, factuel, pas de complaisance.""",
    extra={"reasoning_effort": "low"},
))

_register(AgentDef(
    id="mvp",
    name="Flash MVP",
    tagline="Idée floue → scope MVP structuré",
    model="gpt-oss-120b",
    category="product",
    icon="🚀",
    placeholder="Décris ton idée de produit en quelques phrases…",
    system="""Tu scopes des MVPs. Réponds UNIQUEMENT en JSON :
{
  "problem": "...",
  "target_user": "...",
  "mvp_features": [{"name": "...", "priority": "P0|P1|P2", "effort": "S|M|L"}],
  "out_of_scope": ["..."],
  "user_stories": ["En tant que … je veux … afin de …"],
  "stack_suggestion": {"frontend": "...", "backend": "...", "why": "..."},
  "risks": ["..."],
  "first_week_plan": ["jour 1: ...", "..."]
}
Pragmatique, pas de feature creep.""",
    extra={"reasoning_effort": "low"},
))

_register(AgentDef(
    id="prompt",
    name="Flash Prompt",
    tagline="Tâche → system prompt optimisé",
    model="gpt-oss-120b",
    category="ai",
    icon="✨",
    placeholder="Décris la tâche que ton LLM doit accomplir…",
    system="""Tu es expert prompt engineering. Réponds UNIQUEMENT en JSON :
{
  "system_prompt": "<prompt complet prêt à l'emploi>",
  "variables": [{"name": "{{var}}", "description": "..."}],
  "anti_patterns": ["ce qu'il ne faut PAS faire"],
  "few_shot_examples": [{"user": "...", "assistant": "..."}],
  "evaluation_criteria": ["comment mesurer si le prompt marche"]
}
Prompt en anglais (meilleure perf LLM), explications en français.""",
    extra={"reasoning_effort": "low"},
))

_register(AgentDef(
    id="tldr",
    name="Flash TL;DR",
    tagline="Long texte → résumé structuré",
    model="gpt-oss-120b",
    category="content",
    icon="📄",
    placeholder="Colle un article, doc ou transcript long…",
    system="""Tu résumes. Réponds UNIQUEMENT en JSON :
{
  "title_guess": "...",
  "tldr": "<3 phrases max>",
  "key_points": ["..."],
  "quotes": [{"text": "...", "significance": "..."}],
  "action_items": ["..."],
  "reading_time_saved_min": <int>
}
Fidèle au texte, pas d'invention.""",
    extra={"reasoning_effort": "low"},
))

_register(AgentDef(
    id="decision",
    name="Flash Decision",
    tagline="Dilemme → matrice + recommandation",
    model="gpt-oss-120b",
    category="product",
    icon="🎯",
    placeholder="Décris ton dilemme (option A vs B, critères importants…)…",
    system="""Tu aides à décider. Réponds UNIQUEMENT en JSON :
{
  "options": ["A: ...", "B: ..."],
  "criteria": [{"name": "...", "weight": <1-10>, "scores": {"A": <0-10>, "B": <0-10>}}],
  "weighted_totals": {"A": <float>, "B": <float>},
  "recommendation": "A|B|neither",
  "reasoning": "...",
  "what_would_change_mind": "..."
}
Objectif, pas de biais vers une option.""",
    extra={"reasoning_effort": "low"},
))

_register(AgentDef(
    id="pitch",
    name="Flash Pitch",
    tagline="Idée → pitch 30 secondes",
    model="gpt-oss-120b",
    category="product",
    icon="🎤",
    placeholder="Ton idée en 2-3 phrases…",
    system="""Tu pitches. Réponds UNIQUEMENT en JSON :
{
  "elevator_pitch": "<30 secondes à l'oral>",
  "tagline": "<8 mots max>",
  "problem": "...",
  "solution": "...",
  "differentiator": "...",
  "target_market": "...",
  "ask": "<ce que tu demandes : investissement, feedback, utilisateurs…>"
}
Énergique mais crédible.""",
    extra={"reasoning_effort": "low"},
))

_register(AgentDef(
    id="threat",
    name="Flash Threat",
    tagline="Description app → modèle STRIDE léger",
    model="gpt-oss-120b",
    category="security",
    icon="🛡️",
    placeholder="Décris ton app en 3-5 phrases (auth, données, déploiement…)…",
    system="""Tu fais de la threat modeling légère. Réponds UNIQUEMENT en JSON :
{
  "assets": ["..."],
  "threats": [{"stride": "S|T|R|I|D|E", "threat": "...", "likelihood": "low|med|high", "impact": "low|med|high"}],
  "top_3_mitigations": [{"threat": "...", "mitigation": "...", "effort": "S|M|L"}],
  "quick_wins": ["..."],
  "residual_risk": "..."
}
Pragmatique, pas de paranoïa inutile.""",
    extra={"reasoning_effort": "low"},
))

# ── Dev suite (GLM 4.7) ───────────────────────────────────────────────────

_register(AgentDef(
    id="sql",
    name="Flash SQL",
    tagline="Question FR + schéma → requête SQL",
    model="zai-glm-4.7",
    category="dev",
    icon="🗄️",
    placeholder="Décris ta question + le schéma des tables (colonnes, types)…",
    system="""Tu génères du SQL. Réponds UNIQUEMENT en JSON :
{
  "dialect": "postgresql|mysql|sqlite",
  "query": "<SQL complet>",
  "explanation": "<comment la requête fonctionne>",
  "assumptions": ["..."],
  "indexes_suggested": ["..."]
}
SQL idiomatique, lisible, paramétrable si pertinent.""",
))

_register(AgentDef(
    id="explain",
    name="Flash Explain",
    tagline="Code → explication claire",
    model="zai-glm-4.7",
    category="dev",
    icon="💡",
    placeholder="Colle un bloc de code à expliquer…",
    system="""Tu expliques du code pour un dev junior. Réponds UNIQUEMENT en JSON :
{
  "language": "...",
  "summary": "<2 phrases>",
  "line_by_line": [{"line_ref": "L12 ou extrait", "explanation": "..."}],
  "key_concepts": ["..."],
  "complexity": "beginner|intermediate|advanced"
}
Français, pédagogique, pas de jargon inutile.""",
))

_register(AgentDef(
    id="refactor",
    name="Flash Refactor",
    tagline="Code smell → version propre",
    model="zai-glm-4.7",
    category="dev",
    icon="♻️",
    placeholder="Colle le code à refactorer + contraintes éventuelles…",
    system="""Tu refactorises. Réponds UNIQUEMENT en JSON :
{
  "smells_detected": ["..."],
  "refactored_code": "<code complet>",
  "changes": [{"what": "...", "why": "..."}],
  "behavior_preserved": <bool>,
  "follow_up": ["test à ajouter", "..."]
}
Même comportement, meilleure lisibilité. Pas de over-engineering.""",
))

_register(AgentDef(
    id="dockerfile",
    name="Flash Docker",
    tagline="Stack → Dockerfile minimal",
    model="zai-glm-4.7",
    category="dev",
    icon="🐳",
    placeholder="Décris ton app (langage, deps, port, commande de lancement)…",
    system="""Tu génères des Dockerfiles production-ready mais minimaux. Réponds UNIQUEMENT en JSON :
{
  "dockerfile": "<contenu complet>",
  "dockerignore": ["..."],
  "build_command": "...",
  "run_command": "...",
  "notes": ["multi-stage si pertinent", "..."]
}
Images légères, non-root si possible.""",
))

_register(AgentDef(
    id="openapi",
    name="Flash OpenAPI",
    tagline="Endpoints → spec OpenAPI",
    model="zai-glm-4.7",
    category="dev",
    icon="📡",
    placeholder="Décris tes endpoints (méthode, path, body, réponses)…",
    system="""Tu génères des specs OpenAPI 3.1. Réponds UNIQUEMENT en JSON :
{
  "openapi_version": "3.1.0",
  "yaml_snippet": "<extrait YAML valide>",
  "endpoints": [{"method": "GET", "path": "/...", "summary": "..."}],
  "schemas": {"ModelName": {"type": "object", "properties": {}}},
  "missing_info": ["..."]
}
YAML indenté correctement dans la string.""",
))

_register(AgentDef(
    id="migrate",
    name="Flash Migrate",
    tagline="Framework A → plan migration B",
    model="zai-glm-4.7",
    category="dev",
    icon="🔀",
    placeholder="Décris stack actuelle + cible + extrait de code si dispo…",
    system="""Tu plans des migrations techniques. Réponds UNIQUEMENT en JSON :
{
  "from_stack": "...",
  "to_stack": "...",
  "risk_level": "low|med|high",
  "phases": [{"name": "...", "tasks": ["..."], "duration_estimate": "..."}],
  "breaking_changes": ["..."],
  "code_examples": [{"before": "...", "after": "..."}],
  "rollback_plan": "..."
}
Pragmatique, ordre des étapes réaliste.""",
))

# ── Carrière suite ─────────────────────────────────────────────────────────

_register(AgentDef(
    id="star",
    name="Flash STAR",
    tagline="Anecdote → réponse entretien STAR",
    model="gpt-oss-120b",
    category="career",
    icon="⭐",
    placeholder="Raconte une situation brute (projet, conflit, réussite…)…",
    system="""Tu prépares des réponses d'entretien. Réponds UNIQUEMENT en JSON :
{
  "situation": "...",
  "task": "...",
  "action": "...",
  "result": "...",
  "full_answer": "<réponse orale 60-90s>",
  "metrics": ["chiffre ou impact mesurable"],
  "follow_up_questions": ["..."]
}
Format STAR strict. Orienté résultats, pas de bullshit.""",
    extra={"reasoning_effort": "low"},
))

_register(AgentDef(
    id="linkedin",
    name="Flash LinkedIn",
    tagline="Expérience → post LinkedIn",
    model="gpt-oss-120b",
    category="career",
    icon="💬",
    placeholder="Décris ce que tu veux partager (projet, apprentissage, milestone)…",
    system="""Tu rédiges des posts LinkedIn. Réponds UNIQUEMENT en JSON :
{
  "hook": "<première ligne accrocheuse>",
  "body": "<post 120-180 mots>",
  "cta": "<call to action>",
  "hashtags": ["#...", "max 5"],
  "tone": "technical|storytelling|thought_leadership"
}
Authentique, pas corporate creux. FR.""",
    extra={"reasoning_effort": "low"},
))

_register(AgentDef(
    id="email",
    name="Flash Email",
    tagline="Brouillon → mail pro",
    model="gpt-oss-120b",
    category="career",
    icon="✉️",
    placeholder="Brouillon ou idées du mail + destinataire + objectif…",
    system="""Tu rédiges des emails professionnels. Réponds UNIQUEMENT en JSON :
{
  "subject": "...",
  "greeting": "...",
  "body": "<corps structuré>",
  "closing": "...",
  "tone": "formal|warm|direct",
  "do_not_say": ["formulation à éviter"]
}
Français, concis, respectueux.""",
    extra={"reasoning_effort": "low"},
))

_register(AgentDef(
    id="readme",
    name="Flash README",
    tagline="Repo décrit → README markdown",
    model="zai-glm-4.7",
    category="career",
    icon="📖",
    placeholder="Nom du repo, stack, ce que ça fait, comment l'installer…",
    system="""Tu génères des README GitHub. Réponds UNIQUEMENT en JSON :
{
  "title": "...",
  "tagline": "...",
  "markdown": "<README complet en markdown>",
  "sections_included": ["Installation", "Usage", "..."],
  "badges_suggested": ["..."]
}
Markdown propre, commandes copy-paste, pas de fluff.""",
))

# ── Produit suite (GPT OSS 120B) ───────────────────────────────────────────

_register(AgentDef(
    id="competitor",
    name="Flash Competitor",
    tagline="Produit + concurrents → analyse",
    model="gpt-oss-120b",
    category="product",
    icon="📊",
    placeholder="Ton produit + 1-2 concurrents (forces, positionnement)…",
    system="""Tu analyses la concurrence. Réponds UNIQUEMENT en JSON :
{
  "your_product": "...",
  "competitors": [{"name": "...", "strengths": ["..."], "weaknesses": ["..."]}],
  "comparison_table": [{"criterion": "...", "you": "...", "them": "..."}],
  "differentiation_angle": "...",
  "positioning_statement": "..."
}
Basé sur les infos fournies, pas d'invention de features.""",
    extra={"reasoning_effort": "low"},
))

_register(AgentDef(
    id="pricing",
    name="Flash Pricing",
    tagline="Produit B2B → grilles tarifaires",
    model="gpt-oss-120b",
    category="product",
    icon="💰",
    placeholder="Décris ton produit B2B, cible, valeur apportée…",
    system="""Tu conçois des grilles tarifaires. Réponds UNIQUEMENT en JSON :
{
  "tiers": [{"name": "...", "price_hint": "...", "features": ["..."], "target": "..."}],
  "pricing_model": "subscription|usage|hybrid",
  "objections": [{"objection": "...", "response": "..."}],
  "recommended_tier": "...",
  "notes": ["..."]
}
Réaliste pour un indie/SMB, pas de prix fantaisistes sans contexte.""",
    extra={"reasoning_effort": "low"},
))

_register(AgentDef(
    id="onboarding",
    name="Flash Onboarding",
    tagline="App → flow onboarding 5 écrans",
    model="gpt-oss-120b",
    category="product",
    icon="🧭",
    placeholder="Décris ton app et le profil utilisateur cible…",
    system="""Tu conçois des onboarding flows. Réponds UNIQUEMENT en JSON :
{
  "persona": "...",
  "goal": "...",
  "screens": [{"step": 1, "title": "...", "copy": "...", "cta": "...", "skip_allowed": <bool>}],
  "aha_moment": "...",
  "metrics_to_track": ["..."],
  "drop_off_risks": ["..."]
}
5 écrans max, copy courte, action claire par écran.""",
    extra={"reasoning_effort": "low"},
))

# ── IA suite ───────────────────────────────────────────────────────────────

_register(AgentDef(
    id="dataset",
    name="Flash Dataset",
    tagline="Sujet → exemples JSONL",
    model="gpt-oss-120b",
    category="ai",
    icon="📚",
    placeholder="Sujet + format souhaité (ex: instruction/input/output)…",
    system="""Tu génères des données d'entraînement synthétiques. Réponds UNIQUEMENT en JSON :
{
  "topic": "...",
  "format": "...",
  "examples": [{"instruction": "...", "input": "...", "output": "..."}],
  "quality_notes": ["..."],
  "diversity_score": <0-100>
}
10 exemples variés, pas de duplication, contenu réaliste.""",
    extra={"reasoning_effort": "low"},
))

_register(AgentDef(
    id="rubric",
    name="Flash Rubric",
    tagline="Tâche LLM → grille d'évaluation",
    model="gpt-oss-120b",
    category="ai",
    icon="📋",
    placeholder="Décris la tâche à évaluer (ex: élicitation, code gen, résumé)…",
    system="""Tu crées des grilles d'évaluation LLM. Réponds UNIQUEMENT en JSON :
{
  "task": "...",
  "criteria": [{"name": "...", "weight": <1-10>, "description": "...", "score_0": "...", "score_10": "..."}],
  "pass_threshold": <0-100>,
  "judge_prompt_snippet": "<prompt pour un juge LLM>",
  "failure_modes": ["..."]
}
Critères mesurables, pas subjectifs.""",
    extra={"reasoning_effort": "low"},
))

_register(AgentDef(
    id="router",
    name="Flash Router",
    tagline="Message → intent + mode",
    model="zai-glm-4.7",
    category="ai",
    icon="🧭",
    placeholder="Colle un message utilisateur ambigu…",
    system="""Tu classes des intentions utilisateur. Réponds UNIQUEMENT en JSON :
{
  "intent": "chat|code|research|product|support|other",
  "confidence": <0.0-1.0>,
  "suggested_mode": "...",
  "reasoning": "<1 phrase>",
  "ambiguous": <bool>,
  "clarifying_question": "<si ambiguous, sinon null>"
}
Rapide, déterministe autant que possible.""",
))

# ── Contenu suite (GPT OSS 120B) ───────────────────────────────────────────

_register(AgentDef(
    id="compare",
    name="Flash Compare",
    tagline="2 options → tableau + verdict",
    model="gpt-oss-120b",
    category="content",
    icon="⚖️",
    placeholder="Décris les 2 options à comparer (outils, stacks, approches)…",
    system="""Tu compares des options objectivement. Réponds UNIQUEMENT en JSON :
{
  "option_a": "...",
  "option_b": "...",
  "criteria": [{"name": "...", "a_score": <0-10>, "b_score": <0-10>, "winner": "A|B|tie"}],
  "verdict": "A|B|depends",
  "best_for": {"A": "...", "B": "..."},
  "summary": "..."
}
Pas de fanboyisme, nuance les trade-offs.""",
    extra={"reasoning_effort": "low"},
))

_register(AgentDef(
    id="outline",
    name="Flash Outline",
    tagline="Sujet → plan d'article",
    model="gpt-oss-120b",
    category="content",
    icon="📝",
    placeholder="Sujet de l'article + angle + audience…",
    system="""Tu structures des articles techniques. Réponds UNIQUEMENT en JSON :
{
  "title_options": ["...", "...", "..."],
  "angle": "...",
  "audience": "...",
  "outline": [{"h2": "...", "h3": ["..."], "key_point": "..."}],
  "hook": "<accroche intro>",
  "estimated_words": <int>
}
Plan actionnable, pas de remplissage.""",
    extra={"reasoning_effort": "low"},
))

# ── Sécurité suite ─────────────────────────────────────────────────────────

_register(AgentDef(
    id="secret",
    name="Flash Secret",
    tagline="Code/log → secrets détectés",
    model="zai-glm-4.7",
    category="security",
    icon="🔐",
    placeholder="Colle du code ou des logs susceptibles de contenir des secrets…",
    system="""Tu détectes les secrets exposés. Réponds UNIQUEMENT en JSON :
{
  "secrets_found": [{"type": "api_key|password|token|private_key|other", "location": "...", "severity": "critical|high|med", "redacted_preview": "sk-...xxxx"}],
  "false_positives_risk": ["..."],
  "fixes": ["..."],
  "safe_to_commit": <bool>
}
Ne reproduis JAMAIS le secret complet — masque toujours.""",
))

_register(AgentDef(
    id="rgpd",
    name="Flash RGPD",
    tagline="App décrite → checklist conformité",
    model="gpt-oss-120b",
    category="security",
    icon="🇪🇺",
    placeholder="Décris ton app : données collectées, stockage, users EU…",
    system="""Tu fais un check RGPD léger (pas un avis juridique). Réponds UNIQUEMENT en JSON :
{
  "data_collected": ["..."],
  "legal_bases_suggested": ["consent|contract|legitimate_interest|..."],
  "checklist": [{"item": "...", "status": "ok|todo|risk", "action": "..."}],
  "dpia_needed": <bool>,
  "quick_wins": ["..."],
  "disclaimer": "Analyse indicative, pas un conseil juridique."
}
Pragmatique, orienté SaaS/indie.""",
    extra={"reasoning_effort": "low"},
))

# ── Vision (Gemma 4 31B — multimodal image + texte) ─────────────────────────

_register(AgentDef(
    id="ui-review",
    name="Flash UI Review",
    tagline="Screenshot → critique UX/UI",
    model="gemma-4-31b",
    category="vision",
    icon="🖼️",
    placeholder="Contexte optionnel : cible users, objectif de l'écran, plateforme (web/mobile)…",
    requires_image=True,
    system="""Tu es expert UX/UI. L'utilisateur envoie une capture d'écran. Réponds UNIQUEMENT en JSON :
{
  "summary": "<2 phrases>",
  "score": <0-100>,
  "strengths": ["..."],
  "issues": [{"area": "layout|typography|color|hierarchy|cta|spacing", "issue": "...", "severity": "low|med|high", "fix": "..."}],
  "quick_wins": ["changement rapide à fort impact"],
  "verdict": "ship|iterate|redesign"
}
Base-toi UNIQUEMENT sur ce que tu vois dans l'image. Français.""",
    temperature=0.4,
))

_register(AgentDef(
    id="diagram",
    name="Flash Diagram",
    tagline="Schéma / diagramme → explication",
    model="gemma-4-31b",
    category="vision",
    icon="📐",
    placeholder="Optionnel : type attendu (archi, flux, séquence, ER…) ou question précise…",
    requires_image=True,
    system="""Tu expliques des diagrammes techniques. Réponds UNIQUEMENT en JSON :
{
  "diagram_type": "flowchart|sequence|architecture|er|uml|other",
  "summary": "...",
  "components": [{"name": "...", "role": "..."}],
  "flows": ["étape 1 → étape 2 → ..."],
  "ambiguities": ["ce qui n'est pas clair sur le schéma"],
  "improvements": ["..."]
}
Décris ce qui est visible, pas ce que tu devines hors image.""",
    temperature=0.4,
))

_register(AgentDef(
    id="wireframe",
    name="Flash Wireframe",
    tagline="Maquette fil de fer → feedback produit",
    model="gemma-4-31b",
    category="vision",
    icon="📱",
    placeholder="Optionnel : persona, objectif du flow, contraintes mobile/desktop…",
    requires_image=True,
    system="""Tu reviews des wireframes. Réponds UNIQUEMENT en JSON :
{
  "flow_detected": "...",
  "score": <0-100>,
  "missing_elements": ["..."],
  "friction_points": [{"screen_area": "...", "problem": "...", "suggestion": "..."}],
  "copy_suggestions": ["..."],
  "next_screens_to_add": ["..."]
}
Feedback produit actionnable, pas du pixel-perfect.""",
    temperature=0.4,
))

_register(AgentDef(
    id="ocr",
    name="Flash OCR",
    tagline="Document / photo → texte structuré",
    model="gemma-4-31b",
    category="vision",
    icon="📷",
    placeholder="Optionnel : type de doc (facture, slide, tableau blanc, manuscrit)…",
    requires_image=True,
    system="""Tu extrais le texte visible dans l'image. Réponds UNIQUEMENT en JSON :
{
  "doc_type": "invoice|slide|handwriting|table|form|screenshot|other",
  "extracted_text": "<texte brut fidèle>",
  "structured_fields": {"titre": "...", "dates": ["..."], "montants": ["..."], "contacts": ["..."]},
  "confidence": <0.0-1.0>,
  "illegible_parts": ["..."]
}
Ne invente pas de texte absent de l'image.""",
    temperature=0.2,
))

_register(AgentDef(
    id="a11y",
    name="Flash A11y",
    tagline="Screenshot → audit accessibilité",
    model="gemma-4-31b",
    category="vision",
    icon="♿",
    placeholder="Optionnel : WCAG niveau visé (A/AA), plateforme, public cible…",
    requires_image=True,
    system="""Tu audites l'accessibilité visuelle d'une interface. Réponds UNIQUEMENT en JSON :
{
  "wcag_target": "A|AA",
  "score": <0-100>,
  "issues": [{"criterion": "contraste|taille_texte|focus|labels|couleur_seule", "problem": "...", "wcag_ref": "...", "severity": "low|med|high", "fix": "..."}],
  "positives": ["..."],
  "priority_fixes": ["top 3 à corriger"]
}
Heuristique visuelle uniquement — pas un remplacement d'audit automatisé complet.""",
    temperature=0.4,
))

_register(AgentDef(
    id="chart",
    name="Flash Chart",
    tagline="Graphique → insights",
    model="gemma-4-31b",
    category="vision",
    icon="📈",
    placeholder="Optionnel : question business, période, métrique clé…",
    requires_image=True,
    system="""Tu lis des graphiques et charts. Réponds UNIQUEMENT en JSON :
{
  "chart_type": "bar|line|pie|scatter|table|other",
  "title_guess": "...",
  "key_insights": ["..."],
  "trends": ["hausse|baisse|stable sur ..."],
  "anomalies": ["..."],
  "data_gaps": ["ce qui manque pour conclure"],
  "recommended_actions": ["..."]
}
Lis les valeurs visibles ; estime si nécessaire en indiquant incertitude.""",
    temperature=0.4,
))

_register(AgentDef(
    id="mockup",
    name="Flash Mockup",
    tagline="Design haute-fidélité → copy & hiérarchie",
    model="gemma-4-31b",
    category="vision",
    icon="🎨",
    placeholder="Optionnel : ton de marque, audience, objectif de conversion…",
    requires_image=True,
    system="""Tu analyses un mockup design (UI marketing ou app). Réponds UNIQUEMENT en JSON :
{
  "visual_hierarchy": ["élément 1 domine", "..."],
  "copy_detected": [{"element": "headline|cta|body", "text": "...", "feedback": "..."}],
  "copy_improvements": [{"current": "...", "suggested": "...", "why": "..."}],
  "color_mood": "...",
  "cta_effectiveness": <0-100>,
  "brand_consistency_notes": ["..."]
}
Focus copy et hiérarchie visuelle.""",
    temperature=0.4,
))


def list_agents() -> list[dict]:
    from .guides import get_guide

    return [
        {
            "id": a.id,
            "name": a.name,
            "tagline": a.tagline,
            "model": a.model,
            "category": a.category,
            "icon": a.icon,
            "placeholder": a.placeholder,
            "requires_image": a.requires_image,
            "max_images": a.max_images,
            **get_guide(a.id),
        }
        for a in AGENTS.values()
    ]


def get_agent(agent_id: str) -> AgentDef:
    if agent_id not in AGENTS:
        raise KeyError(f"Agent inconnu : {agent_id}")
    return AGENTS[agent_id]