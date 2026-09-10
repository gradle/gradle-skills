# Gradle Skills

[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)

Packaged skills for AI coding agents working in Gradle projects, following the [Agent Skills](https://agentskills.io/home) format.
These skills are harness-agnostic.

The repository doubles as a Claude Code plugin marketplace.
See [Installation](#installation).

## Available Skills

### gradle-best-practices [![v1.0.0](https://img.shields.io/badge/v1.0.0-02303A?logo=gradle&logoColor=white)](skills/gradle-best-practices)

Audits a Gradle build against the [official best practices](https://docs.gradle.org/current/userguide/best_practices.html), produces a prioritized findings report, and proposes fixes. Covers build scripts and sources under `buildSrc/` and `build-logic/`. The catalog is fetched live from `docs.gradle.org` on every run. Requires network access.

**Use when:**

- "Check my build"
- "Audit gradle"
- "Best practices review"
- "Apply best practices to my build"

### gradle-cli [![v1.0.0](https://img.shields.io/badge/v1.0.0-02303A?logo=gradle&logoColor=white)](skills/gradle-cli) [![Evaluated: 7 scenarios, 3 models](https://img.shields.io/badge/evaluated-7%20scenarios%20%C3%97%203%20models-2ea44f)](evals/gradle-cli-1.0.0.md)

Runs Gradle builds and tasks via `./gradlew`, and produces the exact command for any invocation. Knows the right flags, task ordering, and invocation patterns for the project's Gradle version.

**Use when:**

- "Run the tests" / "build this project" / "run X task"
- "Upgrade the gradle wrapper"
- "How do I run …" / "what's the gradle command for …"
- "List the gradle tasks"

> 📊 [Evaluation results for v1.0.0 →](evals/gradle-cli-1.0.0.md)
>
> Scored across 7 scenarios on Sonnet 5, Opus 5, and Deepseek V4 Flash.

## Installation

### Any Agent (Recommended)

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

### Installation as a Plugin

[Agent Plugins](https://agent-plugins.org/) is the vendor-neutral standard for bundling skills and MCP servers into one installable package.
Installing the plugin is the easiest way to keep your local copies current with each release.
The standard deliberately leaves the installation procedure to each client, so consult your agent's documentation, or the [list of compatible clients](https://agent-plugins.org/compatible-clients), for the exact steps.

Two things follow from installing the plugin rather than the skills directly:

- **It is all or nothing.** The plugin's only contents are the two skills above, and it installs both. Unlike [`skills.sh`](https://skills.sh/), it cannot install one.
- **Skill names are client-specific.** The standard does not prescribe how a client names a skill it loads from a plugin. Claude Code prefixes them with the plugin name; other agents may expose them under their bare names.

#### Claude Code Plugin Installation Details

Claude Code does not yet implement the Agent Plugins standard.
This repository is therefore also a Claude Code plugin, published through a marketplace catalog in the same repository.
Its descriptor uses Claude Code's own plugin format, which puts the manifest at `.claude-plugin/plugin.json` rather than the package root.

For teams that already distribute tooling as Claude Code plugins:

```text
/plugin marketplace add gradle/gradle-skills
/plugin install gradle-skills@gradle-skills
```

Claude Code namespaces skills that come from a plugin, so these install as `gradle-skills:gradle-cli` and `gradle-skills:gradle-best-practices` rather than under their bare names.

To register the marketplace for everyone working in a project, commit this to the project's `.claude/settings.json`:

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

`extraKnownMarketplaces` registers the catalog the first time a collaborator who trusts the repository folder starts a session. `enabledPlugins` only keeps the plugin turned on once it is present — it does not fetch it.
Registering is not installing, so each collaborator still runs the install once:

```bash
claude plugin install gradle-skills@gradle-skills
```

No `/plugin marketplace add` is needed beforehand; the settings file already registered the marketplace.

## Usage

Skills are automatically available once installed.
The agent will use them when relevant tasks are detected.

**Examples:**

```text
Check this Gradle project against best practices
```

## Repository Structure

Even though all the skills here are harness-agnostic, this repository is laid out as a [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces): `.claude-plugin/` holds the marketplace catalog and the plugin manifest, and the plugin's contents — the `skills/` directory — sit at the repository root. `skills.sh.json` groups the skills by topic for `skills.sh`.

Each skill follows the [Agent Skills](https://agentskills.io/home) layout, plus a `metadata.json` recording its version, owning organization, abstract, and references.

## License

Apache License 2.0 — see [LICENSE](LICENSE).
