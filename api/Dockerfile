FROM python:3.8.2-buster

COPY update-packages.sh .
RUN chmod +x ./update-packages.sh && ./update-packages.sh

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 8000

RUN useradd --create-home appuser
WORKDIR /home/appuser/
USER appuser

RUN mkdir app
WORKDIR /home/appuser/app

COPY api/ ./api/

COPY main.py . 

ENTRYPOINT [ "/entrypoint.sh" ]