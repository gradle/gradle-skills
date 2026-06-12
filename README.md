# Gradle Skills

A collection of skills for AI coding agents working in Gradle projects. Skills are packaged instructions and references that extend agent capabilities.

Skills follow the [Agent Skills](https://agentskills.io/) format.

## Available Skills

### gradle-best-practices

Audits a project's Gradle build against the [official Gradle best practices](https://docs.gradle.org/current/userguide/best_practices.html), produces a prioritized findings report, and **proposes code changes** to bring the build into compliance. Covers both Gradle scripts and Java/Kotlin/Groovy sources under `buildSrc/` and `build-logic/`.

The best-practices catalog is **fetched live from `docs.gradle.org` on every run** — the skill ships no embedded list, so it always reflects the latest published documentation across all seven categories (general, structuring builds, dependencies, tasks, performance, security, testing). Requires network access.

**Use when:**

- "Check my build"
- "Audit gradle"
- "Best practices review"
- "Apply best practices to my build"

## Installation

Install into Claude Code, Codex, Gemini, Cursor, and other supported agents via [`skills.sh`](https://skills.sh/):

```bash
npx skills add gradle/gradle-skills
```

To install a specific skill only:

```bash
npx skills add gradle/gradle-skills --skill gradle-best-practices
```

If `npx` is not found, install Node first (e.g. `brew install node`).

## Usage

Skills are automatically available once installed.
The agent will use them when relevant tasks are detected.

**Examples:**

```text
Check this Gradle project against best practices
```

## Skill Structure

Each skill contains:

- `SKILL.md` — instructions for the agent (with YAML frontmatter describing when to activate)
- `metadata.json` — version, organization, abstract, references
- `references/` — supporting documentation the skill loads on demand (optional)

## Repository Layout

```
.
├── skills.sh.json                  # Manifest with topic groupings
└── skills/
    └── <skill_name>/
        ├── SKILL.md
        ├── metadata.json
        └── references/             # optional
            └── *.md                # optional
```

## License

Apache License 2.0 — see [LICENSE](LICENSE).
