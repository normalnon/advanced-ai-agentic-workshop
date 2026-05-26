---
name: tdd
description: "Enforce disciplined RED-GREEN-REFACTOR cycles using **separate subagents** for test writing and implementation. The core innovation: **the Test Wri..."
---

# tdd

> **Path within category:** `tdd/SKILL.md`


# Test-Driven Development — Multi-Agent Orchestration

Enforce disciplined RED-GREEN-REFACTOR cycles using **separate subagents** for test writing and implementation. The core innovation: **the Test Writer never sees implementation code, and the Implementer never sees the specification.** This prevents the LLM from leaking implementation intent into test design.

## When to Use

- User requests TDD, test-first, or red-green-refactor workflow
- User says `/tdd` with a feature description or bug report
- User wants to add a feature with test coverage enforced from the start
- User wants to fix a bug by first writing a reproducing test

## Invocation Modes

| Invocation | Behavior |
|-----------|----------|
| `/tdd <feature>` | Interactive mode — pause for approval at slices and each RED checkpoint |
| `/tdd --auto <feature>` | Autonomous mode — run all slices without pausing; stop ONLY on unrecoverable errors |
| `/tdd --resume` | Resume from `.tdd-state.json` in project root |
| `/tdd --dry-run <feature>` | Validation mode — runs Phase 0 + Phase 1 fully, renders all prompts, but skips `Task()` calls. No code is written. |

In `--auto` mode, skip all `[HUMAN CHECKPOINT]` steps. Print status lines instead:

```
[auto] RED  slice 1/4: "validates email format" — test failing as expected
[auto] GREEN slice 1/4: passing (attempt 1)
[auto] REFACTOR slice 1/4: 1 suggestion applied, 0 skipped
```

Stop and ask the user ONLY when:
- Implementation fails after 5 attempts
- Regressions cannot be auto-fixed after 3 attempts
- A script error makes it impossible to continue (missing binary, permission denied, etc.)

In `--dry-run` mode, validate the entire orchestration pipeline without executing any subagents or writing any code:

1. **Phase 0 runs fully**: detect framework, verify baseline, extract API, discover docs, create state file
2. **Phase 1 runs fully**: decompose into slices (still requires user approval)
3. **For each slice**: render all three agent prompts (Test Writer, Implementer, Refactorer) with actual variables. Print rendered prompts to the user with character counts.
4. **No `Task()` calls are made**. No test files are written. No implementation code is generated.
5. **Validate**: check that all template variables resolve (no `{UNRESOLVED}` placeholders), all scripts execute without error, and the state file is well-formed.
6. **Report summary**:

```
DRY RUN COMPLETE: {feature name}

Phase 0:
  Framework: {framework}
  Language: {language}
  Baseline: {pass|greenfield}
  API surface: {line count} lines
  Doc context: {line count} lines (or "none")

Phase 1:
  Slices: {N} ({layer breakdown})

Prompts rendered: {N * 3} (all variables resolved)
  Test Writer:   {char count} chars
  Implementer:   {char count} chars
  Refactorer:    {char count} chars

State file: .tdd-state.json written
No code was modified.
```

This mode is useful for:
- Validating that scripts work in the project's environment
- Reviewing prompt content before committing to a full TDD run
- Testing skill changes without side effects

## Architecture Overview

```
ORCHESTRATOR (you, reading this file)
├─ Phase 0: Setup — detect framework, extract API, create state file
├─ Phase 1: Decompose into vertical slices → user approves
│
├─ FOR EACH SLICE:
│   ├─ Phase 2 (RED):    Task(Test Writer)  ← spec + API only
│   ├─ Phase 3 (GREEN):  Task(Implementer)  ← failing test + error only
│   └─ Phase 4 (REFACTOR): Task(Refactorer) ← all code + green results
│
└─ Summary
```

### Context Boundaries (the key constraint)

| Agent | Sees | Does NOT See |
|-------|------|-------------|
| **Test Writer** | Slice spec, public API signatures, framework conventions, layer constraints | Implementation code, other slices, implementation plans |
| **Implementer** | Failing test code, test failure output, file tree, existing source, layer constraints | Original spec, slice descriptions, future plans |
| **Refactorer** | All implementation + all tests + green results, layers touched | Original spec, decomposition rationale |

## Workflow

### Phase 0: Setup (once per session)

**Step 1**: Detect framework and test runner.

```
Check for: package.json (jest/vitest), pyproject.toml/pytest.ini (pytest),
go.mod (go test), Cargo.toml (cargo test), Gemfile (rspec), composer.json (phpunit)
```

If ambiguous, ask: "What command runs your tests? (e.g., `npm test`, `pytest`)"

**Step 2**: Detect language from source files (for agent prompts):

```
TypeScript (.ts/.tsx), JavaScript (.js/.jsx), Python (.py), Go (.go), Rust (.rs), Ruby (.rb), PHP (.php)
```

**Step 3**: Verify green baseline.

```bash
bash ~/.claude/skills/tdd/scripts/run_tests.sh {FRAMEWORK} "{TEST_COMMAND}"
```

Parse the JSON output.

- If `status` is `"pass"`: proceed.
- If `status` is `"fail"`: stop — "Existing tests are failing. TDD starts from a green baseline."
- If `status` is `"error"` AND `total` is 0: **greenfield project** — no tests exist yet. This is fine. Proceed.

**Step 4**: Extract the public API surface.

```bash
bash ~/.claude/skills/tdd/scripts/extract_api.sh {SOURCE_DIR}
```

Save the output — this is what the Test Writer will see. If empty (greenfield), that's expected.

**Step 5**: Discover project documentation.

```bash
bash ~/.claude/skills/tdd/scripts/discover_docs.sh {PROJECT_ROOT} --lang {LANGUAGE}
```

This searches for:
- **Documentation files**: README, ARCHITECTURE.md, docs/ folder, DESIGN.md, SPEC files, ADRs
- **API specifications**: OpenAPI/Swagger, GraphQL schemas, .proto files
- **Source docstrings**: JSDoc, Python docstrings, Go doc comments, Rust `///` comments

Save the output as `{DOC_CONTEXT}`. This feeds into:
- **Phase 1** — so slice decomposition is informed by documented behavior and API contracts
- **Phase 2** — so the Test Writer writes tests aligned with documented intent, not just code signatures

If empty (no docs found), that's fine — proceed without doc context.

**Step 6**: Create the state file `.tdd-state.json` in the project root:

```json
{
  "feature": "user's feature description",
  "framework": "jest|vitest|pytest|go|cargo|rspec|phpunit",
  "language": "typescript|javascript|python|go|rust|ruby|php",
  "test_command": "the full test command",
  "source_dir": "src/",
  "doc_context": "output from discover_docs.sh (or empty string)",
  "auto_mode": false,
  "dry_run": false,
  "slices": [],
  "current_slice": 0,
  "phase": "setup",
  "layer_map": {},
  "files_modified": [],
  "test_files_created": []
}
```

Each slice in the `slices` array includes a `layer` field: `"domain"`, `"domain-service"`, `"application"`, or `"infrastructure"`. See Phase 1 for how layers are assigned.

The `layer_map` maps directory prefixes to layers. Built during Phase 1 from project structure:

```json
{
  "layer_map": {
    "src/domain/": "domain",
    "src/services/": "domain-service",
    "src/application/": "application",
    "src/infrastructure/": "infrastructure",
    "src/adapters/": "infrastructure",
    "src/controllers/": "infrastructure"
  }
}
```

If the project has no clear directory-layer mapping (flat structure), set `layer_map` to `{}` and skip path-based validation.

**Step 5a** (auto-detect layer_map): If `layer_map` is empty, scan the source directory for common DDD/layered architecture directory names and auto-populate:

```
Common directory → layer mappings (check if directories exist):
  */domain/       → "domain"
  */models/       → "domain"          (ORM models often serve as domain entities)
  */entities/     → "domain"
  */value_objects/ → "domain"
  */services/     → "application"     (unless clearly infrastructure)
  */application/  → "application"
  */use_cases/    → "application"
  */core/         → "application"
  */infrastructure/ → "infrastructure"
  */adapters/     → "infrastructure"
  */controllers/  → "infrastructure"
  */api/          → "infrastructure"
  */bot/          → "infrastructure"  (Telegram/Discord bot handlers)
  */handlers/     → "infrastructure"
  */repositories/ → "infrastructure"  (concrete repo implementations)
```

Only add entries for directories that actually exist in the source tree. If fewer than 2 directories match, leave `layer_map` empty (flat project). Present the auto-detected map to the user for confirmation:

```
Auto-detected layer map from directory structure:
  src/models/     → domain
  src/services/   → application
  src/core/       → application
  src/bot/        → infrastructure
  src/api/        → infrastructure

Does this mapping look correct? (adjust if needed)
```

**Update state**: `"phase": "setup"`. Write state file immediately.


### Dry-Run Phase Override (Phase 2–4)

In `--dry-run` mode, **replace Phases 2–4 entirely** with the following for each slice:

1. Refresh API surface (`extract_api.sh`)
2. Render the **Test Writer prompt** with all variables filled in. Print it under a `### Test Writer Prompt (slice N)` heading.
3. Render the **Implementer prompt** using placeholder test code: `"(dry-run: test code would be generated by Test Writer)"` for `{FAILING_TEST_CODE}` and `"(dry-run: no test output)"` for `{TEST_FAILURE_OUTPUT}`.
4. Render the **Refactorer prompt** using placeholder values: `"(dry-run: no green output)"` for `{GREEN_TEST_OUTPUT}`, `"(dry-run: code from Test Writer)"` for `{ALL_TEST_CODE}`, `"(dry-run: code from Implementer)"` for `{ALL_IMPLEMENTATION_CODE}`.
5. For each rendered prompt, verify no `{UNRESOLVED_VARIABLE}` patterns remain (regex: `\{[A-Z][A-Z_]+\}`). Report any unresolved variables as errors.
6. Print character counts for each prompt.
7. Move to next slice (no `Task()` calls, no file writes, no test runs).

After all slices are processed, print the dry-run summary and exit. Do NOT clean up the state file — it's useful for subsequent `--resume`.


### Phase 3: GREEN — Minimal Implementation

**Step 1**: Read the failing test file and the test failure output (the full `raw_tail` from the RED phase run_tests.sh result).

**Step 2**: Build the file tree of source files (not test files, not node_modules, etc.):

```bash
find {SOURCE_DIR} -type f \( -name '*.ts' -o -name '*.js' -o -name '*.py' -o -name '*.go' -o -name '*.rs' -o -name '*.rb' -o -name '*.php' \) | grep -v test | grep -v spec | grep -v node_modules | grep -v __pycache__ | grep -v vendor | grep -v target | grep -v dist | grep -v build | head -50
```

**Step 3**: Read existing source files that the test imports or references.

**Step 4**: Read the prompt template from `references/agent_prompts.md` -> "Implementer Agent" section. Fill in:

- `{LANGUAGE}`: Detected language
- `{FAILING_TEST_CODE}`: The complete test file content
- `{TEST_FAILURE_OUTPUT}`: The `raw_tail` from run_tests.sh JSON output
- `{FILE_TREE}`: Source file listing from Step 2
- `{EXISTING_SOURCE}`: Content of relevant source files (if any — may be empty for greenfield)
- `{LAYER}`: The slice's layer tag from Phase 1
- `{LAYER_DEPENDENCY_CONSTRAINT}`: Layer-specific dependency constraint (see agent_prompts.md -> Layer-Specific Constraint Lookup)

On retries (attempt > 1), also fill in the `{?PREVIOUS_ATTEMPT}` section:
- `{PREVIOUS_ATTEMPT_DESCRIPTION}`: the `explanation` field from the failed attempt
- `{PREVIOUS_ATTEMPT_ERROR}`: the `raw_tail` from the test run after the failed attempt

**CRITICAL**: Do NOT include the slice specification, feature description, or any future plans. The Implementer works from the test alone.

**Step 5**: Launch the Implementer agent:

```
Task(subagent_type="general-purpose", prompt=<constructed prompt>)
```

**Step 6**: Parse the JSON response. **Validate layer boundaries**, then apply file changes.

**Step 6a** (Layer path validation): If `layer_map` is not empty, check each file path in the response against the current slice's layer:

```
For each file in response.files:
  inferred_layer = lookup file.path against layer_map (longest prefix match)
  if inferred_layer exists AND inferred_layer != current_slice.layer:
    if inferred_layer is OUTER relative to current_slice.layer:
      REJECT: "Implementer created/modified {file.path} which belongs to
      the {inferred_layer} layer, but this is a {current_slice.layer} slice.
      Inner layers must not depend on outer layers."
      → Re-launch Implementer with appended constraint:
        "Do NOT create or modify files in {inferred_layer} directories.
        This slice is {current_slice.layer} only."
    if inferred_layer is INNER relative to current_slice.layer:
      ALLOW: outer layers may touch inner-layer files (e.g., adding a port interface)
```

Layer ordering for "outer" check: domain < domain-service < application < infrastructure.

If `layer_map` is empty (flat project), skip this validation.

**Step 6b**: Apply validated file changes:

For each file in the response `files` array:
- If `action` is `"create"` or `"overwrite"`: Use the Write tool to create or overwrite the file with the complete content
- If `action` is `"edit"` (used for existing files over 200 lines): Use the Edit tool with `old_string` → `new_string` to apply the changes. The Implementer returns only the changed functions with surrounding context — identify the insertion point or the function being replaced, and use Edit tool accordingly. If the edit target is ambiguous, fall back to reading the full file and using Write.
- For existing files over 200 lines where the Implementer returned full content anyway (action = "overwrite"), prefer using Edit tool to apply only the diff — this prevents accidental reformatting of untouched code

**Step 7**: Run the specific test:

```bash
bash ~/.claude/skills/tdd/scripts/run_tests.sh {FRAMEWORK} "{TEST_COMMAND_FOR_SPECIFIC_TEST}"
```

**Step 8**: RETRY LOOP (if test still fails):

```
attempt = 1
max_attempts = 5
previous_explanation = null
previous_error = null

while status != "pass" AND attempt <= max_attempts:
    previous_explanation = explanation from last Implementer response
    previous_error = raw_tail from last test run

    Launch FRESH Task(Implementer) with:
      - same test code + file tree + existing source (re-read!)
      - NEW failure output
      - PREVIOUS_ATTEMPT section filled in

    Apply changes (Write tool for each file)
    Re-run test
    attempt += 1

if still failing after max_attempts:
    STOP. Present to user:
    "Implementation failed after 5 attempts. Last error: {raw_tail}"
    Ask: "Adjust the test, try a different approach, or debug manually?"
```

Each retry is a **fresh** Task call with only the previous attempt's explanation and error. This prevents the Implementer from going down rabbit holes while giving it enough context to try a different strategy.

**Step 9**: Once the specific test passes, run the FULL test suite:

```bash
bash ~/.claude/skills/tdd/scripts/run_tests.sh {FRAMEWORK} "{FULL_TEST_COMMAND}" --all
```

**Step 10**: Handle regressions:

| Result | Action |
|--------|--------|
| All pass | Proceed to REFACTOR |
| Regressions found | Auto-fix: launch a fresh Implementer with the regression test failures. Apply. Re-run full suite. Repeat up to 3 times. If still failing after 3 regression-fix attempts, STOP and present to user. |

**Step 11** (interactive mode only — skip in `--auto`): Present to the user:

```
GREEN: Test passing with minimal implementation.

Implementation: {explanation from agent response}
Files changed: {list}
All tests: {passed} passing, {failed} failing

Proceed to REFACTOR phase? (or adjust?)
```

**Update state**: `"phase": "green"`, update `files_modified`. Write state immediately.

**Step 12** (domain/domain-service slices only): Layer purity check before REFACTOR:

For each new/modified file in a `domain` or `domain-service` layer slice:
- **Import scan**: Read all import/require statements. Check each imported module against `layer_map`. Flag any import from an outer layer as a violation.
- **Constructor check**: Verify constructor takes NO parameters typed from outer layers (no ORM sessions, HTTP clients, framework configs)
- **Static call check**: No static method calls to outer-layer code
- If violations found, fix them now (move the dependency to a port interface) before entering REFACTOR

**Step 13**: Full-repo import scan (all layers, runs once per slice):

Scan ALL source files (not just session-modified) for dependency direction violations:

```bash
# For each source file, extract imports and check against layer_map
# Language-specific patterns:
#   Python: from X import Y, import X
#   TypeScript/JS: import ... from 'X', require('X')
#   Go: import "X"
```

For each file:
1. Determine its layer from `layer_map` (skip if no match)
2. For each import, determine the imported module's layer from `layer_map`
3. If imported layer is OUTER relative to file's layer → violation

Report violations to the user before REFACTOR:

```
Layer scan found N dependency direction violation(s):
- domain/user.py imports infrastructure/db.py (domain → infrastructure)
- domain/services/registration.py imports adapters/email.py (domain-service → infrastructure)
```

In `--auto` mode: attempt auto-fix (replace concrete import with port interface). In interactive mode: present violations and ask user how to proceed.

This supplements the Refactorer's import checking (which only sees session files) with a repo-wide scan. Static tools miss ~23% of violations (Pruijt et al., 2017) — combining textual + structural checks improves coverage.


### Phase 5: Next Slice or Complete

If more slices remain -> increment `current_slice` in state, return to Phase 2.

If all slices complete -> present summary:

```
TDD Complete: {feature name}

Slices implemented: N
Tests written: N
Files created/modified: {list}
All tests passing: yes
```

Clean up: remove `.tdd-state.json` (in `--auto` mode, remove silently; in interactive, ask user).


## Edge Cases

### Greenfield Projects

No source files, no tests, no test configuration. Handle gracefully:

1. **Phase 0 Step 3**: If run_tests.sh returns `status: "error"` with `total: 0`, check if any test files exist. If none, this is greenfield — proceed.
2. **Phase 0 Step 4**: extract_api.sh will return empty output. Pass `"(No existing API — this is a new project)"` to the Test Writer.
3. **Phase 2**: The Test Writer will create test files from scratch. May need to set up the test framework config (e.g., `jest.config.js`, `pytest.ini`). If the first test run fails with a framework error (not a test failure), create minimal framework config and retry.

### Bug Fix TDD

1. Write a test demonstrating the bug (should FAIL showing the bug exists)
2. Confirm failure matches the reported bug — human checkpoint
3. Fix: minimal code to make test pass (GREEN phase as normal)
4. Verify: no regressions

### Existing Code (Characterization Tests)

1. Write a test for CURRENT behavior (should PASS — this is a characterization test)
2. Modify the test for DESIRED behavior (should FAIL)
3. Proceed with GREEN -> REFACTOR

### User-Provided Tests

If user provides test code:
1. Run to confirm it fails (RED confirmed)
2. Skip to Phase 3 (GREEN) — user-provided tests are authoritative
3. Do not modify without asking

### Flaky Tests

If a test sometimes passes/fails: stop, report, fix the flaky test before continuing.


## Layer Reference

See `references/layer_guide.md` for layer definitions, dependency rules, test strategies by layer, and detection heuristics.

## Anti-Patterns to Avoid

See `references/anti_patterns.md`. Critical ones:
- Never modify a test to make it pass (change implementation, not tests)
- Never write implementation before tests
- Never write all tests at once (vertical slicing)
- Never test implementation details
- Never skip the RED phase
- Never let domain code import infrastructure (dependency direction violation)
- Never mock domain objects — construct real instances instead
