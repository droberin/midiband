FROM python:3-slim

RUN apt-get update && \
 apt-get install -y gcc && \
 apt-get clean && \
 rm -fr /var/cache/apt/archives/

ADD midiband /midiband/midiband
COPY setup.py /midiband/setup.py
COPY docker-entrypoint-server.py /entrypoint-server.py
RUN pip3 install -e midiband

ENTRYPOINT /entrypoint-server.py
