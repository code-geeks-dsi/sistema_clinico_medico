FROM python:3.10.4-alpine3.15

COPY requirements.txt /app/requirements.txt

RUN set -ex \
        && pip install --upgrade pip \
        && pip install --no-cache-dir -r  /app/requirements.txt

WORKDIR /app

ADD . .

# RUN mkdir static && python manage.py collectstatic

EXPOSE 8000

CMD ["gunicorn","--bind",":8000","--workers","3","sistema_clinico_medico.wsgi:application"]

