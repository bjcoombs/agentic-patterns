# Skills Examples

This directory contains skill templates and examples demonstrating the skill overlay architecture from @L2-behavioral-guardrails.md#pattern-21-skill-overlay-architecture.

## What Are Skills?

Skills are markdown files that extend Claude Code's base capabilities (superpowers) with project-specific rules, hook activations, and integration points. They are the mechanism by which a project's constitution (CLAUDE.md) becomes executable behavior.

## File Structure

```
.claude/skills/
├── skill-name/
│   └── SKILL.md          # Skill definition (frontmatter + content)
└── another-skill/
    └── SKILL.md
```

Each skill gets its own directory named after the skill. The skill definition is always named `SKILL.md`.

## Skill Discovery

Claude Code automatically discovers skills in the `.claude/skills/` directory. When you invoke a skill by name, Claude loads the skill definition and applies its rules, hooks, and workflow.

## Frontmatter Format

Every skill must declare:
- `name`: The skill identifier (used for invocation)
- `description`: One-line summary of what the skill does
- `base`: The superpower this skill extends (optional, for skills that extend base capabilities)

```yaml
---
name: tdd-nodejs-plus
description: Test-driven development with full-loop assertions for Node.js
base: superpowers:test-driven-development
---
```

## Skill Anatomy

A skill file contains:

1. **Purpose** — What this skill achieves and why it exists
2. **When to Activate** — Trigger conditions for using this skill
3. **Rules** — Project-specific constraints this skill enforces
4. **Hook Activations** — What guards this skill triggers (PreToolUse, PostToolUse, context-aware)
5. **Integration Points** — How this skill composes with others in the workflow chain
6. **Checklist** — Steps the agent follows when using this skill

## Templates

### SKILL-TEMPLATE.md

A blank skill template with annotated sections. Copy this file to create new skills. Fill in each section following the template structure.

### example-tdd-skill.md

A concrete TDD skill for a hypothetical Node.js ecommerce project. Demonstrates:
- Extending `superpowers:test-driven-development`
- Constitutional rules (no mocking database, no mocking HTTP clients)
- Hook declarations (track source edits, block mock imports)
- Integration with other skills (plan+, verify+, review+)
- Full RED-GREEN-REFACTOR checklist with full-loop assertions

## Usage

1. Copy `SKILL-TEMPLATE.md` to your project's `.claude/skills/your-skill-name/SKILL.md`
2. Fill in each section with your project-specific rules and workflow
3. Reference your skill in CLAUDE.md or invoke it directly by name
4. Skills compose into the skill chain: brain+ -> plan+ -> tdd+ -> verify+ -> review+

## Related Documentation

- @L2-behavioral-guardrails.md — Complete behavioral guardrails framework
- @L2-behavioral-guardrails.md#pattern-21-skill-overlay-architecture — Skill overlay pattern
- @L2-behavioral-guardrails.md#pattern-22-the-skill-chain — Workflow composition
