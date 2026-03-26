# Agentic Patterns Library — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a progressive library of patterns, guidance, and working examples for agentic AI development, organized as a capability pyramid (L0-L4).

**Architecture:** Markdown documentation with TypeScript and Python example code. Each pyramid level is a standalone doc that references adjacent levels. Examples are minimal working code illustrating key patterns. The repo has no runtime — it's a reference library.

**Tech Stack:** Markdown, TypeScript (Node.js / Jest / docker-compose), Python (pytest / docker-compose), Git

---

## File Structure

```
agentic-patterns/
├── README.md                           # Task 1
├── CLAUDE.md                           # Task 2
├── docs/
│   ├── L0-foundation.md                # Task 3
│   ├── L1-feedback-loops.md            # Task 4
│   ├── L2-behavioral-guardrails.md     # Task 5
│   ├── L3-optimization.md              # Task 6
│   ├── L4-culture.md                   # Task 7
│   ├── cross-cutting/
│   │   ├── anti-patterns.md            # Task 8
│   │   ├── migration-guide.md          # Task 9
│   │   └── glossary.md                 # Task 10
│   └── references/
│       ├── wyntrade-case-study.md      # Task 11
│       └── further-reading.md          # Task 12
├── examples/
│   ├── stack-test/
│   │   ├── typescript/                 # Task 13
│   │   └── python/                     # Task 14
│   ├── skills/                         # Task 15
│   ├── guardrails/                     # Task 16
│   └── project-structure/              # Task 17
└── docs/
    └── specs/                          # Already exists
        └── 2026-03-26-agentic-patterns-design.md
    └── plans/                          # Already exists
        └── 2026-03-26-agentic-patterns.md
```

---

## Task 1: README.md — Project Overview

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write README.md**

Content must include:
- One-paragraph description: what this project is and who it's for
- The ASCII pyramid diagram (from spec) showing L0-L4
- Brief summary of each level (2-3 sentences each)
- "Getting Started" section: how to read this repo, recommended order
- "Audience" section: solo devs start at L0, team leads can jump to any level
- "Contributing" section: how to add patterns or examples
- Links to each level doc (`docs/L0-foundation.md` etc.)
- Keep under 100 lines — this is an entry point, not the content

- [ ] **Step 2: Commit**

```
git add README.md
git commit -m "docs: add project README with pyramid overview"
```

---

## Task 2: CLAUDE.md — Agent Constitution for This Repo

**Files:**
- Create: `CLAUDE.md`

- [ ] **Step 1: Write CLAUDE.md**

Content must include:
- Project description (1-2 lines)
- Repo structure overview (reference README for details)
- When writing docs: keep language precise, no filler, no vague requirements
- When writing examples: working code only, no TODOs, no placeholders
- Doc freshness: if you modify code in `examples/`, update the corresponding `docs/` file
- Markdown conventions for this repo
- Reference all level docs via `@` includes
- Hard limit: 150 lines maximum
- Master index: every doc in the repo must be reachable from CLAUDE.md

- [ ] **Step 2: Verify line count is under 150**

- [ ] **Step 3: Commit**

```
git add CLAUDE.md
git commit -m "docs: add CLAUDE.md as project constitution"
```

---

## Task 3: L0 — Foundation

**Files:**
- Create: `docs/L0-foundation.md`
- Create: `examples/project-structure/README.md`

**Dependencies:** Task 1 (README must exist for cross-references)

- [ ] **Step 1: Write docs/L0-foundation.md**

Cover each pattern from the spec section "Level 0: Foundation":

1. **0.1 Deep Modules** — Define deep vs shallow modules. Explain why AI benefits from deep modules (progressive disclosure, reduced context). Include a code sketch showing a deep module interface (3-5 exports, clean types) vs a shallow module (20+ exports, leaking internals). Reference Matt Pocock's graybox module concept.

2. **0.2 Progressive Disclosure** — Explain the discovery hierarchy: README → CLAUDE.md → module interfaces → implementation. Each layer answers "should I go deeper?" Show a directory tree that demonstrates good progressive disclosure vs bad (flat 50-file dir).

3. **0.3 Conceptual File Organization** — Group by domain, not by layer. Show before/after directory layouts. `trading/bridges/` vs `services/handlers/utils/`. Explain that AI uses paths as navigation hints.

4. **0.4 CLAUDE.md as Project Constitution** — What belongs in CLAUDE.md (rules, constraints, conventions, architecture). What doesn't (tutorials, changelogs, detailed API docs). The 150-line hard limit with `@` includes for everything else. CLAUDE.md as master index — all docs must be discoverable from it.

5. **0.5 Git Worktree-Based Development** — Why worktrees matter for agents: parallel isolation, clean slate, non-destructive exploration, deterministic starting state. Basic worktree commands. When to create a worktree vs branch-switch. Convention: `.worktrees/<branch-name>/` directory.

6. **0.6 AI-as-New-Starter Standard** — The litmus test. Cross-reference L4 (culture maintains what L0 establishes).

Each pattern section should follow this structure:
- **Problem**: What goes wrong without this pattern
- **Solution**: The pattern itself
- **In Practice**: Concrete guidance
- **Anti-Pattern**: What to avoid
- **Cross-References**: Links to related patterns in other levels

- [ ] **Step 2: Write examples/project-structure/README.md**

Create before/after directory examples showing shallow vs deep module organization. One TypeScript project layout, one Python project layout. Keep it minimal — 15-20 files per example max. Focus on the structural difference, not the code content.

- [ ] **Step 3: Verify cross-references are valid (no broken links)**

- [ ] **Step 4: Commit**

```
git add docs/L0-foundation.md examples/project-structure/
git commit -m "docs: add L0 foundation — project structure for AI accessibility"
```

---

## Task 4: L1 — Feedback Loops

**Files:**
- Create: `docs/L1-feedback-loops.md`
- Create: `examples/stack-test/typescript/` (multiple files)
- Create: `examples/stack-test/python/` (multiple files)

**Dependencies:** Task 3 (L0 foundational concepts referenced)

- [ ] **Step 1: Write docs/L1-feedback-loops.md**

Cover each pattern from the spec section "Level 1: Feedback Loops":

1. **1.1 Stack Tests** — Define stack test: full Docker stack, API-only verification, no mocks, user journey modeling. Contrast with unit tests (fast, isolated) and integration tests (partial, the worst of both). When to use which. Table comparing the three test types across: scope, speed, isolation, confidence, mock policy, failure diagnosticity.

2. **1.2 Full-Loop Assertion Layering** — Primary / Second-order / Third-order. Concrete example: a token swap test that asserts on API response (primary), database balance change (second-order), and audit log entry (third-order). Show the assertion code. Explain why each layer matters for agent self-diagnosis.

3. **1.3 Sequential / Additive Test Design** — The dependency ordering: startup → auth → basic flows → domain operations → advanced features. Explain why sequence is a diagnostic tool (if startup fails, don't debug trading). Reference the wyntrade test sequencer. Show example test ordering with file names.

4. **1.4 Container Isolation** — Four isolation mechanisms: unique container names, dynamic port allocation, transient volumes, per-test compose files. Docker resource limits (networks ~31 per bridge driver, containers, volumes) as a second motivation beyond collision prevention. Cleanup hygiene: containers and networks must be torn down after each test. Show the naming pattern and port allocation logic.

5. **1.5 No-Mock Philosophy** — Why mocking system components tests your mocks, not your system. When mocks ARE acceptable (external third-party APIs, blockchains without testnet). Show the wyntrade constitutional rules as example.

6. **1.6 Test Integrity Rules** — Five forbidden patterns with code examples showing wrong and right for each: conditional assertions, catch-without-rethrow, optional chaining on expect, early returns before assertions, try-catch wrapping test logic.

- [ ] **Step 2: Create TypeScript stack test example**

Create minimal working stack test example in `examples/stack-test/typescript/`:

Files:
- `package.json` — Jest, docker-compose dependencies
- `jest.config.js` — Stack test configuration (300s timeout, runInBand)
- `docker-compose.test.yml` — Minimal stack: app (Node.js), postgres, redis. Use `${PORT}` variable substitution for dynamic ports.
- `tests/config/stack-utils.ts` — Minimal StackTestUtils: initialize (start containers), cleanup (teardown), makeRequest (HTTP client), waitForReady (health check). Port allocation from available range.
- `tests/stack/app-startup.stack.test.ts` — First sequential test: verify app starts, health endpoint responds, dependencies are connected.
- `tests/stack/user-registration.stack.test.ts` — Second sequential test: register user via API, verify in database via API, check audit trail.
- `README.md` — How to run the examples, what each file does.

Key things to demonstrate:
- Dynamic port allocation (not hardcoded 3000, 5432, 6379)
- Unique container naming per test
- Transient volumes (tmpfs or named volumes that disappear)
- Per-test compose file generation
- Full-loop assertions (API response + database state via API)
- Sequential test ordering via file name prefix

- [ ] **Step 3: Create Python stack test example**

Create equivalent minimal working stack test example in `examples/stack-test/python/`:

Files:
- `pyproject.toml` — pytest, docker-compose dependencies
- `pytest.ini` — Stack test configuration (300s timeout)
- `docker-compose.test.yml` — Same minimal stack: app (Python/FastAPI), postgres, redis.
- `tests/conftest.py` — Stack fixture: start containers (session-scoped), yield, teardown. Port allocation. Container naming.
- `tests/stack/test_app_startup.py` — First test: health endpoint, dependency check.
- `tests/stack/test_user_registration.py` — Second test: register, verify, audit trail.
- `README.md` — How to run, what each file does.

Demonstrate the same isolation and assertion patterns as the TypeScript version, using Python idioms (pytest fixtures, session scope, etc.).

- [ ] **Step 4: Verify examples are consistent (same concepts, different languages)**

- [ ] **Step 5: Commit**

```
git add docs/L1-feedback-loops.md examples/stack-test/
git commit -m "docs: add L1 feedback loops — closed-loop testing with stack tests"
```

---

## Task 5: L2 — Behavioral Guardrails

**Files:**
- Create: `docs/L2-behavioral-guardrails.md`
- Create: `examples/skills/` (template files)

**Dependencies:** Task 4 (guardrails reference L1 test patterns)

- [ ] **Step 1: Write docs/L2-behavioral-guardrails.md**

Cover each pattern from the spec:

1. **2.1 Skill Overlay Architecture** — Define the overlay model: base capability → project additions → hook activations → integration points. Explain the structure of a skill file (frontmatter, base reference, project-specific rules, hook declarations). Show the anatomy of a skill.

2. **2.2 The Skill Chain** — brain+ → plan+ → tdd+ → verify+ → review+. How each skill's output becomes the next's input. The chain as a complete development lifecycle. What happens when you skip a link.

3. **2.3 Hook Automation** — PostToolUse hooks (track changes, enforce coverage). PreToolUse hooks (block destructive ops). Context-aware hooks (detect environment, adjust behavior). Hook script examples. The test-coverage-guard pattern: edit source → pending-tests.json → require test task → block completion.

4. **2.4 Constitutional Rules** — Hard constraints that never relax. Examples from wyntrade: no logger mocks, no blockchain mocks, full accounting. How rules flow from CLAUDE.md through skills to enforcement.

5. **2.5 Zero-Defect Tolerance** — Every error addressed. Why "unrelated failure" is never acceptable for agents. How this enables agents to self-diagnose systematically.

- [ ] **Step 2: Create skill template examples**

Create `examples/skills/` with:
- `SKILL-TEMPLATE.md` — Blank skill template with annotated sections (name, description, base reference, project rules, hooks, integration points)
- `example-tdd-skill.md` — Concrete example: a TDD skill for a hypothetical project, showing how constitutional rules and hook references work
- `README.md` — How to use skill templates, where to place them in a project

- [ ] **Step 3: Commit**

```
git add docs/L2-behavioral-guardrails.md examples/skills/
git commit -m "docs: add L2 behavioral guardrails — skills, hooks, constitutional rules"
```

---

## Task 6: L3 — Optimization

**Files:**
- Create: `docs/L3-optimization.md`
- Create: `examples/guardrails/` (TypeScript middleware example)

**Dependencies:** Task 5 (guardrails are an optimization pattern)

- [ ] **Step 1: Write docs/L3-optimization.md**

Cover each pattern from the spec:

1. **3.1 Smart Routing / Tool Selection** — The routing table concept: map shell commands to optimal tools. Table of common commands and their preferred tools. Token savings estimates (60-80% for search, 75% for file reads).

2. **3.2 Intent Classification** — The intent types: file_read, text_search, file_discovery, file_modify, docker. How to detect intent from command patterns. Compound command splitting on `&&`, `||`, `;`, `|`.

3. **3.3 Environment-Aware Routing** — Detect available tools at session start. Priority: specialized > general > raw command > block. Graceful degradation. Caching detection results.

4. **3.4 Context Engineering — The Scout Pattern** — Invest tokens upfront in structured exploration. Send a lightweight agent to map the codebase before acting. Reference the WISC framework.

5. **3.5 Structured Output over Raw Text** — Compare grep output (200 lines) vs jcodemunch output (5 structured results). Why structured output is more efficient for agent reasoning. When to prefer raw text (specific string searches).

- [ ] **Step 2: Create guardrail middleware example**

Create `examples/guardrails/` with:
- `package.json` — TypeScript project setup
- `src/core/intent.ts` — Intent parser: classify bash commands into intent types, handle compound commands
- `src/core/router.ts` — Router: intent + environment → resolution (allow/advise/block)
- `src/core/environment.ts` — Environment detector: check for RTK, jcodemunch, indexed repos
- `src/config/routing.config.ts` — Data-driven routing rules (the routing table)
- `README.md` — Architecture overview, how to adapt for other projects

This is a simplified version of the damage-control-guardrails showing the core pattern. Focus on the routing logic, not the full Claude Code hook integration.

- [ ] **Step 3: Commit**

```
git add docs/L3-optimization.md examples/guardrails/
git commit -m "docs: add L3 optimization — token efficiency and smart routing"
```

---

## Task 7: L4 — Culture

**Files:**
- Create: `docs/L4-culture.md`

**Dependencies:** Task 6 (culture maintains what L0-L3 establish)

- [ ] **Step 1: Write docs/L4-culture.md**

Cover each pattern from the spec:

1. **4.1 Documentation as Contract** — Stale docs are worse than no docs. Continuous refresh discipline. When code changes, docs update in the same task. Reference the CLAUDE.md master index pattern from L0.

2. **4.2 Evidence-Based Claims** — The verify+ pattern. Run commands, show output, then claim. Examples of bad claims ("tests should pass") vs good claims (command output shown). Evidence format template.

3. **4.3 Aggressive Cleanup** — Dead code, unused imports, stale comments, deprecated files. Why unused code is noise that degrades agent performance. Cleanup as a continuous practice, not a sprint activity.

4. **4.4 Spec Drift Detection** — How docs, tests, and code drift apart. Review checklists that include doc-to-code consistency. Automated checks where possible (broken link detection, stale file age detection).

5. **4.5 The New Starter Standard** — The ultimate test for L0. If someone with zero context can't navigate from CLAUDE.md → understanding, the project isn't agentic-ready. This is the standard that all other levels serve.

Include a review checklist template that teams can adopt.

- [ ] **Step 2: Commit**

```
git add docs/L4-culture.md
git commit -m "docs: add L4 culture — rigor, documentation, and maintenance"
```

---

## Task 8: Anti-Patterns

**Files:**
- Create: `docs/cross-cutting/anti-patterns.md`

**Dependencies:** Tasks 3-7 (all level docs must exist)

- [ ] **Step 1: Write anti-patterns doc**

Catalog of common mistakes organized by pyramid level:

**L0 anti-patterns:**
- God files (2000+ lines, 20+ exports)
- Flat directory structures with no conceptual grouping
- CLAUDE.md that's 500 lines of prose
- Orphaned docs not reachable from CLAUDE.md
- Working directly on main for feature work

**L1 anti-patterns:**
- Integration tests that test 3 of 5 components (the worst of both worlds)
- Mock-heavy test suites that test mocks not code
- Conditional test assertions that silently pass
- Hardcoded ports in Docker test configs
- Running stack tests individually instead of as suites

**L2 anti-patterns:**
- Rules written in CLAUDE.md but never enforced by skills/hooks
- Skipping links in the skill chain
- Hook scripts that only log but don't block

**L3 anti-patterns:**
- Using `grep` when jcodemunch is indexed
- Agent reading 300-line files when 10 lines would suffice
- No environment detection — same routing regardless of available tools

**L4 anti-patterns:**
- "I'll update the docs later"
- Accepting "known issues" as acceptable debt
- Keeping dead code "just in case"

Each anti-pattern: name, what it looks like, why it's harmful, what to do instead.

- [ ] **Step 2: Commit**

```
git add docs/cross-cutting/anti-patterns.md
git commit -m "docs: add anti-patterns catalog"
```

---

## Task 9: Migration Guide

**Files:**
- Create: `docs/cross-cutting/migration-guide.md`

**Dependencies:** Task 8 (references anti-patterns)

- [ ] **Step 1: Write migration guide**

Step-by-step guide for teams moving from traditional to agentic practices:

1. **Phase 0: Assessment** — Checklist: is your project agentic-ready? The new starter test. Identify biggest gaps.
2. **Phase 1: L0 Foundation** — Restructure file layout, write CLAUDE.md (under 150 lines), establish worktree conventions. Expected effort: small, high impact.
3. **Phase 2: L1 Feedback Loops** — Add stack test infrastructure alongside existing tests. Start with app-startup test. Build up sequentially. Don't remove existing tests yet.
4. **Phase 3: L2 Guardrails** — Add skill overlays for your most critical rules. Start with test-integrity and verify+. Add hooks for destructive operation blocking.
5. **Phase 4: L3 Optimization** — Set up jcodemunch or equivalent. Add routing guardrails. Measure token savings.
6. **Phase 5: L4 Culture** — Establish review checklists. Documentation freshness workflow. Cleanup discipline.

Each phase should be independently valuable — you don't need L4 to benefit from L0.

- [ ] **Step 2: Commit**

```
git add docs/cross-cutting/migration-guide.md
git commit -m "docs: add migration guide from traditional to agentic practices"
```

---

## Task 10: Glossary

**Files:**
- Create: `docs/cross-cutting/glossary.md`

**Dependencies:** Tasks 3-7 (all terms defined in level docs)

- [ ] **Step 1: Write glossary**

Alphabetical list of all specialized terms used across the pyramid:
- Stack test, full-loop assertion, assertion layering
- Skill overlay, skill chain, hook automation
- Constitutional rule, zero-defect tolerance
- Smart routing, intent classification, scout pattern
- Deep module, shallow module, graybox module
- Progressive disclosure, container isolation
- Evidence-based claim, spec drift
- Container naming, dynamic port allocation, transient volume
- Master index

Each entry: term, one-sentence definition, which level it belongs to, link to the doc section where it's defined.

- [ ] **Step 2: Commit**

```
git add docs/cross-cutting/glossary.md
git commit -m "docs: add glossary of agentic development terms"
```

---

## Task 11: Wyntrade Case Study

**Files:**
- Create: `docs/references/wyntrade-case-study.md`

**Dependencies:** Tasks 3-7 (case study maps to all levels)

- [ ] **Step 1: Write case study**

Reference document analyzing the wyntrade-core project against the pyramid:

- **Project overview** — Trading automation platform, production-grade
- **L0 in practice** — How wyntrade structures its codebase, its CLAUDE.md with 9 constitutional mandates, worktree usage
- **L1 in practice** — Stack test infrastructure: StackTestUtils (230KB utility class), container isolation (dynamic naming/ports/volumes), sequential test ordering (startup → auth → bridges → swaps → strategies), full-loop assertions, no-mock policy
- **L2 in practice** — 8 skill overlays (brain+, debug+, plan+, tdd+, verify+, review+, test-integrity, test-coverage-guard), hook automation (pending-tests.json, bash-block hooks), constitutional rules enforcement
- **L3 in practice** — Damage-control guardrails: smart routing (RTK/jcodemunch/Grep tool), intent classification, environment-aware routing, Docker safety tiers (always block / context block / context confirm)
- **L4 in practice** — Evidence-based verification, zero-defect tolerance, documentation health tracking

- [ ] **Step 2: Commit**

```
git add docs/references/wyntrade-case-study.md
git commit -m "docs: add wyntrade-core case study"
```

---

## Task 12: Further Reading

**Files:**
- Create: `docs/references/further-reading.md`

**Dependencies:** None (standalone reference)

- [ ] **Step 1: Write further reading**

Curated list of external resources, each with a 2-3 sentence summary of what it offers and how it relates to the pyramid:

**Books:**
- John Ousterhout, "A Philosophy of Software Design" — Deep modules concept (L0)

**Articles:**
- Matt Pocock, "Your codebase is NOT ready for AI" — Deep modules, progressive disclosure (L0)
- Kadam Sagar, "Beyond Copilots: Building a Closed-Loop Agentic Testing Ecosystem" — Skill-based architecture, MCP integration (L1, L2)
- Autonoma, "What is Agentic Testing?" — Intent-based testing, self-healing (L1)

**Videos:**
- DIY Smart Code, WISC Framework — Scout pattern, context engineering (L3)
- Matt Pocock, "Your codebase is NOT ready for AI" (video) — Deep modules, graybox (L0)

**Tools:**
- jcodemunch — Structured code search and symbol navigation (L3)
- RTK (Rust Token Killer) — Token optimization for shell commands (L3)

- [ ] **Step 2: Commit**

```
git add docs/references/further-reading.md
git commit -m "docs: add further reading references"
```

---

## Self-Review Checklist

- [x] **Spec coverage**: All 5 pyramid levels covered (Tasks 3-7). Cross-cutting docs covered (Tasks 8-10). Examples covered (Tasks 13-17 from spec, embedded in Tasks 3-6). References covered (Tasks 11-12).
- [x] **Placeholder scan**: No TBDs, TODOs, or vague instructions. Each step specifies concrete content.
- [x] **Type consistency**: File paths are consistent throughout. Pattern numbering (0.1-0.6, 1.1-1.6, etc.) matches the spec.
- [x] **Cross-references**: Tasks have appropriate dependencies. Later docs reference earlier pyramid levels.
- [x] **Examples parity**: TypeScript and Python stack test examples both specified with equivalent scope.
