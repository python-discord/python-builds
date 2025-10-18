# Python Builds

This repository hosts prebuilt versions of Python that are used for the `!eval`
functionality of [`python-discord/bot`](https://github.com/python-discord/bot).

Built images contain a folder `/snekbin/` which contains the built Python
interpreter.

The subdirectory that contains the interpreter varies by the requested version,
for example, Python `3.14j` will have a binary at
`/snekbin/python/3.14j/bin/python`.

## Adding new versions

To add new versions to the build matrix, edit the `versions.toml` file to include
the desired versions. The GitHub Actions workflow will automatically build and
push the new versions when changes are merged to the main branch.

Additionally, new patch versions are automatically built as part of the cron job
that runs daily. As long as pyenv is updated upstream with the new patch versions,
they will be picked up and built without any manual intervention.

### Version Suffixes

Some Python versions have suffixes, these are specified as follows:

| Suffix | Meaning                               |
| ------ | ------------------------------------- |
| `j`    | JIT enabled build (e.g., `3.11.0j`)   |
| `t`    | Free-threaded build (e.g., `3.11.0t`) |

## GitHub Actions

A manual build can be triggered by going to the "Actions" tab and selecting the
"Build Python Interpreters" workflow. From there, click the "Run workflow" button.

## Built Images

Built images are pushed to the GitHub Container Registry at
[`ghcr.io/python-discord/python-builds`](https://ghcr.io/python-discord/python-builds).
The images are tagged with the Python version they contain, e.g., `3.10.8` as well as
the short tag, e.g., `3.10`.
