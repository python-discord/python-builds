FROM ghcr.io/python-discord/python-builds:builder-base AS python-builder
LABEL org.opencontainers.image.authors="Joe Banks <joe@owlcorp.uk>, Chris Lovering <cj@owlcorp.uk>"

ARG PYTHON_VERSION

RUN [ -z "$PYTHON_VERSION" ] && echo "PYTHON_VERSION Docker build arg is required" && exit 1 || true

RUN /scripts/build_python.sh ${PYTHON_VERSION}
