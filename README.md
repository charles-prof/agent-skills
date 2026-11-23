# Agent Skills 🛠️

A curated collection of production-grade engineering workflows and skills designed for AI coding agents (such as Google Antigravity, Claude Code, Cursor, Codex, Copilot, and Gemini CLI).

Skills encode software engineering best practices, verification runbooks, automated toolchains, and strict guardrails into modular, executable instructions.

---

## ⚡ Quick Start

Fastest path — any agent, one command. The open **[skills CLI](https://github.com/vercel-labs/skills)** installs into 70+ agents (Claude Code, Cursor, Codex, Copilot, Cline, Antigravity, and more):

```bash
npx skills add charles-prof/agent-skills            # install all skills
npx skills add charles-prof/agent-skills --list     # browse before installing
```

Or grab individual skills:

```bash
npx skills add charles-prof/agent-skills --skill ai-pair-programming        # multi-persona pair programming & alignment gates
npx skills add charles-prof/agent-skills --skill google-reviews-verification # authentic reviews & verification gate
npx skills add charles-prof/agent-skills --skill wordpress-core-fse         # 8pt decoupled FSE & Block API v3
npx skills add charles-prof/agent-skills --skill video-logo-removal          # frame-accurate video inpainting
```

---

## 🔌 Prefer a Native Integration? Pick Your Tool Below

<details>
<summary><strong>▼ Antigravity CLI</strong></summary>

Install as a native plugin for skills and subagents across your workspaces:

**Install from the repo:**
```bash
agy plugin install https://github.com/charles-prof/agent-skills.git
```

**Install from a local clone:**
```bash
git clone https://github.com/charles-prof/agent-skills.git
agy plugin install ./agent-skills
```
</details>

<details>
<summary><strong>▼ Gemini CLI</strong></summary>

Install as native skills for auto-discovery, or add to `GEMINI.md` for persistent context:

**Install from the repo:**
```bash
gemini skills install https://github.com/charles-prof/agent-skills.git --path skills
```

**Install from a local clone:**
```bash
gemini skills install ./agent-skills/skills/
```
</details>

<details>
<summary><strong>▼ Claude Code & Cursor</strong></summary>

Install directly using `npx skills`:

```bash
# For Claude Code:
npx skills add charles-prof/agent-skills -a claude-code

# For Cursor:
npx skills add charles-prof/agent-skills -a cursor
```
</details>

---

## 📚 Skill Catalog

| Category | Skill Name (`npx`) | Maintained Path (Nested) | Flat Path (`skills/`) | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Engineering / AI** | `ai-pair-programming` | [`engineering/collaboration/ai-pair-programming/`](./engineering/collaboration/ai-pair-programming/) | [`skills/ai-pair-programming/`](./skills/ai-pair-programming/) | Architectural runbook and operational framework for high-fidelity AI pair-programming: dynamic 7-persona team orchestration, project topology detection, interactive alignment gates (`/plan`, `/grill-me`), regression defense, and pre-flight verification. |
| **Research / Reviews** | `google-reviews-verification` | [`research/reviews/google-reviews-verification/`](./research/reviews/google-reviews-verification/) | [`skills/google-reviews-verification/`](./skills/google-reviews-verification/) | Scrape, authenticate, and cross-verify real Google Reviews with a mandatory human-in-the-loop confirmation gate, Zero AI avatar policy, and schema generator. |
| **CMS / WordPress** | `wordpress-core-fse` | [`cms/wordpress/core-fse/`](./cms/wordpress/core-fse/) | [`skills/wordpress-core-fse/`](./skills/wordpress-core-fse/) | Architectural procedure for engineering decoupled WordPress Full Site Editing (FSE) block themes (8pt grid, Block API v3, SMACSS). |
| **Workflow / Video** | `video-logo-removal` | [`workflow/video-editing/removals/`](./workflow/video-editing/removals/) | [`skills/video-logo-removal/`](./skills/video-logo-removal/) | Spatial inpainting (`delogo`) & matting (`drawbox`) for frame-accurate graphic removal without cutting footage or desyncing audio. |

---

## 📁 Repository Architecture: Dual-Directory Model

This repository employs a **dual flat + nested architecture**:
1. **Nested for Maintenance**: Human developers navigate clean, logical domain hierarchies (`cms/`, `workflow/`, `research/`).
2. **Flat for Publishing**: The open `skills` CLI, Antigravity CLI, and Gemini CLI read from `skills/<skill-name>/`.
3. **Automated Sync Engine**: `scripts/sync_skills.py` keeps the flat and nested directories in 100% parity.

```text
agent-skills/
├── README.md
├── package.json
├── .github/workflows/verify-sync.yml
├── scripts/
│   └── sync_skills.py                     # Sync engine & CI verifier
├── skills/                                # Flat directory for npx skills CLI
│   ├── ai-pair-programming/
│   ├── google-reviews-verification/
│   ├── wordpress-core-fse/
│   └── video-logo-removal/
└── (Domain Categories — Source of Truth)
    ├── engineering/collaboration/ai-pair-programming/
    ├── cms/wordpress/core-fse/
    ├── research/reviews/google-reviews-verification/
    └── workflow/video-editing/removals/
```

### Synchronizing Skills Locally
Whenever you edit or add a skill in a category folder, synchronize the flat directory before committing:

```bash
npm run sync    # runs python3 scripts/sync_skills.py
npm run verify  # validates zero desync (enforced in CI)
```

---

## 📄 License
This repository is licensed under the [MIT License](./LICENSE).
