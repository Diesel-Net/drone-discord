FROM python:3.9
# TODO: update to python version 3.9

# Upgrade pip and setuptools
RUN pip3 install --upgrade pip \
&& pip3 install --upgrade setuptools \
&& pip3 install --upgrade wheel

# Set the environment variables
ENV PYTHONUNBUFFERED=TRUE
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Source code
COPY client-requirements.txt .
COPY README.md .
COPY client.py .

# Install package with 'test' extras from setup.py
RUN pip3 install -r client-requirements.txt

# Expose the flask port
EXPOSE 5000

ENTRYPOINT [ \
    "python3", \
    "client.py" \
]
