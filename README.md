# Gradle Skills

[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](LICENSE)

Skills that teach AI coding agents how to work on Gradle builds.

They follow the [Agent Skills](https://agentskills.io/home) format, so they work in any agent that reads it: Claude Code, Codex, Cursor, Gemini CLI, and others.

## Available Skills

### gradle-best-practices [![v1.0.0](https://img.shields.io/badge/v1.0.0-02303A?logo=gradle&logoColor=white)](skills/gradle-best-practices)

Audits a build against the [official Gradle best practices](https://docs.gradle.org/current/userguide/best_practices.html) and reports what it finds, ordered by impact. Ask it to, and it applies the fixes.

It reads build scripts, settings files, `gradle.properties`, the wrapper config, the version catalog, and the plugin code under `buildSrc/` and `build-logic/`. Every finding links to the practice it came from.

[Benchmark results](evals/gradle-best-practices/gradle-best-practices-1.0.0.md) across several models and agents.

Try:

- "Check my build"
- "Audit this Gradle project"
- "Apply Gradle best practices"

### gradle-wrapper-upgrade [![v1.0.0](https://img.shields.io/badge/v1.0.0-02303A?logo=gradle&logoColor=white)](skills/gradle-wrapper-upgrade)

Upgrades the Gradle wrapper, to the latest release or to a version you name. It pins the distribution's checksum, regenerates `gradlew`, `gradlew.bat`, and the wrapper jar, and then checks that the build still configures on the new version. If it doesn't, the upgrade is rolled back and you get a smaller version step to try instead, with the release notes for it.

Ask *how* to upgrade and you get the commands, not a changed working tree.

It upgrades a wrapper that already exists. It won't add one to a project that has none, and it won't edit your build scripts.

[Benchmark results](evals/gradle-wrapper-upgrade/gradle-wrapper-upgrade-1.0.0.md) across several models and agents.

Try:

- "Upgrade the Gradle wrapper"
- "Bump Gradle to 8.14.4"
- "How do I upgrade the wrapper?"

## Installation

Install all of them. A skill costs nothing until the agent triggers it.

### Claude Code

```text
/plugin marketplace add gradle/gradle-skills
/plugin install gradle-skills@gradle-skills
```

Claude Code namespaces skills that come from a plugin, so these load as `gradle-skills:gradle-best-practices` and `gradle-skills:gradle-wrapper-upgrade`.

To set this up for a whole team, commit to the project's `.claude/settings.json`:

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

That registers the marketplace, but doesn't fetch the plugin. Each collaborator still runs the install once:

```bash
claude plugin install gradle-skills@gradle-skills
```

### Codex, Cursor, Gemini CLI, and others

```bash
npx skills add gradle/gradle-skills
```

Choose your agents when prompted. The skills are written to `.agents/skills/` in the current project; pass `-g` to install them for every project instead. Re-run the command to update.

This covers around 80 agents. [`skills.sh`](https://skills.sh/) has the list, and `npx` needs Node (`brew install node`).

### Anything else

The repository root is also an [Agent Plugins 1.0.0](https://github.com/agentplugins/agent-plugins-spec/blob/main/spec/1.0.0.md) package: `plugin.json` is the manifest, `skills/` holds the skills. Clients that implement the standard can install it directly. Each defines its own procedure, so check your agent's docs or the [list of compatible clients](https://agent-plugins.org/compatible-clients).

## Repository Structure

```text
plugin.json        Agent Plugins manifest
skills.sh.json     skills.sh grouping
.claude-plugin/    Claude Code plugin manifest and marketplace catalog
skills/<name>/
  SKILL.md         instructions, loaded when the skill triggers
  metadata.json    version, owner, abstract, sources
  references/      loaded on demand, not on trigger
```

## License

Apache License 2.0 — see [LICENSE](LICENSE).
