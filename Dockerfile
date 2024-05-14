FROM python:3.9-alpine3.13

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./backend /backend
COPY ./scripts /scripts
COPY ./backend/static /vol/web/static

WORKDIR /backend
EXPOSE 8000



RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home backend && \
    chown -R backend:backend /backend && \
    chmod -R 755 /backend && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R backend:backend /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts && \
    chown -R backend:backend /vol
RUN apk add --no-cache ffmpeg


ENV PATH="/scripts:/py/bin:$PATH"

USER backend

CMD ["run.sh"]