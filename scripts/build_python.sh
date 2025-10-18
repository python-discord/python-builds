#!/usr/bin/env bash
set -euxo pipefail
shopt -s inherit_errexit

py_version="${1}"

if [[ $py_version == *j ]]; then
    # Enable JIT mode when passed a version that ends with a "j"
    py_version="${py_version%j}"
    PYTHON_CONFIGURE_OPTS+=" --enable-experimental-jit --with-tail-call-interp"
fi

"${PYENV_ROOT}/plugins/python-build/bin/python-build" \
    "${py_version}" \
    "/snekbin/"
"/snekbin/bin/python" -m pip install -U pip

# Clean up some unnecessary files to reduce image size bloat.
find /snekbin/ -depth \
\( \
    \( -type d -a \( \
        -name test -o -name tests -o -name idle_test \
    \) \) \
    -o \( -type f -a \( \
        -name '*.pyc' -o -name '*.pyo' -o -name 'libpython*.a' \
    \) \) \
\) -exec rm -rf '{}' +
