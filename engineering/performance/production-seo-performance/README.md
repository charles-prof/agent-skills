# Production SEO & Web Performance ⚡🔍

A production-grade architectural skill and operational runbook for AI coding agents and human developers. Enforces staging-guarded Schema.org Knowledge Graphs, 100% self-hosted local `.woff2` font pipelines, Zero-FOUC critical CSS rendering, layout shift (CLS) prevention, and automated pre-release verification gates.

Designed for **Google Antigravity**, **AGY CLI**, **Claude Code**, **Cursor**, and **Gemini CLI**.

---

## ⚡ Quick Start

Install directly into your workspace with the open `skills` CLI:

```bash
npx skills add charles-prof/agent-skills --skill production-seo-performance
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
  npx skills add charles-prof/agent-skills --skill production-seo-performance -a claude-code
  npx skills add charles-prof/agent-skills --skill production-seo-performance -a cursor
  ```

---

## 🌟 Why This Skill?

Most web applications suffer from four subtle, compounding production regressions:
1. **Staging Indexation Leaks:** Staging or preview URLs get indexed by Google, creating duplicate content penalties and splitting domain authority.
2. **Third-Party Font Latency & FOUC:** External calls to Google Fonts or Typekit introduce render-blocking DNS/TLS overhead, causing Flash of Unstyled Content and degrading First Contentful Paint (FCP).
3. **Cumulative Layout Shift (CLS):** Images and embeds render without reserved dimensions, causing disruptive visual reflows that fail Google Core Web Vitals.
4. **Fragmented Structured Data:** Microdata or basic meta tags output isolated fragments instead of an interconnected Schema.org Knowledge Graph (`@graph`) linking the business, founder, services, and FAQs.

This skill codifies **battle-tested production solutions** into an automated, executable standard:
- 🛑 **4 Non-Negotiable Hard Gates:** Zero staging leaks, 100% self-hosted `.woff2` fonts, explicit media dimensions, and automated pre-release auditing.
- 🏛️ **Interconnected Entity Graph:** Unified Schema.org `@graph` connecting Organization, Founder, Facility, Service, and FAQ rich snippets.
- 🧪 **Automated CLI Auditor (`scripts/audit_production_readiness.py`):** Standalone verification script checking schema syntax, font leaks, staging guards, and image dimensions.
- 👥 **Multi-Persona Sign-Off Matrix:** Clear operational roles for Eleanor (Human Copy), Chloe (CRO/Meta), Sally (UX/Performance/Zero-FOUC), and Forge (Systems/Schema).

---

## 👥 Meet the Canonical Team

- **🌿 Eleanor (Brand & Human Experience Guardian):** Audits meta titles, descriptions, and FAQs to guarantee warm, human, active voice with zero robotic corporate jargon.
- **⚡ Chloe (CRO & Digital Marketing Lead):** Optimizes SERP CTR (click-through rate), OpenGraph social preview cards, and high-impact FAQ rich snippet coverage.
- **🛠️ Sally (UX & Performance Systems Architect):** Eliminates Flash of Unstyled Content (FOUC), preloads local `.woff2` typography, and enforces zero layout shifts (CLS < 0.1).
- **⚙️ Forge (Core Systems Engineer):** Implements the staging environment guard, Schema `@graph` data resolvers, compiler checks, and automated audit gates.
- **🏛️ CharNithi (Visual Direction & Executive Authority):** Studio founder and visual director anchoring the Schema.org founder entity node.

---

## 🛠️ Automated Verification Script

Run the included verification script in local development or CI/CD pipelines:

```bash
python3 scripts/audit_production_readiness.py --path .
```

---

## 📄 License
This skill is licensed under the [MIT License](../../../LICENSE).
