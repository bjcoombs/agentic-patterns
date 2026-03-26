---
name: skill-name
description: One-line description of what this skill does
base: superpowers:base-skill-name
---

# Skill Name

## Purpose

[What this skill achieves]

This skill extends the base `superpowers:base-skill-name` capability with project-specific rules and workflow constraints.

## When to Activate

[Trigger conditions — when should the agent use this skill]

Activate this skill when:
- [Condition 1]
- [Condition 2]
- [Condition 3]

## Rules

[Project-specific constraints this skill enforces]

1. **Rule name** — Description and rationale
2. **Rule name** — Description and rationale
3. **Rule name** — Description and rationale

These rules flow from the project's constitutional rules in CLAUDE.md and must not be violated.

## Hook Activations

[What hooks does this skill activate? What do they block/advise?]

**PreToolUse hooks:**
- [hook-name]: Blocks [operation] with reason [explanation]

**PostToolUse hooks:**
- [hook-name]: Tracks [state] and emits [warning/action]

**Context-aware hooks:**
- [hook-name]: Detects [condition] and [action]

## Integration Points

[What other skills does this compose with? What comes before/after?]

**Used by:**
- [skill-name] — [how this skill integrates]

**Feeds into:**
- [skill-name] — [what output this skill produces for the next skill]

**Dependencies:**
- [dependency] — [why it's required]

## Checklist

[Steps the agent must follow when using this skill]

1. [ ] [Step 1 — what to do, how to verify completion]
2. [ ] [Step 2 — what to do, how to verify completion]
3. [ ] [Step 3 — what to do, how to verify completion]
4. [ ] [Step 4 — what to do, how to verify completion]
5. [ ] [Step 5 — what to do, how to verify completion]

---

**Base capability**: `superpowers:base-skill-name`
**Skill version**: 1.0.0
**Last updated**: YYYY-MM-DD
