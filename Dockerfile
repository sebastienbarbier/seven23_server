FROM python:3.12-slim-bookworm

WORKDIR /app
RUN mkdir /app/collectstatic

RUN adduser --disabled-password --gecos "" seven23
RUN chown seven23:seven23 /app /app/collectstatic
VOLUME /app/collectstatic

COPY --chown=seven23 . .

RUN apt-get update && \
 apt-get install -y --no-install-recommends \
   libpq5 libjpeg62-turbo zlib1g libffi8 && \
 apt-get install -y --no-install-recommends \
   gcc libpq-dev libjpeg-dev zlib1g-dev libffi-dev && \
 python -m pip install --upgrade pip --no-cache-dir && \
 python -m pip install -r requirements.txt --no-cache-dir && \
 apt-get purge -y --auto-remove gcc libpq-dev libjpeg-dev zlib1g-dev libffi-dev && \
 rm -rf /var/lib/apt/lists/*

USER seven23
EXPOSE 8000

ENTRYPOINT [ "/app/docker/entrypoint.sh" ]
