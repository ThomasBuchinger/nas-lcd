FROM ubuntu:23.04

RUN apt-get update && \
    apt-get install -y \
        i2c-tools \
        python3-smbus \
        libi2c-dev \
        python3-dev \
        vim

WORKDIR /app
ADD ./ /app
CMD [ "python3", "hello_world.py", "0", "27" ]
