# WordPress Core & FSE Architectural Skill 🏛️

A production-grade **agent skill** and architectural standard for building decoupled, high-performance WordPress Full Site Editing (FSE) block themes and native bespoke blocks.

This skill eliminates Gutenberg layout fragility by establishing a decoupled tri-layer architecture:
1. **Declarative Data Registries**: Single-source-of-truth PHP data registries and sanitized admin meta boxes.
2. **Bespoke Dynamic Blocks**: Native Block API v3 blocks with server-side `render.php` templates and semantic BEM markup.
3. **Decoupled SMACSS Layout**: Modular CSS organized into Base, Layout, Modules, State, and Theme layers, strictly adhering to an **8pt quantized grid**.

---

## 📦 What's Inside

```text
cms/wordpress/core-fse/
├── SKILL.md                          # Master AI agent instructions & hard-gate rules
├── README.md                         # Human-readable documentation & usage guide
├── scripts/
│   └── validate_fse_theme.py         # Automated CLI validator for 8pt grid, theme.json, & block.json
└── templates/
    ├── theme.json                    # Canonical theme.json v3 boilerplate with 8pt spacing tokens
    ├── block.json                    # Canonical Block API v3 configuration
    ├── render.php                    # Canonical BEM server-side block render template
    └── registry-sample.php           # Canonical declarative PHP single-source-of-truth registry
```

---

## 🚀 Installation & Activation

### Option 1: Workspace Installation (Project-Specific)
Copy the skill into your project's `.agents/skills/` directory so any AI agent working on the repository automatically adopts the standard:

```bash
mkdir -p .agents/skills/wordpress-core-fse
cp -r cms/wordpress/core-fse/* .agents/skills/wordpress-core-fse/
```

### Option 2: Global Installation (Machine-Wide)
Copy the skill into your global Antigravity/Gemini configuration directory:

```bash
mkdir -p ~/.gemini/config/skills/wordpress-core-fse
cp -r cms/wordpress/core-fse/* ~/.gemini/config/skills/wordpress-core-fse/
```

---

## 🧪 Automated Verification Script

Test your theme against the architectural standards:

```bash
python3 scripts/validate_fse_theme.py --theme-path /path/to/wp-content/themes/your-theme
```

### Checks Performed:
- ✅ `theme.json` valid JSON and schema version (v2 or v3).
- ✅ Spacing presets strictly quantized to the **8pt grid** (`8px`, `16px`, `24px`, `32px`, `40px`, etc.).
- ✅ All custom blocks declare `"apiVersion": 3` and have existing `render.php` files.
- ✅ Zero forbidden inline layout styles (`display: flex`, `padding`, `margin`, `grid`) in block markup.
