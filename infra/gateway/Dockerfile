FROM python:3.15.0-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
COPY requirements/runtime.txt /tmp/runtime.txt
RUN python -m pip install --no-cache-dir --requirement /tmp/runtime.txt \
    && useradd --create-home --uid 10001 oc2
COPY --chown=oc2:oc2 services /app/services
COPY --chown=oc2:oc2 web /app/web
USER oc2
EXPOSE 8088
CMD ["python", "-m", "services.gateway"]
