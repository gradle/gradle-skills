# Contributing to Gradle Skills

Thank you for your interest in contributing!
This repository packages skills that teach AI coding agents to work on Gradle builds.
This guide covers how to propose a change, what a skill here is expected to look like, and what to check before you open a pull request.

## Before you start

Open an issue before starting work on a new skill or a substantial change to an existing one, or comment on an existing issue.

For a new skill, the issue should answer:

- What task does it cover, and what does an agent get wrong on that task without it?
- Why is it not part of an existing skill?
- What would a successful run look like, and how would you tell it apart from a failed one?

Small fixes — a wrong command, a broken link, outdated guidance — can go straight to a pull request.

### Security vulnerabilities

Do not report security vulnerabilities to the public issue tracker.
Follow the [security policy](https://github.com/gradle/gradle-skills/security/policy).

### Code of Conduct

This project is governed by the [Code of Conduct](CODE_OF_CONDUCT.md), which applies to issues, pull requests, and discussions.

## What makes a good skill

Skills in this repository follow the [Agent Skills specification](https://agentskills.io/specification) and must work in any agent that supports it.
Read the specification before writing a skill; for guidance on writing one well, see Anthropic's [Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) and its [`skill-creator` skill](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/skill-creator/skills/skill-creator/SKILL.md). Their advice applies beyond Claude.

On top of the specification, this repository expects:

- **A procedure, not advice.** Give the agent steps it can follow and a way to check the result. "Verify by diff" is a step; "be careful" is not.
- **Narrow.** A skill does one job and says what it does not do. `gradle-wrapper-upgrade` upgrades an existing wrapper; it does not add one or repair the build.
- **Harness-agnostic.** Describe capabilities, not one agent's tool names, and do not rely on a specific model's behavior.
- **Offline and reproducible where possible.** If the skill needs reference material, ship it under `references/` rather than fetching it at run time.
- **Cheap to load.** Everything in `SKILL.md` is read on every run. Move material that only some runs need into `references/` and tell the agent exactly when to open it.
- **Correct for the Gradle versions it claims.** State the supported range and check commands and APIs against the documentation for those versions.

## Repository layout

```text
skills/<skill-name>/
├── SKILL.md          # frontmatter + instructions the agent follows
├── metadata.json     # version, organization, date, abstract, references
└── references/       # optional, loaded on demand

evals/<skill-name>/
└── <skill-name>-<version>.md   # published evaluation, one per released version
```

Beyond the `name` and `description` the specification requires, `SKILL.md` frontmatter here must include `license`, `metadata.author`, and `metadata.version`. The consistency check enforces all five.
The `description` is what the agent uses to decide whether to load the skill, so name the task and the phrases that should trigger it.

Adding a skill also touches files outside its directory:

- `README.md` — a `### <skill-name>` section with a version badge, a short description, and example prompts.
- `skills.sh.json` — the skill in a grouping.
- `plugin.json`, `.claude-plugin/plugin.json`, and `.claude-plugin/marketplace.json` — update `description` and `keywords` if the plugin's scope changes. The three files must stay identical on every field they share; `version` is not one of them, and the marketplace entry must not set it (see [Versions](#versions)).

## Testing your change

Maintainers evaluate skills with an internal benchmark before each release; results are published under [`evals/`](evals).
That framework is not public yet, so a pull request cannot be expected to include benchmark results.
Instead, test the skill by hand and describe what you did in the pull request:

1. Install the skill from your working copy, either with `npx skills add ./` or, in Claude Code, with `claude --plugin-dir .`.
2. Run it against at least one real Gradle project where the skill applies, and one where it should decline or stop.
3. Run the same prompt without the skill, and compare.

Note the agent, the model, the Gradle version, and the prompts you used.

## Checks

CI runs these on every pull request; run them locally first:

```bash
# Lint Markdown
npx markdownlint-cli2 "**/*.md"

# Validate JSON syntax
find . -name '*.json' -not -path './.git/*' -print0 | xargs -0 -I{} jq empty "{}"

# Check that every text file ends with a newline
git ls-files -z | while IFS= read -r -d '' f; do
  if [ -s "$f" ] && grep -Iq . "$f" && [ -n "$(tail -c1 "$f")" ]; then
    echo "missing final newline: $f"
  fi
done

# Check manifests, skill versions, and links
python3 .github/scripts/check-consistency.py
```

The consistency check verifies that `plugin.json` satisfies the Agent Plugins manifest rules, that the three plugin manifests agree, that each skill's `SKILL.md` declares the frontmatter this repository requires and states the same version as its `metadata.json`, that no skill version is ahead of the plugin version, that `README.md` has a correct version badge per skill, and that every relative link in the root Markdown docs resolves.

## Versions

Leave version numbers alone unless a maintainer asks otherwise; they are set when a release is cut.

Each skill and the plugin that bundles them have separate versions, with different jobs:

- A **skill version** records what changed in that skill, and is the version its evaluation under `evals/` refers to. It is stated in the skill's `SKILL.md` (`metadata.version`), its `metadata.json`, and its README badge.
- The **plugin version** is what installed copies are updated by. Clients compare it to decide whether an update is available: Claude Code does, and the Agent Plugins specification permits any client to. It is stated in `plugin.json` and `.claude-plugin/plugin.json`, and nowhere else — Claude Code ignores a version in the marketplace entry in favor of `.claude-plugin/plugin.json`.

A skill change that ships without a plugin version bump never reaches plugin users. So when a release changes any skill:

1. Bump the version of each changed skill, following [Semantic Versioning](https://semver.org/).
2. Bump the plugin version by at least the largest of those bumps: a minor bump to any skill means at least a minor bump to the plugin. Adding a skill is a minor bump; removing one is a major bump.

Unchanged skills keep their versions, so a skill version can lag behind the plugin version, but can never be ahead of it.

## Commits

- [Write good commit messages](https://cbea.ms/git-commit/#seven-rules).
- [Sign off your commits](https://git-scm.com/docs/git-commit#Documentation/git-commit.txt---signoff) to indicate that you agree to the terms of the [Developer Certificate of Origin](https://developercertificate.org/). Pull requests from outside the Gradle organization can only be accepted if all commits are signed off. To sign off commits after the fact, run `git rebase --signoff origin/main` and force-push.
- Keep commits discrete and self-contained: one logical change per commit.

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE).
