# Gradle Skills

[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)

Packaged skills for AI coding agents working in Gradle projects, following the [Agent Skills](https://agentskills.io/) format. Harness-agnostic.

Also packaged as a Claude Code plugin marketplace. See [Installation](#installation).

## Available Skills

### gradle-best-practices [![v2.0.0](https://img.shields.io/badge/v2.0.0-02303A?logo=gradle&logoColor=white)](skills/gradle-best-practices)

Audits a Gradle build against the [official best practices](https://docs.gradle.org/current/userguide/best_practices.html), produces a prioritized findings report, and proposes fixes. Covers build scripts and sources under `buildSrc/` and `build-logic/`. The catalog is fetched live from `docs.gradle.org` on every run. Requires network access.

**Use when:**

- "Check my build"
- "Audit gradle"
- "Best practices review"
- "Apply best practices to my build"

### gradle-cli [![v1.3.0](https://img.shields.io/badge/v1.3.0-02303A?logo=gradle&logoColor=white)](skills/gradle-cli)

Runs Gradle builds and tasks via `./gradlew`, and produces the exact command for any invocation. Knows the right flags, task ordering, and invocation patterns for the project's Gradle version.

**Use when:**

- "Run the tests" / "build this project" / "run X task"
- "Upgrade the gradle wrapper"
- "How do I run …" / "what's the gradle command for …"
- "List the gradle tasks"

**[Evaluation results →](evals/gradle-cli-1.3.0.md)** v1.3.0 tested across 7 scenarios on Sonnet 5, Opus 5, and Deepseek V4 Flash.

## Installation

### Any agent (recommended)

Install into Claude Code, Codex, Gemini, Cursor, and other supported agents via [`skills.sh`](https://skills.sh/):

```bash
npx skills add gradle/gradle-skills
```

To install a specific skill only:

```bash
npx skills add gradle/gradle-skills --skill gradle-best-practices
```

If `npx` is not found, install Node first (e.g. `brew install node`).

This is the expected path for every agent, Claude Code included.

### Claude Code plugin marketplace (optional)

For teams that already distribute tooling as Claude Code plugins, this repository also doubles as a plugin marketplace.

```text
/plugin marketplace add gradle/gradle-skills
/plugin install gradle-skills@gradle-skills
```

Restart Claude Code afterwards. The plugin bundles every skill in this repository; unlike `skills.sh`, it cannot install a single skill.

To enable the marketplace and plugin for everyone working in a repository, commit this to its `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "gradle-skills": {
      "source": {
        "source": "github",
        "repo": "gradle/gradle-skills"
      }
    }
  },
  "enabledPlugins": {
    "gradle-skills@gradle-skills": true
  }
}
```

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
├── .claude-plugin/
│   ├── plugin.json                 # Claude Code plugin manifest
│   └── marketplace.json            # Claude Code marketplace catalog
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
