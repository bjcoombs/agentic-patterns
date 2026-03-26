---
name: tdd-nodejs-plus
description: Test-driven development with full-loop assertions for Node.js projects
base: superpowers:test-driven-development
---

# tdd+ — Node.js TDD with Full-Loop Assertions

## Purpose

Enforces test-driven development with full-stack testing for Node.js projects. Extends the base TDD workflow with project-specific constraints: no mocking databases or HTTP clients, full-loop assertion requirements, and test file tracking.

## When to Activate

Activate this skill when:
- Implementing new features or bug fixes
- Modifying existing behavior that requires test updates
- Writing tests for untested code paths

## Rules

1. **No database mocking** — Use real database connections in Docker containers. Mocking databases hides integration failures.
2. **No HTTP client mocking** — Use real HTTP clients against test servers. Mocking hides network and serialization failures.
3. **Full-loop assertion layering** — After primary assertions pass, verify second-order and third-order consequences:
   - Primary: Core behavior works
   - Second-order: Database state updated correctly
   - Third-order: Audit logs, notifications, downstream effects
4. **Test-first mandate** — Write failing tests before implementation. No exceptions.
5. **RED-GREEN-REFACTOR** — Follow strict TDD cycle:
   - RED: Write failing test, verify it fails for the right reason
   - GREEN: Implement minimum code to pass
   - REFACTOR: Clean up while keeping tests green

## Hook Activations

**PostToolUse hooks:**
- `track-source-edits`: When source files (`src/**/*.ts`) are edited, add to `pending-tests.json` and emit "TEST TASK REQUIRED"
- `track-test-edits`: When test files are edited, remove corresponding source files from `pending-tests.json`

**PreToolUse hooks:**
- `block-mock-imports`: Block attempts to import mock modules for database, HTTP, or blockchain clients
- `require-test-before-implementation`: When pending tests exist for a file, block implementation edits until test is written

## Integration Points

**Used by:**
- `plan+` skill — creates test plans as part of implementation planning

**Feeds into:**
- `verify+` skill — produces test results for verification
- `review+` skill — test output becomes part of compliance review

**Composes with:**
- `test-integrity` skill — validates test structure (no conditional assertions, no catch without rethrow)

## Checklist

When implementing with this skill:

1. [ ] **Identify test scope** — What behavior needs testing? What are the full-loop assertions?
2. [ ] **Write failing test (RED)** — Create test that fails for the expected reason
3. [ ] **Verify RED** — Run test, confirm it fails with clear error message indicating missing functionality
4. [ ] **Implement minimum code (GREEN)** — Write only what's needed to pass the test
5. [ ] **Verify GREEN** — Run test, confirm it passes
6. [ ] **Add full-loop assertions** — Extend test with second-order and third-order assertions
7. [ ] **Verify full-loop** — Run complete test suite, confirm all assertions pass
8. [ ] **Refactor** — Clean up code while keeping tests green
9. [ ] **Final verification** — Run full test suite, confirm no regressions

## Test File Conventions

```typescript
// test/integration/trading/swap.test.ts
describe('Swap execution', () => {
  it('should execute swap and update balances', async () => {
    // Arrange: Setup test state
    // Act: Execute the swap
    // Assert: Primary assertion
    expect(result.status).toBe('success');

    // Assert: Second-order (database state)
    const fromBalance = await getBalance(fromWallet);
    expect(fromBalance).toBe(initialFrom - amount);

    // Assert: Third-order (audit log)
    const auditLog = await getAuditLog(swapId);
    expect(auditLog).toMatchObject({
      type: 'SWAP_EXECUTED',
      from: fromWallet,
      to: toWallet,
      amount: amount
    });
  });
});
```

## Anti-Patterns to Avoid

- Writing implementation before tests
- Mocking database or HTTP clients
- Asserting only primary behavior without full-loop verification
- Skipping the refactor step
- Moving on when tests pass without understanding why

---

**Base capability**: `superpowers:test-driven-development`
**Skill version**: 1.0.0
**Last updated**: 2026-03-26
