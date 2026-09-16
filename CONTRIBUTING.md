# Contributing

## Development setup

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
uv sync --all-extras
uv run pytest
uv run ruff check .
uv run ruff format .
```

`requirements.txt` is a generated file for consumers who don't use uv. Never hand-edit it — regenerate it after changing dependencies in `pyproject.toml`:

```bash
uv lock
uv export --no-hashes --no-dev --format requirements-txt -o requirements.txt
```

## Release process

1. Bump `version` in `pyproject.toml` following [Semantic Versioning](https://semver.org/).
2. Move the relevant `[Unreleased]` entries in `CHANGELOG.md` under a new `## [X.Y.Z] - YYYY-MM-DD` heading, and add the corresponding comparison link at the bottom of the file.
3. Commit the version bump and changelog update.
4. Tag the commit: `git tag vX.Y.Z && git push origin vX.Y.Z`.
5. Create a GitHub Release from that tag. This triggers the `release.yml` workflow, which builds the package and publishes it to PyPI via trusted publishing.
