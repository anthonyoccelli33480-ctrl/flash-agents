"""Guide utilisateur par agent — quoi faire avant / après le run."""

GUIDES: dict[str, dict[str, list[str]]] = {
    "review": {
        "how_to": [
            "Colle un `git diff`, un extrait de fichier ou un PR (idéalement < 500 lignes).",
            "Indique le langage ou le framework si ce n'est pas évident dans le code.",
        ],
        "next_steps": [
            "Corrige d'abord tout ce qui est marqué critical.",
            "Applique les fix suggérés dans ton IDE, puis relance Flash Review sur le diff corrigé.",
            "Si le verdict est rewrite → enchaîne avec Flash Refactor.",
            "Merge seulement quand le verdict est ship ou fix_first résolu.",
        ],
    },
    "fix": {
        "how_to": [
            "Colle la stack trace complète + le fichier/fonction concerné.",
            "Ajoute ce que tu as déjà essayé (optionnel mais utile).",
        ],
        "next_steps": [
            "Applique le patch ou suis fix_steps dans l'ordre.",
            "Relance ton test ou ta commande qui plantait.",
            "Si confidence < 0.7 → vérifie manuellement avant de déployer.",
            "Garde prevention en commentaire ou dans un test de non-régression.",
        ],
    },
    "commit": {
        "how_to": [
            "Colle un `git diff` (staged ou entre deux commits).",
            "Un diff trop gros ? résume les fichiers touchés en une ligne en tête.",
        ],
        "next_steps": [
            "Copie commit_subject + commit_body dans `git commit`.",
            "Ouvre ta PR avec pr_title et pr_description.",
            "Si breaking_change = true → documente dans le CHANGELOG.",
        ],
    },
    "regex": {
        "how_to": [
            "Décris en français ce que tu veux matcher (emails, dates, URLs…).",
            "Donne 1–2 exemples de chaînes qui doivent matcher / ne pas matcher.",
        ],
        "next_steps": [
            "Teste pattern dans ton code ou sur regex101.com.",
            "Vérifie les edge_cases listés avec tes vrais données.",
            "Intègre dans ton validateur avec les flags indiqués.",
        ],
    },
    "test": {
        "how_to": [
            "Colle la fonction ou la classe à tester (avec imports si besoin).",
            "Précise le framework préféré (pytest, jest…) si tu en as un.",
        ],
        "next_steps": [
            "Copie les tests dans un fichier `test_*.py` ou `*.test.ts`.",
            "Lance la suite : les tests doivent passer sur le code actuel.",
            "Complète missing_coverage si tu vises une couverture haute.",
        ],
    },
    "sql": {
        "how_to": [
            "Décris ta question en français.",
            "Colle le schéma des tables (noms colonnes, types, clés).",
        ],
        "next_steps": [
            "Exécute query sur une base de dev (jamais prod direct).",
            "Vérifie assumptions — ajoute les index_suggested si la requête est lente.",
            "Paramètre les valeurs utilisateur (pas de concat SQL).",
        ],
    },
    "explain": {
        "how_to": [
            "Colle le bloc de code opaque (algo, regex, hook React…).",
            "Indique ton niveau si tu veux plus ou moins de détail.",
        ],
        "next_steps": [
            "Relis line_by_line en parallèle du code dans ton IDE.",
            "Note key_concepts dans un commentaire ou une doc interne.",
            "Si tu modifies le code, relance Flash Explain sur la nouvelle version.",
        ],
    },
    "refactor": {
        "how_to": [
            "Colle le code qui sent mauvais (fonction longue, duplication…).",
            "Ajoute tes contraintes : « pas de nouvelle dépendance », « garder l'API publique ».",
        ],
        "next_steps": [
            "Remplace ton code par refactored_code.",
            "Lance tes tests existants — behavior_preserved doit tenir.",
            "Implémente les follow_up (tests manquants).",
            "Commit avec Flash Commit sur le diff.",
        ],
    },
    "dockerfile": {
        "how_to": [
            "Décris : langage, version, deps, port, commande de start, variables d'env.",
            "Mentionne si tu as besoin de multi-stage ou GPU.",
        ],
        "next_steps": [
            "Crée Dockerfile + .dockerignore à la racine du repo.",
            "Build : `docker build -t monapp .` puis teste run_command.",
            "Ajuste notes (volumes, secrets) avant push sur un registry.",
        ],
    },
    "openapi": {
        "how_to": [
            "Liste tes endpoints : méthode, path, body, codes de réponse.",
            "Colle un extrait de code routeur si tu en as un.",
        ],
        "next_steps": [
            "Copie yaml_snippet dans `openapi.yaml` ou fusionne avec ta spec existante.",
            "Valide sur editor.swagger.io.",
            "Génère un client SDK ou branche ta doc API (Scalar, Redoc).",
        ],
    },
    "migrate": {
        "how_to": [
            "Décris stack actuelle + cible (ex: CRA → Vite, REST → GraphQL).",
            "Colle un extrait représentatif du code à migrer.",
        ],
        "next_steps": [
            "Suis phases dans l'ordre — ne saute pas les breaking_changes.",
            "Crée une branche `migrate/...` et un ticket par phase.",
            "Teste rollback_plan avant de toucher la prod.",
        ],
    },
    "jd": {
        "how_to": [
            "Colle l'offre complète (titre, missions, stack, profil).",
            "Ajoute 3–5 lignes sur ton profil / ce que tu cherches.",
        ],
        "next_steps": [
            "Si match_score > 70 → adapte ton CV avec cv_bullets.",
            "Utilise cover_letter_hook en intro de lettre (Flash Email si besoin).",
            "Prépare interview_questions pour l'entretien.",
            "Investigue red_flags avant d'accepter.",
        ],
    },
    "star": {
        "how_to": [
            "Raconte une situation brute (projet, conflit, échec retourné…).",
            "Donne des chiffres si tu en as (%, délais, équipe).",
        ],
        "next_steps": [
            "Répète full_answer à voix haute 2–3 fois (60–90 s).",
            "Mémorise metrics — les recruteurs accrochent aux chiffres.",
            "Prépare follow_up_questions avec tes vraies réponses.",
        ],
    },
    "linkedin": {
        "how_to": [
            "Décris le milestone : projet shipped, apprentissage, recrutement…",
            "Indique le ton voulu (technique, storytelling).",
        ],
        "next_steps": [
            "Copie hook + body dans LinkedIn — vérifie le rendu mobile.",
            "Poste aux heures creuses (8h–9h ou 17h–18h).",
            "Réponds aux commentaires dans les 2 h pour le reach.",
        ],
    },
    "email": {
        "how_to": [
            "Brouillon ou bullet points + destinataire + objectif du mail.",
            "Précise le ton (formel, direct, chaleureux).",
        ],
        "next_steps": [
            "Relis do_not_say — reformule si tu as écrit pareil.",
            "Envoie ou planifie — garde subject court (< 50 car.).",
            "Pour une candidature : enchaîne après Flash JD.",
        ],
    },
    "readme": {
        "how_to": [
            "Nom du repo, stack, ce que ça fait, comment installer/lancer.",
            "Liens demo / screenshot si tu en as.",
        ],
        "next_steps": [
            "Colle markdown dans README.md à la racine.",
            "Ajoute badges_suggested en tête du fichier.",
            "Vérifie que les commandes d'install fonctionnent sur une machine fraîche.",
        ],
    },
    "eval": {
        "how_to": [
            "Colle le critère d'évaluation + sortie A + sortie B (même prompt).",
            "Sois explicite sur ce qui compte (précision, ton, longueur…).",
        ],
        "next_steps": [
            "Retiens le winner pour ton pipeline ou ton prompt.",
            "Applique improvement_* à la sortie perdante et re-teste.",
            "Exporte criteria_scores pour ton benchmark (Flash Rubric pour formaliser).",
        ],
    },
    "mvp": {
        "how_to": [
            "Décris le problème et pour qui (pas la solution).",
            "2–3 phrases suffisent — reste flou si c'est flou.",
        ],
        "next_steps": [
            "Implémente uniquement les features P0.",
            "Colle out_of_scope sur le mur du projet — ne les fais pas en v1.",
            "Suis first_week_plan jour par jour.",
            "Valide avec 1 utilisateur réel avant d'ajouter du P1.",
        ],
    },
    "prompt": {
        "how_to": [
            "Décris la tâche que ton LLM doit accomplir (entrée → sortie attendue).",
            "Mentionne contraintes : ton, langue, format, longueur.",
        ],
        "next_steps": [
            "Copie system_prompt dans ton app / .env / config agent.",
            "Remplace variables par tes vraies valeurs.",
            "Teste avec few_shot_examples puis mesure via evaluation_criteria.",
            "Itère en évitant anti_patterns.",
        ],
    },
    "tldr": {
        "how_to": [
            "Colle l'article, transcript ou doc long (PDF copié en texte).",
            "Pour un URL : copie le contenu toi-même (pas de fetch auto).",
        ],
        "next_steps": [
            "Partage tldr à ton équipe si c'est une veille.",
            "Traite action_items un par un.",
            "Archive key_points dans Notion/Obsidian avec la source.",
        ],
    },
    "decision": {
        "how_to": [
            "Nomme clairement option A et option B.",
            "Liste tes critères importants (coût, temps, risque…).",
        ],
        "next_steps": [
            "Suis recommendation si weighted_totals sont convaincants.",
            "Si tu hésites encore → vérifie what_would_change_mind avec de vraies données.",
            "Documente la décision (ADR ou note) pour ne pas re-débattre.",
        ],
    },
    "pitch": {
        "how_to": [
            "Ton idée en 2–3 phrases — problème + solution.",
            "À qui tu pitches (investisseur, client, recruteur).",
        ],
        "next_steps": [
            "Répète elevator_pitch en chronométrant (30 s max).",
            "Utilise tagline sur ta landing ou ton LinkedIn.",
            "Adapte ask selon ton interlocuteur du jour.",
        ],
    },
    "threat": {
        "how_to": [
            "Décris l'app : auth, données stockées, déploiement, intégrations tierces.",
            "3–5 phrases suffisent.",
        ],
        "next_steps": [
            "Implémente top_3_mitigations dans l'ordre effort S → M.",
            "Crée des tickets pour chaque threat likelihood/impact high.",
            "Revois après un changement d'archi majeur.",
        ],
    },
    "competitor": {
        "how_to": [
            "Décris ton produit en une phrase.",
            "Nomme 1–2 concurrents et ce que tu sais d'eux.",
        ],
        "next_steps": [
            "Utilise differentiation_angle sur ta landing page.",
            "Met à jour positioning_statement dans ton pitch deck.",
            "Vérifie comparison_table avec des faits réels (pas du marketing).",
        ],
    },
    "pricing": {
        "how_to": [
            "Produit B2B, cible (indie, PME, enterprise), valeur principale.",
            "Prix concurrents connus si tu en as.",
        ],
        "next_steps": [
            "Teste recommended_tier avec 2–3 prospects.",
            "Prépare les réponses objections pour tes calls de vente.",
            "Ajuste price_hint après le premier paiement réel.",
        ],
    },
    "onboarding": {
        "how_to": [
            "Décris l'app et le premier usage idéal (aha moment).",
            "Profil user : débutant, power user, mobile…",
        ],
        "next_steps": [
            "Implémente screens dans Figma ou direct en code.",
            "Mesure metrics_to_track dès le jour 1.",
            "Réduis drop_off_risks sur les étapes identifiées.",
        ],
    },
    "dataset": {
        "how_to": [
            "Sujet du dataset + format (instruction/input/output ou autre).",
            "Précise le cas d'usage (fine-tune, eval, router…).",
        ],
        "next_steps": [
            "Exporte examples en `.jsonl` (une ligne JSON par exemple).",
            "Relis quality_notes — supprime les exemples faibles.",
            "Complète à 50–100 exemples pour un vrai fine-tune.",
        ],
    },
    "rubric": {
        "how_to": [
            "Décris la tâche LLM à évaluer (élicitation, code gen, résumé…).",
            "Donne un exemple de bonne et mauvaise sortie si possible.",
        ],
        "next_steps": [
            "Utilise judge_prompt_snippet dans ton pipeline d'eval.",
            "Score tes sorties avec criteria + pass_threshold.",
            "Documente failure_modes dans ton README benchmark.",
        ],
    },
    "router": {
        "how_to": [
            "Colle un message utilisateur ambigu ou réel de ton app.",
            "Plusieurs intents mélangés = bon cas de test.",
        ],
        "next_steps": [
            "Si ambiguous → pose clarifying_question à l'utilisateur.",
            "Branche suggested_mode sur le bon agent Flash ou handler.",
            "Collecte les erreurs de routing pour affiner ton regex/ML.",
        ],
    },
    "compare": {
        "how_to": [
            "Nomme et décris les 2 options (outils, stacks, modèles…).",
            "Indique ton contexte (solo dev, prod, budget…).",
        ],
        "next_steps": [
            "Suis verdict si best_for correspond à ton contexte.",
            "Partage summary en doc d'archi ou thread LinkedIn.",
            "Re-teste dans 6 mois — les stacks évoluent vite.",
        ],
    },
    "outline": {
        "how_to": [
            "Sujet de l'article + angle + audience cible.",
            "Longueur visée si tu as une préférence.",
        ],
        "next_steps": [
            "Choisis un title_options et rédige section par section.",
            "Utilise hook comme intro — ne le jette pas.",
            "Vise estimated_words pour rester focus.",
        ],
    },
    "secret": {
        "how_to": [
            "Colle du code, un .env accidentel, ou des logs.",
            "Ne colle pas de vrais secrets de prod si tu les as déjà exposés ailleurs.",
        ],
        "next_steps": [
            "Si safe_to_commit = false → rotate immédiatement chaque secret trouvé.",
            "Applique fixes (gitignore, env vars, vault).",
            "Relance après correction pour confirmer safe_to_commit = true.",
        ],
    },
    "rgpd": {
        "how_to": [
            "Décris : données collectées, où elles sont stockées, users EU ou non.",
            "Mentionne cookies, analytics, sous-traitants.",
        ],
        "next_steps": [
            "Traite chaque checklist item status todo ou risk.",
            "Ajoute disclaimer + politique de confidentialité sur ton site.",
            "Si dpia_needed → consulte un juriste (ce n'est pas un avis légal).",
        ],
    },
    # ── Vision (Gemma 4 31B) ──────────────────────────────────────────────
    "ui-review": {
        "how_to": [
            "Upload une capture PNG/JPEG (écran entier ou composant isolé).",
            "Ajoute du contexte en texte : cible, objectif, web ou mobile.",
        ],
        "next_steps": [
            "Corrige les issues severity high en premier.",
            "Applique quick_wins dans Figma ou ton code sous 1 h.",
            "Si verdict redesign → refais une capture après itération et relance.",
        ],
    },
    "diagram": {
        "how_to": [
            "Upload un schéma lisible (archi, flux, séquence, ER, whiteboard photo).",
            "Pose une question précise en texte si tu veux zoomer sur un aspect.",
        ],
        "next_steps": [
            "Corrige ambiguities dans ton outil de diagramme (Mermaid, Excalidraw…).",
            "Partage summary + flows à l'équipe pour validation.",
            "Exporte en doc d'archi si diagram_type = architecture.",
        ],
    },
    "wireframe": {
        "how_to": [
            "Upload wireframe basse ou moyenne fidélité (Figma export, photo tableau blanc).",
            "Précise le persona et le parcours attendu.",
        ],
        "next_steps": [
            "Ajoute missing_elements et next_screens_to_add au flow.",
            "Intègre copy_suggestions avant de passer en hi-fi.",
            "Re-teste friction_points avec 1 utilisateur.",
        ],
    },
    "ocr": {
        "how_to": [
            "Upload photo ou scan lisible (facture, slide, formulaire, tableau).",
            "Indique doc_type si tu le connais pour de meilleurs champs structurés.",
        ],
        "next_steps": [
            "Vérifie extracted_text contre l'original — confidence < 0.8 = relecture humaine.",
            "Copie structured_fields dans ton CRM / tableur / Notion.",
            "Rephotographie illegible_parts si besoin.",
        ],
    },
    "a11y": {
        "how_to": [
            "Upload capture de l'écran à auditer (état focus/hover si pertinent).",
            "Indique le niveau WCAG visé (AA recommandé).",
        ],
        "next_steps": [
            "Implémente priority_fixes dans l'ordre.",
            "Valide avec axe DevTools ou Lighthouse en complément.",
            "Re-audite après correctifs — l'audit visuel ne couvre pas tout.",
        ],
    },
    "chart": {
        "how_to": [
            "Upload screenshot d'un graphique (dashboard, slide, rapport).",
            "Pose ta question business en texte (optionnel).",
        ],
        "next_steps": [
            "Croise key_insights avec les données brutes si tu les as.",
            "Agis sur recommended_actions prioritaires.",
            "Complète data_gaps avant une décision importante.",
        ],
    },
    "mockup": {
        "how_to": [
            "Upload mockup haute-fidélité (landing, app screen, ad creative).",
            "Précise audience et objectif (signup, achat, lecture…).",
        ],
        "next_steps": [
            "Applique copy_improvements sur le design.",
            "Vérifie cta_effectiveness — A/B test si score < 70.",
            "Aligne brand_consistency_notes avec ta charte graphique.",
        ],
    },
}


def get_guide(agent_id: str) -> dict[str, list[str]]:
    return GUIDES.get(agent_id, {"how_to": [], "next_steps": []})