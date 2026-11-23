# Interactive Interview Rubric (`/grill-me`)

Use this rubric when initiating interactive alignment interviews with human partners or team leads.

## Core Rules for the Interviewer
1. **One Question at a Time:** Never overwhelm the partner with multi-part questions or wall-of-text options.
2. **Recommended Answer First:** Prefix the recommended choice with `(Recommended)` and provide a crisp rationale.
3. **No Redundant Yes/No:** Avoid trivial boolean queries; present meaningful architectural or UX trade-offs.
4. **Eliminate Assumptions Upfront:** If an implementation detail is ambiguous, grill the requirement before writing code.
5. **Honor the Partner's Time:** Keep options concise (1-2 sentences per choice), unnumbered (UI adds numbering), and free of artificial "Other" options (UI provides one).

---

## Question Archetypes

### 1. Scope & Identifier Alignment
- **Goal:** Establish the operational boundaries of a feature, skill, or refactor.
- **Example:**
  - *Question:* "What should be the official identifier and operational scope for [Feature/Skill]?"
  - *Recommended Option:* `(Recommended) [Option A] — Full production suite covering [X, Y, Z].`
  - *Alternative Option:* `[Option B] — Minimalist approach covering only [X].`

### 2. Architectural & Data Boundary Decisions
- **Goal:** Decide between state management patterns, persistence strategies, or data schemas.
- **Example:**
  - *Question:* "Where should the canonical state reside for [Entity]?"
  - *Recommended Option:* `(Recommended) Centralized local store with reactive subscriber events.`
  - *Alternative Option:* `Scoped component state passed via props.`

### 3. UX, Theming & Visual Hierarchy
- **Goal:** Determine surface styling, theme support, or layout behavior.
- **Example:**
  - *Question:* "How should the design adapt across light and dark aesthetics?"
  - *Recommended Option:* `(Recommended) Coordinate both Background & Panel tokens simultaneously to ensure WCAG AA contrast.`
  - *Alternative Option:* `Single dark-mode default with static high-contrast borders.`

### 4. Quality & Release Governance
- **Goal:** Define test coverage expectations, release versioning, and commit strategy.
- **Example:**
  - *Question:* "How should this release be versioned and announced?"
  - *Recommended Option:* `(Recommended) Minor version bump with human-readable release notes filtering out raw variable names.`
  - *Alternative Option:* `Patch release with technical commit log.`
