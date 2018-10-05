FROM python:3.6.5-alpine3.7

ENV BASE_DIR_DIR /opt/webapp/

COPY requirements.txt .

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN rm -r requirements.txt

RUN mkdir -p $BASE_DIR_DIR/source/
WORKDIR $BASE_DIR_DIR

COPY run.sh /usr/bin

COPY source $BASE_DIR_DIR/source/
ENV PROJECT_ROOT $BASE_DIR_DIR/source/

EXPOSE 5000
WORKDIR $PROJECT_ROOT
CMD ["run.sh"]
