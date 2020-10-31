FROM python:3.8-buster AS builder

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt


FROM python:3.8-slim-buster

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd --create-home appuser
WORKDIR /home/appuser/
USER appuser

COPY --from=builder /opt/venv/ /home/appuser/venv/
ENV PATH="/home/appuser/venv/bin:$PATH"

COPY ./api/ api/

EXPOSE 8000
ENTRYPOINT python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
