# L0: Foundation — Project Structure for AI Accessibility

Your codebase is the biggest influence on AI's output. Structure it so an AI with zero prior context can navigate, understand, and contribute effectively.

## Pattern 0.1 — Deep Modules

**Problem**: Shallow modules expose too much surface area. When a module exports 20+ functions, types leak across boundaries, and the AI must track many interconnections simultaneously. Each export creates a potential coupling point. The agent wastes context understanding implementation details that should be hidden.

**Solution**: A deep module has a simple interface with lots of implementation hidden behind it. The AI sees the seam — a clean, small set of exports — and delegates implementation details to the interior. Based on John Ousterhout's "A Philosophy of Software Design" and Matt Pocock's graybox module concept: modules where tests lock down behavior, the public interface is carefully controlled, and the interior is delegatable to AI.

**In Practice**:
- Export 3-5 functions maximum per module
- Put complex logic behind a simple facade
- Let tests specify behavior, not implementation
- Keep types focused — avoid "kitchen sink" interfaces

```typescript
// Deep module — clean interface, complexity hidden
// ecommerce/fulfillment/index.ts
export interface FulfillmentConfig {
  sourceWarehouse: WarehouseId;
  targetRegion: RegionId;
  confirmations: number;
}

export async function fulfillOrder(config: FulfillmentConfig, items: OrderItem[]): Promise<FulfillmentResult>
export async function getFulfillmentStatus(orderId: string): Promise<FulfillmentStatus>
export function getSupportedRegions(): readonly RegionId[]
```

```typescript
// Shallow module — leaking internals, 20+ exports
// ecommerce/fulfillment/index.ts
export function fulfillOrder(...) { }
export function getFulfillmentStatus(...) { }
export function getSupportedRegions() { }
export function validateConfig(...) { }           // internal
export function parseWarehouseId(...) { }              // internal
export function serializeOrder(...) { }               // internal
export function deserializeOrder(...) { }              // internal
export function calculateShipping(...) { }               // internal
export function estimateTax(...) { }                // internal
export function formatAddress(...) { }              // internal
export function parseAddress(...) { }               // internal
// ... 10 more internal utilities
```

**Anti-Pattern**: Creating "utils" files that export 20+ helper functions. If you can't describe what a module does in one sentence, it's too shallow.

**Cross-References**: See [L2: Skills Framework](L2-behavioral-guardrails.md) for how skills enforce deep module boundaries during implementation. [Pattern 0.8 — Aggressive Cleanup](#pattern-08--aggressive-cleanup) covers maintaining depth through continuous cleanup.

---

## Pattern 0.2 — Progressive Disclosure

**Problem**: A flat directory with 50 files forces the AI to read everything to understand relationships. Deep nesting hides important files behind many clicks. Both extremes waste context — the agent can't discover structure incrementally.

**Solution**: Directory structure mirrors mental models. AI discovers complexity gradually: README → CLAUDE.md → module interfaces → implementation. Each layer gives enough context to decide whether to go deeper.

**In Practice**:
- Put entry points at the root: `README.md`, `CLAUDE.md`
- Group related files into directories by domain
- Keep depth to 3-4 levels maximum
- Each directory should have a clear purpose

```
Good — progressive disclosure
project/
├── README.md                    # Overview, entry point
├── CLAUDE.md                    # Agent contract
├── ecommerce/                   # Domain module
│   ├── index.ts                 # Public interface
│   ├── fulfillment/             # Sub-domain
│   │   ├── index.ts
│   │   └── shipping.ts
│   └── catalog/                 # Sub-domain
│       └── index.ts
└── testing/                     # Cross-cutting concern
    └── stack-test.ts
```

```
Bad — flat 50-file directory
project/
├── README.md
├── fulfillment_shipstation.ts
├── fulfillment_fedex.ts
├── catalog_shopify.ts
├── catalog_woocommerce.ts
├── catalog_bigcommerce.ts
├── ecommerce_inventory.ts
├── ecommerce_tax.ts
├── ecommerce_pricing.ts
├── ecommerce_checkout.ts
├── ecommerce_monitoring.ts
├── ecommerce_recovery.ts
... (40 more files)
```

**Anti-Pattern**: "Treasure hunt" structures where understanding one file requires reading 10 others scattered across the tree.

**Cross-References**: [Pattern 0.3](#pattern-03--conceptual-file-organization) expands on grouping by domain. [L4: New Starter Standard](L4-standards-measurement.md) tests whether disclosure works for zero-context agents.

---

## Pattern 0.3 — Conceptual File Organization

**Problem**: Grouping by technical layer (`services/`, `handlers/`, `utils/`, `types/`) separates related concepts. The AI can't find all ecommerce code in one place — it's scattered across directories. File paths become meaningless navigation hints.

**Solution**: Group by domain or capability. AI uses file paths as navigation hints. Co-locate related code by what it does, not what language construct it uses.

**In Practice**:
- `ecommerce/fulfillment/` not `services/fulfillment/`
- `ecommerce/types.ts` inside the domain, not a global `types/` dir
- One domain per directory, cross-cutting concerns at root level

```
Before — technical layering
src/
├── services/
│   ├── checkout.ts
│   ├── fulfillment.ts
│   └── monitoring.ts
├── handlers/
│   ├── orderHandler.ts
│   └── fulfillmentHandler.ts
├── utils/
│   ├── tax.ts
│   └── shipping.ts
└── types/
    ├── checkout.ts
    └── fulfillment.ts
```

```
After — conceptual organization
src/
├── ecommerce/
│   ├── index.ts                 # Public interface
│   ├── checkout.ts              # Implementation
│   ├── monitor.ts               # Monitoring logic
│   ├── types.ts                 # Domain types
│   └── utils/                   # Ecommerce-specific utilities
│       ├── tax.ts
│       └── shipping.ts
├── fulfillment/
│   ├── index.ts
│   ├── shipstation.ts
│   └── types.ts
└── monitoring/                  # Cross-cutting
    └── index.ts
```

**Anti-Pattern**: Creating `shared/` or `common/` directories that become dumping grounds for unrelated code. If code is shared between two domains, question whether those domains are properly separated.

**Cross-References**: [Pattern 0.1](#pattern-01--deep-modules) shows how deep modules reinforce conceptual organization. [L1: Stack Tests](L1-feedback-loops.md) demonstrates testing at domain boundaries.

---

## Pattern 0.4 — CLAUDE.md as Project Constitution

**Problem**: An agent entering a project needs to know: what is this, how is it structured, what must I never do, what patterns must I follow. Scattering this across READMEs, CONTRIBUTING files, and wiki pages forces the agent to hunt for rules it may violate before finding them.

**Solution**: CLAUDE.md is the single source of truth — a contract, not a tutorial. It answers the essential questions in one place. Hard limit: **150 lines maximum**. Beyond that, link to external docs.

**In Practice**:
```markdown
# Project — Agent Contract

## Project Description
One-sentence summary of what this project does.

## Repository Structure
Tree diagram showing major directories and their purposes.

## Constitutional Rules (Never Violate)
1. No mocking core system components
2. Evidence-based claims only
3. Zero-defect tolerance

## Level Documentation
- @docs/L0-foundation.md
- @docs/L1-feedback-loops.md
```

Every referenced doc must be reachable from CLAUDE.md — it serves as the master index. An agent discovers any project document by starting here and following `@filename.md` links.

**Anti-Pattern**: Writing tutorials or extensive guides in CLAUDE.md. Every line beyond 150 displaces context the agent needs for the actual task. Link to docs instead.

**Cross-References**: [Pattern 0.6](#pattern-06--ai-as-new-starter-standard) tests whether CLAUDE.md succeeds. [Pattern 0.7 — Documentation as Contract](#pattern-07--documentation-as-contract) covers keeping docs in sync with code.

---

## Pattern 0.5 — Git Worktree-Based Development

**Problem**: Multiple agents working on the same codebase create conflicts. Switching branches leaves artifacts. Experiments risk the main branch. Context carries over between sessions, creating hidden state.

**Solution**: Use git worktrees as the default working model. Each task or feature branch gets its own working directory — sharing the same git object store but with separate working trees.

**In Practice**:

Worktree management can be manual, but is most effective when automated through agent skills. The [obra/superpowers](https://github.com/obra/superpowers) framework provides a **[using-git-worktrees](https://github.com/obra/superpowers)** skill that automates worktree creation with smart directory selection and safety verification — agents create isolated worktrees at the start of feature work without manual `git worktree` commands.

```bash
# Manual equivalent (agents typically use the skill instead)
git worktree add .worktrees/feature-x feature-x
cd .worktrees/feature-x
# ... make changes, commit, test ...
git worktree remove .worktrees/feature-x
```

Benefits:
- **Parallel isolation**: Multiple agents on separate branches without conflict
- **Clean slate**: No leftover artifacts from previous sessions
- **Non-destructive**: Experiment without risking the main branch
- **Deterministic state**: Worktrees created from a known commit

Convention: `.worktrees/<branch-name>/` directory.

**Anti-Pattern**: Working directly on main for feature work. Agents should never modify main without explicit instruction.

**Cross-References**: [L2: Skills](L2-behavioral-guardrails.md) can enforce worktree usage via hooks. [L3: Optimization](L3-optimization.md) benefits from deterministic starting states. See [Further Reading](docs/references/further-reading.md) for the superpowers framework.

---

## Pattern 0.6 — AI-as-New-Starter Standard

**Problem**: Projects accumulate implicit knowledge. "Oh, we always put types in `src/types/`" or "utils files are in `shared/`" — assumptions never written down. Each assumption is a point where an agent will go wrong.

**Solution**: If someone with zero context cannot understand your project from CLAUDE.md + README + file structure alone, the project is not agentic-ready. Every assumption not codified in these entry points creates friction for AI agents.

**In Practice**:
- Test by asking: "Would a new developer understand this from README alone?"
- Put answers in CLAUDE.md, not tribal knowledge
- Let file structure tell the story
- Explicit conventions over implicit ones

**Anti-Pattern**: "They should just read the code." Code shows what exists, not why. AI agents need intent and structure, not just implementation.

**Cross-References**: [Pattern 0.4](#pattern-04--claude-md-as-project-constitution) specifies CLAUDE.md format. [L4: New Starter Audit](L4-standards-measurement.md#pattern-43--new-starter-standard) covers maintaining this over time.

---

## Pattern 0.7 — Documentation as Contract

**Problem**: Stale documentation is worse than no documentation. When docs are outdated, agents follow them with false confidence, leading to wasted tokens, incorrect implementations, and cascading errors. Documentation freshness is often treated as a one-time task rather than a continuous obligation.

**Solution**: **Treat documentation as a living contract with the codebase.** When code changes, update the corresponding documentation in the SAME task—not deferred to "later." Every change that affects behavior must include a corresponding documentation update.

The CLAUDE.md master index pattern (from [Pattern 0.4](#pattern-04--claude-md-as-project-constitution)) is the enforcement mechanism: documentation not linked from CLAUDE.md is orphaned and therefore dead. Link validation is part of the contract.

**Key principles:**
- **Synchronous updates:** Code changes and doc updates happen in the same task
- **Reference integrity:** All docs must be reachable from CLAUDE.md via link chains
- **Version-aware docs:** When patterns evolve, mark old versions as deprecated and link to current ones
- **Example currency:** Code examples in docs must match the current codebase

**In Practice**:

**Before starting a task:**
1. Read the relevant documentation sections
2. Verify the examples match current code
3. If docs are stale, flag it before proceeding

**During implementation:**
1. Make code changes
2. IMMEDIATELY update affected docs
3. Update CLAUDE.md links if structure changed
4. Run link validation to catch orphans

**Example task flow:**
```
Task: Refactor authentication flow

1. Read L1/L2 patterns for auth
2. Implement new auth logic
3. Update L1/L2 pattern docs with new flow
4. Update CLAUDE.md if patterns moved
5. Verify: grep -r "old_auth_function" docs/
6. Commit: Code + docs together
```

**Never defer:**
- "I'll update the docs in a separate PR"
- "The docs are close enough for now"
- "I'll document this when the feature is complete"

**Anti-Pattern**: "Good enough" documentation ("the agent can figure it out"). Deferred updates (code changes + doc ticket for "later"). Orphaned content not linked from CLAUDE.md. Unverified examples. Zombie docs kept around — version control is the archive.

**Cross-References**: [Pattern 0.4](#pattern-04--claude-md-as-project-constitution) establishes the master index mechanism. [Pattern 4.2 — Spec Drift Detection](L4-standards-measurement.md#pattern-42--spec-drift-detection) provides automated checks for doc freshness. [Pattern 4.3 — New Starter Standard](L4-standards-measurement.md#pattern-43--new-starter-standard) is the ultimate test for entry point clarity.

---

## Pattern 0.8 — Aggressive Cleanup

**Problem**: Dead code, unused imports, stale comments, and deprecated files accumulate over time. Every file an agent reads is context that could displace something important. Unused code is not harmless legacy—it's noise that degrades agent performance by consuming context window and creating confusion about what's actually used.

**Solution**: **Treat cleanup as a continuous practice, not a quarterly sprint.** When you find dead code during a task, remove it as part of that task. Every task should leave the codebase cleaner than it found it.

**Cleanup scope:**
- **Unused imports:** Remove imports that aren't referenced
- **Dead code:** Remove functions, classes, and methods that aren't called
- **Stale comments:** Remove comments that duplicate the code or are outdated
- **Deprecated files:** Remove files marked as deprecated or unused
- **Superseded documentation:** Delete docs that no longer reflect the system — do not move them to an `archive/` directory. Version control preserves history; keeping stale docs pollutes context and creates ambiguity about what's current.
- **TODO comments:** Either do the task or remove the TODO
- **Debug code:** Remove print statements, debug logging, temporary files

**Detection tools:**
```bash
# Unused imports (Python)
$ ruff check --select F401

# Dead code detection
$ vulture myproject/

# Find stale TODOs
$ grep -r "TODO" --include="*.py" | grep "201[0-9]"  # Old TODOs

# Find deprecated markers
$ grep -r "deprecated" --include="*.py"
```

**In Practice**:

**During any task:**
1. Use the relevant file
2. Notice dead code nearby
3. Remove it as part of the same commit
4. Verify nothing breaks (run tests)
5. Note the cleanup in commit message

**Example:**
```
Task: Fix authentication bug

1. Open auth.py to fix bug
2. Notice unused function: old_auth_method()
3. Search codebase: grep -r "old_auth_method" → only definition found
4. Remove function
5. Run tests: pytest tests/auth/ → pass
6. Commit: "Fix auth bug and remove unused old_auth_method"
```

**Targeted cleanup sessions:**
```bash
# Find and remove unused imports
$ ruff check --select F401 --fix .

# Find large comment blocks
$ find . -name "*.py" -exec wc -l {} \; | sort -n | tail -20
# Review top 20 files for excessive comments

# Find stale files (not modified in 2+ years)
$ find . -name "*.py" -mtime +730 -ls
```

**Commit message pattern:**
```
[Primary task description]

Cleanup:
- Remove unused imports in X files
- Delete dead function: old_auth_method()
- Remove stale TODO comments from 2023
```

**Anti-Pattern**: "Just in case" retention. Commented-out code. Defensive cleanup avoidance ("someone might be using this"). Cleanup theater (removing a few imports but leaving major dead code). Deferred cleanup. Archive directories.

**Cross-References**: [Pattern 4.1 — Evidence-Based Claims](L4-standards-measurement.md#pattern-41--evidence-based-claims) establishes the standard for verifying cleanup doesn't break anything. [Pattern 4.2 — Spec Drift Detection](L4-standards-measurement.md#pattern-42--spec-drift-detection) provides automated tools for detecting dead code. [Pattern 0.4](#pattern-04--claude-md-as-project-constitution) requires removing docs for deleted code.

---

## Related Patterns

- **L1: Feedback Loops** — Testing at module boundaries validates deep module design
- **L2: Behavioral Guardrails** — Skills enforce structural conventions during implementation
- **L3: Optimization** — Good structure reduces token overhead for navigation
- **L4: Standards & Measurement** — Maturity practices: evidence-based discipline, drift detection, metrics

## Further Reading

- John Ousterhout, *A Philosophy of Software Design* — Deep modules concept
- Matt Pocock, "Your codebase is NOT ready for AI" — Graybox modules, progressive disclosure
- @docs/references/further-reading.md

## Practitioner Insight

> "I don't think software engineering is dead with AI: in fact, quite the opposite."
> — Peter Steinberger, creator of OpenClaw

Agentic development demands more structure and discipline than traditional development, not less. L0's patterns — deep modules, progressive disclosure, a clear project constitution — exist because agents need well-defined entry points and clean interfaces even more than humans do. The overhead of getting these right pays dividends in every agent session that follows.

---

**Next:** [L1: Feedback Loops — Closed-Loop Testing](L1-feedback-loops.md) | [Back to Overview](../README.md)
