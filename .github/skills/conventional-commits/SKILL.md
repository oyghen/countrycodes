---
name: conventional-commits
description: Write git commit messages that follow the Conventional Commits specification (type(scope): description, optional body and footers). Use whenever the user asks to write, draft, review, fix, or reword a commit message, summarize staged changes or a diff as a commit, or mentions "conventional commits", "commit message", "semantic commit", or changelog-friendly commits. Also use when choosing between types like feat, fix, docs, refactor, perf, test, build, ci, or chore, or when flagging breaking changes (! or BREAKING CHANGE footer). Do not use for pull request descriptions, release notes, or general git operations like rebasing or branching.
---

# Conventional Commits

Write and review commit messages using the Conventional Commits format:

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

## Choosing the message

- Use an established type that reflects the change: `feat` for user-facing functionality, `fix` for bug fixes, `docs` for documentation, `refactor` for behavior-preserving restructuring, `perf` for performance improvements, `test` for tests, `build` for build/dependency changes, `ci` for CI configuration, and `chore` for other maintenance.
- Add a concise scope when it helps identify the affected area, such as `feat(cli): ...`.
- Keep the description imperative, specific, and concise. Do not end it with a period.
- Add a body only when it clarifies why the change was made or important implementation context.
- Mark breaking changes with `!` after the type/scope and explain them in a `BREAKING CHANGE:` footer.
- Include issue references or other footers when supported by the task context.
- Follow repository-specific conventions when they add useful constraints, but preserve the Conventional Commits structure.

## Examples

```text
feat(countrycodes): add lookup by dial code
fix(cli): handle empty lookup results
chore: expose workspace tasks in Agents Run button
refactor(api)!: remove deprecated lookup method

BREAKING CHANGE: callers must use search_countries instead.
```

When drafting from a diff, summarize the intent of the change rather than listing modified files. When reviewing a proposed message, check its type, optional scope, description, and any breaking-change declaration against the actual change.
