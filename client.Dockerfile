FROM python:3.9

RUN pip3 install --upgrade pip \
&& pip3 install --upgrade setuptools \
&& pip3 install --upgrade wheel

ENV PYTHONUNBUFFERED=TRUE
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY client-requirements.txt .
COPY README.md .
COPY client.py .

RUN pip3 install -r client-requirements.txt

ENTRYPOINT [ \
    "python3", \
    "client.py" \
]
