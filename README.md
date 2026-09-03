# Gradle Skills

A collection of skills for AI coding agents working in Gradle projects. Skills are packaged instructions and references that extend agent capabilities.

Skills follow the [Agent Skills](https://agentskills.io/) format.

**The skills are harness-agnostic.** They contain no vendor- or tool-specific instructions and work in any agent that supports the Agent Skills format. They assume only capabilities every coding agent has: reading files, matching glob patterns, fetching URLs, and running shell commands.

This repository is *additionally* packaged as a Claude Code plugin marketplace, for teams that distribute tooling that way. That is a convenience, not the primary distribution channel — see [Installation](#installation).

## Available Skills

### gradle-best-practices

Audits a project's Gradle build against the [official Gradle best practices](https://docs.gradle.org/current/userguide/best_practices.html), produces a prioritized findings report, and **proposes code changes** to bring the build into compliance. Covers both Gradle scripts and Java/Kotlin/Groovy sources under `buildSrc/` and `build-logic/`.

The best-practices catalog is **fetched live from `docs.gradle.org` on every run** — the skill ships no embedded list, so it always reflects the latest published documentation across all seven categories (general, structuring builds, dependencies, tasks, performance, security, testing). Requires network access.

**Use when:**

- "Check my build"
- "Audit gradle"
- "Best practices review"
- "Apply best practices to my build"

### gradle-cli

Runs Gradle builds and tasks from the command line with `gradle` or the `./gradlew` wrapper, and produces the exact, copy-pasteable command for any invocation — using the flags valid for the project's Gradle version (7.0–9.x) and the tasks defined in the current project. It orients first (wrapper vs. system Gradle, the project's declared version, the installed version), discovers built-in and project-custom tasks, then runs the command or hands it over. Covers task selection in multi-project builds, the full grouped flag catalog, version-by-version flag differences, and wrapper operations (add/use/upgrade, including the run-the-task-twice step, SHA-256 verification, and authenticated distributions).

**Use when:**

- "Run the tests" / "build this project" / "run X task"
- "Upgrade the gradle wrapper"
- "How do I run …" / "what's the gradle command for …"
- "List the gradle tasks"

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

For teams that already distribute tooling as Claude Code plugins, this repository also doubles as a plugin marketplace. It installs the same skills — nothing here is Claude-specific — so use it only if the plugin workflow is what you want.

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
