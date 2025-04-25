FROM python:3.12-alpine AS build
ARG MRMAT_VERSION="0.0.0.dev0"
ADD dist/mrmat_python_api_fastapi-*-py3-none-any.whl /
RUN pip install --user /mrmat_python_api_fastapi-*-py3-none-any.whl

FROM python:3.12-alpine
ARG MRMAT_VERSION="0.0.0.dev0"
LABEL VERSION=$MRMAT_VERSION
RUN addgroup -g 1000 app && \
    adduser -g 'App User' -u 1000 -G app -D app
COPY --from=build /root/.local /home/app/.local
RUN chown -R 1000:1000 /home/app/.local

USER app:app
EXPOSE 8000
#CMD ["/home/app/.local/bin/uvicorn", "--host", "0.0.0.0", "--port", "8000", "mrmat_python_api_fastapi.app:app"]
CMD ["/home/app/.local/bin/mrmat-python-api-fastapi"]
