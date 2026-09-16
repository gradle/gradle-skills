# Gradle Skills

[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)

Packaged skills for AI coding agents working in Gradle projects, following the [Agent Skills](https://agentskills.io/home) format.
These skills are harness-agnostic.

The repository doubles as a Claude Code plugin marketplace.
See [Installation](#installation).

## Available Skills

### gradle-best-practices [![v1.1.0](https://img.shields.io/badge/v1.1.0-02303A?logo=gradle&logoColor=white)](skills/gradle-best-practices)

Audits a Gradle build against the [official best practices](https://docs.gradle.org/current/userguide/best_practices.html), produces a prioritized findings report, and proposes fixes. Covers build scripts and sources under `buildSrc/` and `build-logic/`. The catalog ships with the skill under `references/` — 45 practices, verified against the Gradle 9.7.1 documentation — so every run checks the same things and no network access is needed.

**Use when:**

- "Check my build"
- "Audit gradle"
- "Best practices review"
- "Apply best practices to my build"

### gradle-wrapper-upgrade [![v1.0.0](https://img.shields.io/badge/v1.0.0-02303A?logo=gradle&logoColor=white)](skills/gradle-wrapper-upgrade)

Upgrades an existing Gradle wrapper — to the latest release, or to a version you name. Pins the distribution's SHA-256, preserves the existing distribution type, runs the `wrapper` task twice so the launch scripts and jar are regenerated from the new version's templates, and verifies by diff. Narrow by design — it does not add a wrapper to a project that has none.

**Use when:**

- "Upgrade the Gradle wrapper" / "bump Gradle to 8.14.4"
- "Update `distributionUrl`"
- "How do I upgrade the wrapper?"

## Installation

### As a Plugin (Recommended)

[Agent Plugins](https://agent-plugins.org/) is the vendor-neutral standard for bundling skills and MCP servers into one installable package.
This repository conforms to [Agent Plugins 1.0.0](https://github.com/agentplugins/agent-plugins-spec/blob/main/spec/1.0.0.md): the manifest is `plugin.json` at the repository root, and the skills are discovered from `skills/`.
The standard deliberately leaves the installation procedure to each client, so consult your agent's documentation, or the [list of compatible clients](https://agent-plugins.org/compatible-clients), for the exact steps.

Install the plugin rather than the individual skills.

Three things follow from installing the plugin:

- **It is all or nothing.** The plugin's contents are the skills above, and it installs all of them. Unlike [`skills.sh`](https://skills.sh/), it cannot install only one.
- **New skills will be added here.** A plugin update will pick up every new one.
- **Skill names are client-specific.** The standard does not prescribe how a client names a skill it loads from a plugin. Claude Code prefixes them with the plugin name; other agents may expose them under their bare names.

#### Claude Code Plugin Installation Details

Claude Code does not yet implement the Agent Plugins standard.
This repository is therefore also a Claude Code plugin, published through a marketplace catalog in the same repository.
Claude Code's own plugin format puts the manifest at `.claude-plugin/plugin.json` rather than the package root, so that descriptor exists alongside the root `plugin.json` and carries the same metadata.

In Claude Code, install with:

```text
/plugin marketplace add gradle/gradle-skills
/plugin install gradle-skills@gradle-skills
```

Claude Code namespaces skills that come from a plugin, so these install as `gradle-skills:gradle-best-practices` and `gradle-skills:gradle-wrapper-upgrade` rather than under their bare names.

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

### Any Agent, as Individual Skills

Where a plugin is not an option, or you want exactly one skill, install into Claude Code, Codex, Gemini, Cursor, and other supported agents via [`skills.sh`](https://skills.sh/):

```bash
npx skills add gradle/gradle-skills
```

To install a specific skill only:

```bash
npx skills add gradle/gradle-skills --skill gradle-best-practices
```

If `npx` is not found, install Node first (e.g. `brew install node`).

Rerun the command after a release to pick up changes, and again for any skill added since you installed.

## Usage

Skills are automatically available once installed.
The agent will use them when relevant tasks are detected.

**Example prompt to trigger `gradle-best-practices`:**

```text
Check this build against known best practices
```

## Repository Structure

The repository root is an [Agent Plugins](https://agent-plugins.org/) package: `plugin.json` is the portable manifest and `skills/` is the standard's fixed discovery location for skills. There is no `mcp.json`, which the standard permits.

The same tree is also laid out as a [Claude Code plugin marketplace](https://code.claude.com/docs/en/plugin-marketplaces): `.claude-plugin/` holds the marketplace catalog and Claude Code's own copy of the plugin manifest. `skills.sh.json` groups the skills by topic for `skills.sh`.

Each skill follows the [Agent Skills](https://agentskills.io/home) layout, and add a `metadata.json` recording its version, owning organization, abstract, and references.

## License

Apache License 2.0 — see [LICENSE](LICENSE).
