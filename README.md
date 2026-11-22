# Agent Skills 🛠️

A curated collection of modular, production-tested **skills** and runbooks designed for AI coding agents (such as Google Antigravity, Gemini CLI, and Claude Code).

Skills extend agent capabilities with battle-tested procedures, complex toolchains, automated verification scripts, and domain-specific runbooks.

---

## 📚 Skill Catalog

| Category | Skill | Path | Description |
| :--- | :--- | :--- | :--- |
| **Workflow / Video** | `video-logo-removal` | [`workflow/video-editing/removals/`](./workflow/video-editing/removals/) | Spatial inpainting (`delogo`) & matting (`drawbox`) for frame-accurate graphic removal without cutting footage or desyncing audio. |
| **Research / Reviews** | `google-reviews-verification` | [`research/reviews/google-reviews-verification/`](./research/reviews/google-reviews-verification/) | Scrape, authenticate, and cross-verify real Google Reviews with a mandatory human-in-the-loop confirmation gate, Zero AI avatar policy, and schema generator. |
| **CMS / WordPress** | `wordpress-core-fse` | [`cms/wordpress/core-fse/`](./cms/wordpress/core-fse/) | Production runbook for decoupled WordPress Full Site Editing (FSE) block themes, strict 8pt grid, bespoke dynamic blocks (API v3 + render.php), SMACSS architecture, and declarative registries. |

---

## 🚀 How to Install & Use Skills

### Option A: Install Globally (Available across all projects)
Copy the skill folder to your global Antigravity/Gemini configuration directory:

```bash
mkdir -p ~/.gemini/config/skills/video-logo-removal
cp -r workflow/video-editing/removals/* ~/.gemini/config/skills/video-logo-removal/
```

### Option B: Install in a Specific Workspace (Team-Shared via Git)
Copy the skill into your project's `.agents/skills/` directory:

```bash
mkdir -p .agents/skills/video-logo-removal
cp -r workflow/video-editing/removals/* .agents/skills/video-logo-removal/
```

Once installed, your AI agent automatically detects the skill's description and loads the runbook whenever a relevant task is requested.

---

## 📁 Repository Structure

```text
agent-skills/
├── README.md
├── LICENSE
└── workflow/
    └── video-editing/
        └── removals/
            ├── SKILL.md                 # Agent instruction file with YAML frontmatter
            ├── README.md                # Human-readable documentation & overview
            └── scripts/
                └── verify_removal.py    # Automated test script for pixel-level leak verification
```

---

## 🤝 Contributing New Skills

1. Create a logical category folder under `workflow/`, `devops/`, `testing/`, etc.
2. Structure the skill with a standard `SKILL.md` file featuring clear YAML frontmatter (`name` and `description`).
3. Include verification checks or executable helper scripts under `scripts/`.
4. Submit a Pull Request!

---

## 📄 License
This repository is licensed under the [MIT License](./LICENSE).
