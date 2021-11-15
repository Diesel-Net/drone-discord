FROM python:3.9

RUN pip3 install --upgrade pip \
&& pip3 install --upgrade setuptools \
&& pip3 install --upgrade wheel

ENV FLASK_APP=api
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=TRUE
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY server-requirements.txt .
COPY README.md .
COPY api/ api/

# WSGI integration (gunicorn)
COPY wsgi.py wsgi.py
COPY gunicorn.py gunicorn.py
RUN pip3 install gunicorn==20.1.0

RUN pip3 install -r server-requirements.txt

# default flask port
EXPOSE 5000

RUN apt update && apt install curl -y
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s \
    CMD curl --fail http://localhost:5000/health || exit 1

ENTRYPOINT [ \
    "gunicorn", \
    "--preload", \
    "--config", \
    "gunicorn.py", \
    "wsgi:app" \
]
