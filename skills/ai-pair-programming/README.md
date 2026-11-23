# AI Pair-Programming & Multi-Persona Orchestration 👥🚀

A production-grade engineering skill suite for AI coding agents and human developers. Transforms unpredictable single-agent pairing into a disciplined, high-fidelity engineering guild with dynamic persona orchestration, automated project topology detection, interactive alignment gates, and zero-regression safeguards.

Designed for **Google Antigravity**, **AGY CLI**, **Claude Code**, **Cursor**, and **Gemini CLI**.

---

## ⚡ Quick Start

Install directly into your workspace with the open `skills` CLI:

```bash
npx skills add charles-prof/agent-skills --skill ai-pair-programming
```

### Native Agent Installations

- **Antigravity CLI (AGY):**
  ```bash
  agy plugin install https://github.com/charles-prof/agent-skills.git
  ```
- **Gemini CLI:**
  ```bash
  gemini skills install https://github.com/charles-prof/agent-skills.git --path skills
  ```
- **Claude Code & Cursor:**
  ```bash
  npx skills add charles-prof/agent-skills --skill ai-pair-programming -a claude-code
  npx skills add charles-prof/agent-skills --skill ai-pair-programming -a cursor
  ```

---

## 🌟 Why This Skill?

Most AI coding sessions fail for three consistent reasons:
1. **The Single-Generalist Trap:** One agent attempts to be the architect, developer, designer, tester, and copywriter simultaneously, leading to shallow trade-offs and code rot.
2. **"Code First, Ask Later":** Agents guess ambiguous requirements instead of conducting crisp upfront alignment, forcing frustrating re-dos.
3. **Subtle Regressions:** Aesthetic changes update button accents while leaving background canvas flat; light mode renders unreadable white text; tests hang in watcher loops.

This skill codifies **real-world production lessons** into an executable runbook:
- 👥 **Dynamic Team Personas:** Deploy specialized personas (Winston for Architecture, Sally for UX, Eleanor for Human Empathy, Chloe for Brand, Amelia for Code, Murat for QA, John for Product).
- 🔍 **Automated Topology Detection:** Scans your codebase's dependencies, structure, tests, and documentation to automatically recommend the optimal team size and persona mix.
- 🛑 **5 Non-Negotiable Hard Gates:** Enforces alignment before code, atomic reversible commits, pre-flight verification, and the "Two Main Players" rule.
- 🌿 **Humane Communication:** Filters raw variables and technical jargon out of user-facing release notes.

---

## 👥 Meet the Canonical Personas

| Persona | Badge | Role | Domain |
| :--- | :---: | :--- | :--- |
| **Winston** | 📐 | **System Architect** | Persistence schemas, state slices, WASM/Worker RPC, system boundaries. |
| **Sally** | 🎨 | **UX & Design Specialist** | Design systems, glassmorphism, Tailwind CSS, responsive layouts. |
| **Eleanor** | 🌿 | **Human Experience & Empathy** | Cognitive load audits, light/dark contrast serenity, humane simplicity. |
| **Chloe** | 📜 | **Brand & Storyteller** | Mission narrative, onboarding copy, brand consistency, public voice. |
| **Amelia** | 💻 | **Lead Software Engineer** | Modern component code, bug fixes, refactoring, atomic conventional commits. |
| **Murat** | 🛡️ | **QA Test Architect** | Unit tests (Vitest/Jest), boundary regressions, automated quality gates. |
| **John** | 🚀 | **Product Manager** | User stories, acceptance criteria, milestone releases, and human-readable release notes. |

*Teams scale dynamically: Lean Pair (2 personas), Balanced Team (4 personas), or Full Guild (7 personas).*

---

## 🛑 The 5 Non-Negotiable Hard Gates

1. **Gate 1: Project Topology & Roster Approval Before Code** — Detect codebase structure before writing code.
2. **Gate 2: Interactive Alignment Gate (`/grill-me` + `/plan`)** — Ask clarifying questions and generate an approved spec before implementation.
3. **Gate 3: The "Two Main Players" & Inversion Safeguard** — Theme changes must coordinate **Background** and **Panels** together, and pass a Light/Dark Mode Inversion Audit.
4. **Gate 4: Atomic Reversible Conventional Commits** — Record each unit of work in discrete, revertible conventional commits (`feat:`, `fix:`, `style:`).
5. **Gate 5: Strict Pre-Flight Verification Gate** — Run tests, lint, and build with clean exits before marking tasks done or releasing.

---

## 📁 Included Assets & Templates

```text
skills/ai-pair-programming/
├── SKILL.md                          # Comprehensive agent runbook
├── README.md                         # Documentation & quickstart
├── scripts/
│   └── detect-team-topology.mjs      # Codebase scanner & team recommender
└── templates/
    ├── team-roster.template.json     # Configurable persona roster schema
    ├── learning-proposal.template.md # /learn structured proposal artifact
    ├── plan-spec.template.md         # /plan architectural feature specification
    └── interview-rubric.template.md  # /grill-me interactive interview questions
```

### Running the Topology Detector
```bash
# Scan current project and view recommended team
node scripts/detect-team-topology.mjs

# Export configuration to JSON
node scripts/detect-team-topology.mjs --export team-roster.json

# Scan a specific repository directory
node scripts/detect-team-topology.mjs /path/to/project
```

---

## 🛠️ Antigravity Slash Commands

- `/plan` — Generates a structured feature plan specification before touching code.
- `/grill-me` — Launches an interactive interview to align on design trade-offs.
- `/learn` — Creates a `learning_proposal.md` artifact to transfer hard-won team learnings.
- `/schedule` — Sets non-blocking timers or recurring background quality checks.

---

## 📄 License

Licensed under the [MIT License](../../LICENSE).
