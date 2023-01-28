FROM alpine:latest

RUN apk add py3-pip
RUN pip install selenium

COPY autosnap.py ./
RUN echo '20       16       *       *       *       /autosnap.py' >> /etc/crontabs/root
RUN echo '9        6        *       *       *       /autosnap.py' >> /etc/crontabs/root

CMD ["sleep", "infinity"]
