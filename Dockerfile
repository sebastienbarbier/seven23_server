FROM python:3.7-alpine

WORKDIR /app

COPY . .

RUN \
 apk add --no-cache postgresql-libs bash && \
 apk add --no-cache --virtual .build-deps alpine-sdk postgresql-dev && \
 python -m pip install --upgrade pip --no-cache-dir && \
 python -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

EXPOSE 8000

ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
