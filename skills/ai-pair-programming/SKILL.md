---
name: ai-pair-programming
description: >-
  Architectural runbook and operational framework for high-fidelity AI-human pair programming.
  Enforces a dynamic multi-persona team topology (Winston, Sally, Eleanor, Chloe, Amelia,
  Murat, John), interactive alignment gates (/plan, /grill-me, /learn), the Two Main Players
  theming safeguard, light/dark inversion defense, atomic reversible conventional commits,
  and strict pre-flight verification.
---

# AI Pair-Programming & Multi-Persona Orchestration Runbook

Follow this runbook when pairing with human developers, orchestrating agent teams, or implementing features, refactors, and aesthetic shifts across complex codebases.

This framework transforms AI pairing from an unpredictable single-agent interaction into a disciplined, high-fidelity engineering guild. It establishes clear domain boundaries, enforces non-negotiable quality hard-gates, prevents contrast and regression failures, and honors the human developer's vision through structured alignment.

---

## 🛑 Non-Negotiable Hard-Gate Rules

When an AI agent pairs on any task, the following five production hard-gates must be strictly respected:

1. **Gate 1: Project Topology & Roster Approval Before Code**
   Never modify source files without first establishing the active team roster (size, roles, personas). The agent must run the project topology detector (`scripts/detect-team-topology.mjs`) or adopt an approved team configuration.
2. **Gate 2: Interactive Alignment Gate (`/grill-me` + `/plan`)**
   For non-trivial features, refactors, or architectural shifts, the agent must ask clarifying multiple-choice questions with recommended options and generate an approved plan spec before modifying code. Never assume requirements.
3. **Gate 3: The "Two Main Players" & Inversion Safeguard**
   When styling or theming UI, modifying accent colors alone is strictly forbidden. Both **Background** and **Panel** surfaces must be calibrated together to preserve aesthetic soul. Furthermore, all surfaces must pass a Light/Dark Mode Inversion Audit (never leave hardcoded dark-mode tokens like `text-white` on light-mode backgrounds).
4. **Gate 4: Atomic Reversible Conventional Commits**
   Every completed milestone, refactor, or bug fix must be captured as a discrete, reversible conventional commit (`feat:`, `fix:`, `style:`, `test:`, `chore:`). Commits must never mix unrelated concerns or leave uncommitted debris in the working tree.
5. **Gate 5: Strict Pre-Flight Verification Gate**
   No task is complete, and no release tag is published, until the project's verification suite (typecheck, linting, unit tests, and production build) passes with clean process exits.

---

## 👥 Dynamic Team Persona Topology

AI pair programming succeeds when specialized perspectives critique and collaborate rather than a single generalist guessing every angle. Personas can be scaled based on project size (Lean 2-Persona, Balanced 4-Persona, or Full Guild 7-Persona).

```mermaid
classDiagram
    class HumanPartner {
        <<Human-in-the-Loop>>
        +Vision & Intent
        +Approvals & Guidance
    }
    class Winston {
        <<System Architect>>
        +Database Schemas
        +WASM / RPC State Slices
        +System Boundaries
    }
    class Sally {
        <<UX & Design Specialist>>
        +Glassmorphism & Theming
        +Tailwind Spacing Scales
        +Responsive Layouts
    }
    class Eleanor {
        <<Human Experience & Empathy>>
        +Cognitive Load Audit
        +Humane Simplicity
        +Contrast & Serenity
    }
    class Chloe {
        <<Brand & Storytelling>>
        +Mission Narrative
        +Landing Copy & Culture
        +Public Voice
    }
    class Amelia {
        <<Lead Software Engineer>>
        +Component Engineering
        +Feature Implementation
        +Atomic Commits
    }
    class Murat {
        <<QA Test Architect>>
        +Unit Test Suites
        +Data Integrity Gates
        +Pre-Flight Verification
    }
    class John {
        <<Product Manager>>
        +PRD & Milestones
        +Jargon-Free Release Notes
        +Changelog Governance
    }

    HumanPartner --> Winston : Intent
    HumanPartner --> John : Priority
    Winston --> Amelia : Technical Contracts
    Sally --> Amelia : Visual Specs & Tokens
    Eleanor --> Sally : Empathy & Contrast Audit
    Chloe --> John : Brand Narrative
    Amelia --> Murat : Code for Verification
    Murat --> HumanPartner : Verified Green State
```

### The 7 Canonical Archetypes

| Persona | Badge | Role | Primary Responsibility | Governed Gates |
| :--- | :---: | :--- | :--- | :--- |
| **Winston** | 📐 | **System Architect** | Persistence schemas, state slices, modular boundaries, tech debt analysis. | Gate 1, Gate 2 |
| **Sally** | 🎨 | **UX & Design Specialist** | Visual hierarchies, glassmorphic styling, Tailwind v4 tokens, responsive layouts. | Gate 3 |
| **Eleanor** | 🌿 | **Human Experience & Empathy** | Cognitive load audits, light/dark contrast serenity, filtering technical jargon. | Gate 3, Gate 5 |
| **Chloe** | 📜 | **Brand & Storyteller** | Mission narrative, onboarding copy, brand consistency, public voice. | Gate 2 |
| **Amelia** | 💻 | **Lead Software Engineer** | High-fidelity component code, bug fixes, refactoring, atomic conventional commits. | Gate 4 |
| **Murat** | 🛡️ | **QA Test Architect** | Unit tests (Vitest/Jest), boundary regressions, automated quality gates. | Gate 5 |
| **John** | 🚀 | **Product Manager** | User stories, acceptance criteria, milestone releases, and human-readable release notes. | Gate 2, Gate 5 |

---

## 🏛️ Phased Execution Lifecycle

```mermaid
flowchart TD
    P1["Phase 1: Project Discovery & Topology Detection<br/>(Scan stack, test suites, recommend roster)"] --> P2["Phase 2: Interactive Alignment Gate<br/>(/grill-me questions + /plan specification)"]
    P2 --> P3["Phase 3: Multi-Persona Execution Loop<br/>(Winston Architect -> Amelia Dev -> Sally UX -> Eleanor Empathy)"]
    P3 --> P4["Phase 4: Regression Defense & Contrast Audit<br/>(Two Main Players rule, Inversion audit, Shell sanity)"]
    P4 --> P5["Phase 5: Pre-Flight Verification & Release<br/>(Murat tests/build -> John jargon-free release notes -> Atomic commit)"]
```

---

### Phase 1: Project Discovery & Topology Detection

Before touching application code, analyze the codebase environment to configure the team roster:

1. **Run the Project Topology Detector:**
   ```bash
   node scripts/detect-team-topology.mjs
   ```
2. **Evaluate Detected Pillars:**
   - **Frontend / UI present:** Sally (UX) and Eleanor (Empathy) are essential.
   - **Database / State layer present:** Winston (Architect) governs schema boundaries.
   - **Test runner detected:** Murat (QA) enforces test execution gates.
   - **Documentation / Public facing:** Chloe (Brand) reviews user onboarding copy.
3. **Confirm Roster with Human Partner:**
   If running for the first time, present the suggested team roster. Allow the human partner to scale up to the Full Guild (7 personas) or trim down to a Lean Pair (Amelia + Murat) for focused tasks.

---

### Phase 2: Interactive Alignment Gate (`/grill-me` + `/plan`)

Assumptions are the root cause of code churn. Execute structured elicitation before writing implementations:

1. **The `/grill-me` Protocol:**
   - Present **one question at a time** using an interactive choice UI.
   - Prefix the strongest architectural option with `(Recommended)` and provide crisp rationale.
   - Drill into ambiguity: state persistence, edge case handling, mobile viewports, or user tone.
2. **The `/plan` Specification:**
   - Produce a structured plan specification using `templates/plan-spec.template.md`.
   - Specify:
     - Executive summary & target personas.
     - User stories with verifiable acceptance criteria.
     - Component breakdown (which files are created vs modified).
     - Regression risks (theming, state nullability, shell constraints).
     - Step-by-step implementation sequence.
3. **Approval Gate:** The human partner must review and approve the plan before execution commences.

---

### Phase 3: Multi-Persona Execution Loop

Implementation proceeds along a clear handoff sequence:

1. **Architect Handshake (Winston):**
   - Establishes interfaces, TypeScript types, and database queries.
   - Guarantees data layers operate deterministically without race conditions.
2. **Engineering Execution (Amelia):**
   - Writes clean, modern, modular code honoring existing project conventions.
   - Breaks complex changes into incremental steps.
3. **UX & Design Review (Sally):**
   - Inspects glassmorphism tokens, border contrast, and padding consistency.
   - Validates multi-breakpoint responsiveness (ensures controls remain accessible on mobile viewports).
4. **Human Experience Audit (Eleanor):**
   - Ensures the interface breathes: removes visual noise, reduces cognitive friction.
   - Confirms copy speaks to humble humans with strong ambition rather than robotic machines.

---

### Phase 4: Hard-Learned Regression Defense Protocols

This phase embeds the hard-won lessons from high-fidelity production shipping:

#### 1. The "Two Main Players" Theming Rule
> *Never change accent colors without coordinating Background and Panel base surfaces.*

When introducing or switching themes (e.g., Dark Cosmos, Technical Flight Deck, Botanical Light Mode):
- **Player 1 (Background):** Base canvas color and ambient radial glow orbs (`--ambient-orb-1`, `--ambient-orb-2`).
- **Player 2 (Panels):** Translucent glass surfaces (`--glass-bg`, `--glass-border`, `--glass-glow`).
- **Failure Mode:** Only changing button accents leaves the application feeling murky, flat, or out-of-place. Both base canvas and panels must transform in unison.

#### 2. The Light/Dark Inversion Audit
> *Never leave hardcoded dark tokens in a multi-theme application.*

Common inversion failures:
- Hardcoded `text-white` or `text-slate-100` that becomes invisible on light backgrounds.
- Metric counters (e.g. `00`, progress percentages) rendering in near-invisible beige on white panels.
- Active navigation tabs fading into the panel surface due to static opacity settings.
- **Rule:** Use theme-aware CSS custom properties (`var(--color-text-main)`, `var(--color-surface-panel)`) or semantic Tailwind utility tokens.

#### 3. Platform & Shell Boundaries
> *Respect the host environment and avoid fragile chaining.*

- **No `&&` command chaining** when targeting Windows, PowerShell, or cross-platform environments.
- **Vitest & Test Runners:** Always pass flags to ensure tests terminate cleanly (e.g. `npx vitest run` or `--watch=false`) rather than hanging in interactive watcher mode.
- **Sandbox Working Directories:** Verify `cwd` explicitly when executing commands in multi-repository or sub-directory workspaces.

---

### Phase 5: Pre-Flight Verification & Release Cadence

No feature or version is released without passing through the final quality gates:

1. **Automated Verification (Murat):**
   ```bash
   npm run lint
   npm test
   npm run build
   ```
   All checks must complete with zero errors.
2. **Release Notes Jargon Filter (John & Eleanor):**
   - Release notes for end-users must explain **benefits and human value in simple, humble English**.
   - Strip internal CSS variable names, database column renames, and low-level code parameters from user-facing announcements.
   - Developers inspect git diffs; human users deserve clear, inspiring communication.
3. **Atomic Reversible Conventional Commit:**
   - Commit each change using standard Conventional Commits:
     ```bash
     git add [specific files]
     git commit -m "feat(module): descriptive human-readable summary"
     ```
   - Commit types: `feat`, `fix`, `style`, `refactor`, `test`, `chore`, `docs`.

---

## 🛠️ Antigravity Slash Command Runbook

| Command | Persona In Charge | Action & Deliverable |
| :--- | :--- | :--- |
| `/plan` | **Winston (Architect)** | Creates structured feature plan specification before touching code. |
| `/grill-me` | **John (PM) & Winston** | Initiates interactive interview to eliminate assumptions and align on design trade-offs. |
| `/learn` | **John (PM) & Amelia** | Creates a `learning_proposal.md` artifact documenting lessons learned, rationale, and proposed diffs. |
| `/schedule` | **Murat (QA)** | Configures recurring background health checks, test runs, or timers. |
| `/compact` | **Winston (Architect)** | Summarizes conversation context when sessions become extensive. |

---

## ⚠️ Critical Anti-Patterns & Failure Modes

| Anti-Pattern | Why It Fails | Required Correction |
| :--- | :--- | :--- |
| **"Code First, Ask Later"** | Agent starts coding based on assumptions, requiring total rewrites. | Enforce Gate 2: `/grill-me` interview and `/plan` spec first. |
| **Accent-Only Theming** | Changing primary color buttons while leaving panels murky gray. | Enforce Gate 3: Apply the "Two Main Players" rule (Background + Panels). |
| **Light-Mode Ghost Text** | Hardcoded white or light gray text rendered on white surfaces. | Conduct an Inversion Audit across all headings, metrics, and navigation tabs. |
| **The Mega-Commit** | Staging 40 modified files with message "fixed stuff". | Enforce Gate 4: Stage atomic commits per logical feature or fix. |
| **Release Without Verification** | Releasing code that breaks production build or test suite. | Enforce Gate 5: Run lint, test, and build before every release. |
| **Technical Jargon Overload** | Telling human users "Updated --glass-bg from #140726 to #E0DDD8". | Enforce Eleanor's Log: Explain the serene visual atmosphere in plain language. |

---

## 📋 Pre-Flight Release Checklist

- [ ] Project topology analyzed and active personas established
- [ ] Requirements aligned via `/grill-me` and `/plan` spec
- [ ] UI tested across both Dark and Light modes (zero ghost text, WCAG contrast verified)
- [ ] Responsive viewports checked for collision and layout overflow
- [ ] Linting executed with 0 errors
- [ ] Unit test suite executed and passed with clean exit
- [ ] Production build passes without errors
- [ ] Release notes authored in clear, humane language (no raw variables)
- [ ] Atomic, reversible conventional commit recorded
