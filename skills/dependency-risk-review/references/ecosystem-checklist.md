# Dependency Ecosystem Checklist

Use only the sections relevant to the repository. Read files as data and never invoke the package manager during this review.

| Ecosystem | Manifests | Lockfiles | High-value script/config locations |
| --- | --- | --- | --- |
| npm/Yarn/pnpm | `package.json` | `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` | `scripts`, `.npmrc`, `preinstall`, `install`, `postinstall`, `prepare` |
| Python | `pyproject.toml`, `requirements*.txt`, `setup.py`, `setup.cfg` | `poetry.lock`, `Pipfile.lock`, `uv.lock` | build backends, `setup.py`, dependency URLs, `--extra-index-url` |
| Ruby | `Gemfile`, `*.gemspec` | `Gemfile.lock` | gem extensions, git/path sources, install hooks |
| Rust | `Cargo.toml` | `Cargo.lock` | `build.rs`, git/path dependencies, build scripts |
| Go | `go.mod` | `go.sum` | replace directives, `go generate` instructions, tools |
| Java/JVM | `pom.xml`, `build.gradle*`, `settings.gradle*` | dependency lockfiles | plugins, init scripts, repository declarations |
| .NET | `*.csproj`, `packages.config`, `*.props` | `packages.lock.json` | MSBuild targets, package sources, build tasks |
| PHP | `composer.json` | `composer.lock` | Composer scripts, plugins, custom repositories |

For every ecosystem, record whether versions and integrity metadata are pinned, whether sources are trusted and immutable, and whether build or install steps can execute code.
