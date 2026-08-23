import json
import os
from pathlib import Path

import tomllib


def resolve_version(friendly_version: str) -> str:
    """Resolve a friendly version like '3.10t' to an exact version like '3.10.12'."""
    # Strip JIT for now as it's not recognized by pyenv
    is_free_threaded = friendly_version.endswith('t')
    is_jit = friendly_version.endswith('j')
    base_version = friendly_version.rstrip('jt')

    pyenv_root = Path(os.environ.get("PYENV_ROOT", "/pyenv"))
    pyenv_versions = pyenv_root / "plugins/python-build/share/python-build"

    matching_versions = []

    for version_file in pyenv_versions.glob(f"{base_version}.*"):
        version_str = version_file.name

        if version_str.endswith("-dev"):
            continue

        if version_str.endswith("t") and is_free_threaded:
            matching_versions.append(version_str.rstrip('t'))
        elif not version_str.endswith("t"):
            matching_versions.append(version_str)

    if not matching_versions:
        raise ValueError(f"No matching versions found for base version '{base_version}'")

    def version_sort_key(s):
        def part_key(p):
            n, *rc = p.split('rc')
            # rc suffix sorts below final release (no rc = inf)
            return (int(n), int(rc[0]) if rc else float('inf'))
        return [part_key(p) for p in s.split('.')]

    matching_versions.sort(key=version_sort_key)

    latest_version = matching_versions[-1]

    latest_version += 'j' if is_jit else ''
    latest_version += 't' if is_free_threaded else ''

    return latest_version

if __name__ == "__main__":
    versions_toml_path = Path(os.environ.get("VERSIONS_TOML", "/versions.toml"))

    if not versions_toml_path.exists():
        raise FileNotFoundError(f"Could not find versions.toml at expected path: {versions_toml_path}")

    with versions_toml_path.open("rb") as f:
        versions_config = tomllib.load(f)

    friendly_versions = set(versions_config["config"]["versions"])

    resolved_versions = [
        {"tag": v, "version": resolve_version(v)} for v in friendly_versions
    ]

    print(json.dumps(resolved_versions))
