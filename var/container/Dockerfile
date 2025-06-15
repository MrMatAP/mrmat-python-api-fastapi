FROM python:3.13-alpine AS build
ARG MRMAT_VERSION="0.0.0.dev0"
ARG GIT_SHA=""
ARG WHEEL=""
ADD "$WHEEL" /
RUN pip install --user /mrmat_python_api_fastapi-*.whl

FROM python:3.13-alpine
ARG MRMAT_VERSION="0.0.0.dev0"
ARG GIT_SHA=""

LABEL org.opencontainers.image.title="MrMat :: Python API :: FastAPI"
LABEL org.opencontainers.image.description="A demonstration of common API interactions using Python's FastAPI"
LABEL org.opencontainers.image.authors="MrMat"
LABEL org.opencontainers.image.vendor="The MrMat Organisation"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.version="$MRMAT_VERSION"
LABEL org.opencontainers.image.revision="$GIT_SHA"
LABEL org.opencontainers.image.source="https://github.com/MrMatAP/mrmat-python-api-fastapi"

RUN addgroup -g 1000 app && \
    adduser -g 'App User' -u 1000 -G app -D app
COPY --from=build /root/.local /home/app/.local
RUN chown -R 1000:1000 /home/app/.local

USER app:app
EXPOSE 8000
CMD ["/home/app/.local/bin/opentelemetry-instrument", \
     "/home/app/.local/bin/uvicorn", "--host", "0.0.0.0", "--port", "8000", "mrmat_python_api_fastapi.app:app"]
