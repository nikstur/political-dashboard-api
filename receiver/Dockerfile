FROM python:3.8-buster AS builder

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt


FROM python:3.8-slim-buster

COPY update-packages.sh .
RUN chmod +x ./update-packages.sh && ./update-packages.sh

RUN useradd --create-home appuser
WORKDIR /home/appuser/
USER appuser

COPY --from=builder /opt/venv /home/appuser/venv
ENV PATH="/home/appuser/venv/bin:$PATH"

COPY receiver/ receiver/

ENTRYPOINT [ "python", "-m", "receiver.main" ]
