# Google Reviews Verification & Scraping Skill 🌟

A production-grade skill and runbook for AI coding agents to scrape, authenticate, and format real Google Reviews from Google Maps and Search Knowledge Panels.

---

## 🎯 Purpose

Modern businesses, schools, and healthcare facilities thrive on social proof. However, AI agents frequently make two fatal mistakes when integrating reviews:
1. **Hallucinating reviews**: Fabricating quotes, altering reviewer wording, or making up star counts.
2. **Injecting AI / Stock Faces**: Pairing real reviewers' names with fake AI stock photos, destroying user trust.

This skill equips agents with a battle-tested protocol to:
- Ingest real Google Knowledge Panel data via a hybrid protocol (OCR screenshots, SERP queries, Maps links) without tripping anti-bot gates.
- Enforce **Zero AI Avatars**: preserve real uploaded Google profile photos or generate clean, branded first-letter fallback badges (`G`, `J`, `S`).
- Extract reviewer-attached event photos (e.g., graduation ceremonies, awards) into institutional milestone showcases.
- Force a **Mandatory Alignment Interview Gate** before any data touches code or database registries.
- Validate review data structures using the bundled CLI script.

---

## 📂 Repository Structure

```text
google-reviews-verification/
├── SKILL.md                 # Agent instruction runbook with YAML frontmatter
├── README.md                # Human developer documentation
└── scripts/
    └── validate_reviews.py  # Python validation & schema formatter CLI
```

---

## 🚀 Usage

### 1. Agent Invocation
When using Antigravity, Gemini CLI, or Claude Code, activate the skill:
```text
"Scrape real Google reviews from https://www.google.com/search?q=business+name and integrate them into our theme registry."
```
The agent activates `SKILL.md`, extracts candidate reviews, presents the alignment table, and asks for your confirmation.

### 2. Validating Reviews with the CLI Script
```bash
# Validate a JSON reviews file
python3 scripts/validate_reviews.py --input reviews.json

# Convert JSON reviews directly into a PHP theme registry array
python3 scripts/validate_reviews.py --input reviews.json --format php --output registry_snippet.php
```

---

## 📋 Schema Format

```json
{
  "entity_name": "Sample Academy",
  "rating_value": 4.8,
  "review_count": 120,
  "google_maps_url": "https://maps.google.com/?q=...",
  "reviews": [
    {
      "author": "Jane Doe",
      "rating": 5,
      "date": "2024",
      "role": "Parent of Kindergarten Student",
      "source": "Google Review",
      "avatar": "/assets/photos/avatars/avatar-jane.jpg",
      "quote": "The curriculum and caring teachers have completely transformed our child's confidence."
    }
  ]
}
```

---

## 📄 License
Licensed under the [MIT License](../../../LICENSE).
