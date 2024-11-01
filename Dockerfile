FROM python:3.10-slim

WORKDIR "/app"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1


COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY run.sh run.sh

COPY llm_agent llm_agent

CMD ["bash", "run.sh", "prod"]