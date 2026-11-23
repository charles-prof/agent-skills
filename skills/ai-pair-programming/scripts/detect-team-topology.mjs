#!/usr/bin/env node

/**
 * Project Team Topology & Persona Detector
 *
 * Scans a target codebase (package.json, directory structure, test suites, docs)
 * and automatically recommends the optimal AI pair programming team topology and personas.
 *
 * Usage:
 *   node detect-team-topology.mjs [target_directory]
 *   node detect-team-topology.mjs --json
 *   node detect-team-topology.mjs --export team-roster.json
 */

import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
let targetDir = process.cwd();
let outputJson = false;
let exportPath = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--json') {
    outputJson = true;
  } else if (args[i] === '--export' && args[i + 1]) {
    exportPath = args[i + 1];
    i++;
  } else if (args[i] === '--help' || args[i] === '-h') {
    console.log(`
Project Team Topology & Persona Detector
Usage:
  node detect-team-topology.mjs [options] [target_directory]

Options:
  --json          Output results as JSON for agent automation
  --export <file> Write recommended team roster JSON to specified file
  --help, -h      Display this help dialog
`);
    process.exit(0);
  } else if (!args[i].startsWith('-')) {
    targetDir = path.resolve(args[i]);
  }
}

if (!fs.existsSync(targetDir)) {
  console.error(`Error: Directory not found: ${targetDir}`);
  process.exit(1);
}

// 1. Analyze Package.json
let pkg = null;
const pkgPath = path.join(targetDir, 'package.json');
if (fs.existsSync(pkgPath)) {
  try {
    pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
  } catch (err) {
    // Ignore JSON parse errors
  }
}

const allDeps = pkg
  ? { ...pkg.dependencies, ...pkg.devDependencies, ...pkg.peerDependencies }
  : {};

// 2. Scan Directory Structure
function hasSubdir(dirName) {
  return (
    fs.existsSync(path.join(targetDir, dirName)) ||
    fs.existsSync(path.join(targetDir, 'src', dirName))
  );
}

function findFiles(dir, filter, maxDepth = 3, currentDepth = 0) {
  if (!fs.existsSync(dir) || currentDepth > maxDepth) return [];
  let results = [];
  try {
    const list = fs.readdirSync(dir, { withFileTypes: true });
    for (const item of list) {
      if (item.name === 'node_modules' || item.name === '.git' || item.name === 'dist') continue;
      const fullPath = path.join(dir, item.name);
      if (item.isDirectory()) {
        results = results.concat(findFiles(fullPath, filter, maxDepth, currentDepth + 1));
      } else if (filter(item.name)) {
        results.push(fullPath);
      }
    }
  } catch (e) {
    // Permission or I/O error
  }
  return results;
}

const testFiles = findFiles(targetDir, name =>
  name.endsWith('.test.ts') ||
  name.endsWith('.test.tsx') ||
  name.endsWith('.test.js') ||
  name.endsWith('.spec.ts') ||
  name.endsWith('.spec.js')
);

const docFiles = findFiles(targetDir, name =>
  name.endsWith('.md') || name.endsWith('.mdx')
);

// 3. Evaluate Technology Pillars
const pillars = {
  frontend: Boolean(
    allDeps.react || allDeps.vue || allDeps.svelte || allDeps.next || allDeps.nuxt || allDeps.astro || allDeps.vite || hasSubdir('components')
  ),
  styling: Boolean(
    allDeps.tailwindcss || allDeps['@tailwindcss/postcss'] || allDeps['styled-components'] || allDeps.sass || fs.existsSync(path.join(targetDir, 'src', 'index.css'))
  ),
  database: Boolean(
    allDeps['@electric-sql/pglite'] || allDeps.pg || allDeps.prisma || allDeps['@prisma/client'] || allDeps.drizzle || allDeps.sqlite3 || allDeps['@supabase/supabase-js']
  ),
  testing: Boolean(
    allDeps.vitest || allDeps.jest || allDeps.playwright || allDeps['@playwright/test'] || allDeps.cypress || testFiles.length > 0
  ),
  typescript: Boolean(
    allDeps.typescript || fs.existsSync(path.join(targetDir, 'tsconfig.json'))
  ),
  documentation: Boolean(
    hasSubdir('docs') || docFiles.length >= 3
  )
};

// 4. Recommend Persona Roster
const personas = [];

// Amelia (Lead Developer) is always active
personas.push({
  id: 'lead_developer',
  name: 'Amelia',
  badge: '💻',
  role: 'Lead Software Engineer',
  rationale: 'Core implementation driver, executes approved plans with atomic reversible commits.',
  essential: true
});

// Winston (Architect)
if (pillars.database || pillars.typescript || hasSubdir('services') || hasSubdir('api')) {
  personas.push({
    id: 'architect',
    name: 'Winston',
    badge: '📐',
    role: 'System Architect',
    rationale: `Detected ${pillars.database ? 'database/persistence layer' : 'system contracts'}; governs schemas, boundaries, and Gate 1 & 2.`,
    essential: true
  });
}

// Sally (UX & Design)
if (pillars.frontend || pillars.styling) {
  personas.push({
    id: 'ux_designer',
    name: 'Sally',
    badge: '🎨',
    role: 'UX & Design Specialist',
    rationale: `Detected UI framework and styling (${pillars.styling ? 'Tailwind/CSS system' : 'Components'}); enforces design systems, responsiveness, and Gate 3 (Two Main Players).`,
    essential: true
  });
}

// Eleanor (Empathy & Human Experience)
if (pillars.frontend) {
  personas.push({
    id: 'empathy_strategist',
    name: 'Eleanor',
    badge: '🌿',
    role: 'Human Experience & Empathy Strategist',
    rationale: 'Active for user-facing applications; guards contrast readability, light/dark mode serenity, and humane simplicity.',
    essential: true
  });
}

// Murat (QA Test Architect)
if (pillars.testing || testFiles.length > 0) {
  personas.push({
    id: 'test_architect',
    name: 'Murat',
    badge: '🛡️',
    role: 'QA Test Architect',
    rationale: `Detected test framework (${testFiles.length} test files); enforces Gate 5 pre-flight verification and regression prevention.`,
    essential: true
  });
} else {
  // Suggest adding Murat anyway for quality discipline
  personas.push({
    id: 'test_architect',
    name: 'Murat',
    badge: '🛡️',
    role: 'QA Test Architect',
    rationale: 'Recommended to scaffold initial test suites and enforce pre-flight build integrity.',
    essential: false
  });
}

// John (Product Manager)
personas.push({
  id: 'product_manager',
  name: 'John',
  badge: '🚀',
  role: 'Product Manager',
  rationale: 'Maintains milestone trajectory, authors human-readable changelogs, and filters technical jargon from release notes.',
  essential: true
});

// Chloe (Brand Storyteller)
if (pillars.documentation || hasSubdir('public')) {
  personas.push({
    id: 'brand_storyteller',
    name: 'Chloe',
    badge: '📜',
    role: 'Brand & Storytelling Strategist',
    rationale: 'Coordinates mission narrative, public onboarding copy, and cultural tone.',
    essential: false
  });
}

// Topology determination
let topologyTier = 'lean_pair_2_personas';
if (personas.length >= 6) {
  topologyTier = 'full_suite_7_personas';
} else if (personas.length >= 4) {
  topologyTier = 'balanced_team_4_personas';
}

const result = {
  project_name: pkg?.name || path.basename(targetDir),
  project_path: targetDir,
  detected_pillars: pillars,
  recommended_topology: topologyTier,
  total_recommended_personas: personas.length,
  personas
};

if (exportPath) {
  const exportDir = path.dirname(path.resolve(exportPath));
  if (!fs.existsSync(exportDir)) {
    fs.mkdirSync(exportDir, { recursive: true });
  }
  fs.writeFileSync(path.resolve(exportPath), JSON.stringify(result, null, 2), 'utf8');
}

if (outputJson) {
  console.log(JSON.stringify(result, null, 2));
  process.exit(0);
}

// Human-friendly terminal presentation
console.log('\n======================================================');
console.log('  🛰️  AI PAIR PROGRAMMING: PROJECT TOPOLOGY DETECTOR  ');
console.log('======================================================\n');
console.log(`📁 Target Codebase: ${result.project_path}`);
console.log(`📦 Project Name:    ${result.project_name}`);
console.log(`🏷️  Recommended:    ${topologyTier.toUpperCase().replace(/_/g, ' ')}\n`);

console.log('🔍 Detected Technical Pillars:');
console.log(`  • Frontend Framework:  ${pillars.frontend ? '✅ Yes' : '❌ None detected'}`);
console.log(`  • Styling System:      ${pillars.styling ? '✅ Yes (Tailwind/CSS)' : '❌ None detected'}`);
console.log(`  • Database / State:    ${pillars.database ? '✅ Yes (PGlite/Postgres/State)' : '❌ None detected'}`);
console.log(`  • Test Suites:         ${pillars.testing ? `✅ Yes (${testFiles.length} test files)` : '⚠️ None detected'}`);
console.log(`  • TypeScript:          ${pillars.typescript ? '✅ Yes' : '❌ JavaScript'}`);
console.log(`  • Documentation:       ${pillars.documentation ? `✅ Yes (${docFiles.length} markdown files)` : '⚠️ Minimal'}\n`);

console.log('👥 Recommended AI Persona Team:');
for (const p of personas) {
  const status = p.essential ? '[Core]' : '[Recommended]';
  console.log(`  ${p.badge} ${p.name.padEnd(8)} | ${p.role.padEnd(30)} ${status}`);
  console.log(`     └─ ${p.rationale}`);
}

console.log('\n------------------------------------------------------');
if (exportPath) {
  console.log(`💾 Saved team roster configuration to: ${exportPath}`);
} else {
  console.log('💡 Tip: Export this configuration with:');
  console.log(`   node detect-team-topology.mjs --export team-roster.json`);
}
console.log('------------------------------------------------------\n');
