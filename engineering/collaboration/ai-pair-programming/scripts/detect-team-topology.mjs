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
let installBmadPrompt = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--json') {
    outputJson = true;
  } else if (args[i] === '--install-bmad' || args[i] === '--setup-bmad') {
    installBmadPrompt = true;
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
  --install-bmad  Display guided BMad Method installation options for testing & architecture
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

// Scan for BMad Framework & Skills
function detectBMad(dir) {
  const bmadLocations = [
    path.join(dir, '.agent', 'skills'),
    path.join(dir, '.skills'),
    path.join(dir, 'skills'),
    path.join(dir, '_bmad')
  ];
  const bmadSkills = new Set();
  for (const loc of bmadLocations) {
    if (fs.existsSync(loc)) {
      try {
        const items = fs.readdirSync(loc);
        for (const item of items) {
          if (item.startsWith('bmad-')) {
            bmadSkills.add(item);
          }
        }
      } catch (e) {
        // Ignore read errors
      }
    }
  }
  const skillsArray = Array.from(bmadSkills);
  const hasTea = bmadSkills.has('bmad-tea') || skillsArray.some(s => s.startsWith('bmad-testarch-'));
  const hasArchitect = bmadSkills.has('bmad-agent-architect') || bmadSkills.has('bmad-create-architecture');
  const hasPM = bmadSkills.has('bmad-agent-pm') || bmadSkills.has('bmad-create-prd');
  const hasDev = bmadSkills.has('bmad-agent-dev') || bmadSkills.has('bmad-dev-story');

  return {
    installed: bmadSkills.size > 0,
    skillCount: bmadSkills.size,
    skills: skillsArray,
    hasTea,
    hasArchitect,
    hasPM,
    hasDev
  };
}

const bmadInfo = detectBMad(targetDir);

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
  ),
  bmad: bmadInfo.installed,
  bmadSkillCount: bmadInfo.skillCount
};

// 4. Recommend Persona Roster
const personas = [];

// Amelia (Lead Developer) is always active
personas.push({
  id: 'lead_developer',
  name: 'Amelia',
  badge: '💻',
  role: 'Lead Software Engineer',
  rationale: bmadInfo.hasDev
    ? 'Core implementation driver, supercharged with BMad Dev (bmad-dev-story, bmad-code-review) and atomic commits.'
    : 'Core implementation driver, executes approved plans with atomic reversible commits.',
  essential: true,
  bmad_superpower: bmadInfo.hasDev ? 'bmad-dev-story, bmad-code-review' : null
});

// Winston (Architect)
if (pillars.database || pillars.typescript || hasSubdir('services') || hasSubdir('api')) {
  personas.push({
    id: 'architect',
    name: 'Winston',
    badge: '📐',
    role: 'System Architect',
    rationale: bmadInfo.hasArchitect
      ? `Detected ${pillars.database ? 'database/persistence layer' : 'system contracts'}; armed with BMad Architecture (bmad-create-architecture, readiness checks).`
      : `Detected ${pillars.database ? 'database/persistence layer' : 'system contracts'}; governs schemas, boundaries, and Gate 1 & 2.`,
    essential: true,
    bmad_superpower: bmadInfo.hasArchitect ? 'bmad-create-architecture' : 'bmad-create-architecture (available via BMad)'
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
    essential: true,
    bmad_superpower: bmadInfo.skills.includes('bmad-create-ux-design') ? 'bmad-create-ux-design' : null
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
    essential: true,
    bmad_superpower: 'Integrates with BMad CIS & Design Thinking (Maya / Dr. Quinn)'
  });
}

// Murat (QA Test Architect)
if (pillars.testing || testFiles.length > 0) {
  personas.push({
    id: 'test_architect',
    name: 'Murat',
    badge: '🛡️',
    role: 'QA Test Architect',
    rationale: bmadInfo.hasTea
      ? `Detected test framework (${testFiles.length} test files); fully armed with BMad TEA (Test Engineering Architecture, ATDD, trace matrix).`
      : `Detected test framework (${testFiles.length} test files); enforces Gate 5 pre-flight verification. [Recommend BMad TEA for ATDD & trace matrix]`,
    essential: true,
    bmad_superpower: bmadInfo.hasTea ? 'bmad-tea, bmad-testarch-atdd, bmad-testarch-trace' : 'bmad-tea (Unlockable)'
  });
} else {
  // Suggest adding Murat anyway for quality discipline
  personas.push({
    id: 'test_architect',
    name: 'Murat',
    badge: '🛡️',
    role: 'QA Test Architect',
    rationale: bmadInfo.hasTea
      ? 'Armed with BMad TEA to scaffold initial test suites and enforce pre-flight build integrity.'
      : 'Recommended to scaffold initial test suites and enforce pre-flight build integrity.',
    essential: false,
    bmad_superpower: bmadInfo.hasTea ? 'bmad-tea' : 'bmad-tea (Unlockable)'
  });
}

// John (Product Manager)
personas.push({
  id: 'product_manager',
  name: 'John',
  badge: '🚀',
  role: 'Product Manager',
  rationale: bmadInfo.hasPM
    ? 'Maintains milestone trajectory with BMad PRD tools (bmad-create-prd, bmad-create-epics-and-stories) and jargon-free release notes.'
    : 'Maintains milestone trajectory, authors human-readable changelogs, and filters technical jargon from release notes.',
  essential: true,
  bmad_superpower: bmadInfo.hasPM ? 'bmad-create-prd, bmad-create-epics-and-stories' : 'bmad-create-prd (available via BMad)'
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
  bmad_ecosystem: bmadInfo,
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
console.log(`  • Documentation:       ${pillars.documentation ? `✅ Yes (${docFiles.length} markdown files)` : '⚠️ Minimal'}`);
console.log(`  • BMad Ecosystem:      ${bmadInfo.installed ? `✅ Active (${bmadInfo.skillCount} BMad skills detected, TEA: ${bmadInfo.hasTea ? 'Enabled' : 'Partial'})` : '⚡ Not detected (Upgrade Opportunity)'}\n`);

console.log('👥 Recommended AI Persona Team:');
for (const p of personas) {
  const status = p.essential ? '[Core]' : '[Recommended]';
  console.log(`  ${p.badge} ${p.name.padEnd(8)} | ${p.role.padEnd(30)} ${status}`);
  console.log(`     └─ ${p.rationale}`);
  if (p.bmad_superpower) {
    console.log(`        ⚡ BMad Superpower: ${p.bmad_superpower}`);
  }
}

// BMad Recommendation / Installation Banner
if (!bmadInfo.installed || installBmadPrompt) {
  console.log('\n======================================================');
  console.log('  💡 BMAD SUPERPOWER OPPORTUNITY (TESTING & ARCHITECTURE)');
  console.log('======================================================');
  console.log('BMad Method is not detected in this project.');
  console.log('Installing BMad unlocks industry-grade tooling for your personas:');
  console.log('  • 🛡️  Murat (QA Test Architect): Unlocks 9 Test Engineering Architecture (TEA) skills:');
  console.log('      - bmad-testarch-atdd: Test-Driven Acceptance Testing (write failing tests before code)');
  console.log('      - bmad-testarch-test-design: System-level & epic-level test strategy');
  console.log('      - bmad-testarch-trace: Requirements-to-test traceability matrix');
  console.log('      - bmad-testarch-nfr: Performance & security non-functional assessment');
  console.log('      - bmad-code-review: Parallel adversarial review agents (Blind Hunter, Edge Case Hunter)');
  console.log('  • 📐 Winston (Architect): bmad-create-architecture & bmad-check-implementation-readiness');
  console.log('  • 🚀 John (Product Manager): bmad-create-prd, bmad-create-epics-and-stories, bmad-create-story');
  console.log('  • 💻 Amelia (Lead Dev): bmad-dev-story & bmad-quick-dev\n');
  console.log('👉 To install BMad in this project (after user approval):');
  console.log('   Run: npx bmad-method install');
  console.log('   Or:  agy plugin install https://github.com/bmad-code/bmad-method.git');
  console.log('======================================================');
}

console.log('\n------------------------------------------------------');
if (exportPath) {
  console.log(`💾 Saved team roster configuration to: ${exportPath}`);
} else {
  console.log('💡 Tip: Export this configuration with:');
  console.log(`   node detect-team-topology.mjs --export team-roster.json`);
}
console.log('------------------------------------------------------\n');
