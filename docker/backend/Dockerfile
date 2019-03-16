FROM python:3.6

#RUN apt-get update && \
#    apt-get install default-libmysqlclient-dev

WORKDIR /app
COPY requirements.txt .
RUN rm -f /usr/bin/python && ln -s /usr/bin/python3.6 /usr/bin/python
RUN rm -f /usr/bin/python3 && ln -s /usr/bin/python3.6 /usr/bin/python3

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
RUN tar -xzf ta-lib-0.4.0-src.tar.gz
RUN  cd ta-lib/ && ./configure && make && make install
RUN pip3 install numpy
RUN pip3 install -r requirements.txt

ADD . /app
